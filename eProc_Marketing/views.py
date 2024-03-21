import csv
import os
import re
import datetime
import time
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render
from flask import Flask, request
import pywhatkit as kit
from io import TextIOWrapper
from django.views.decorators.csrf import csrf_exempt

app = Flask(__name__)

def index(request):
    return render(request, 'home.html')

def send_whatsapp_message(phone_number, message, send_time):
    try:
        # Check if message is missing
        if not message:
            print("Message is missing. Nothing to send.")
            return

        # Send the message
        kit.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute)

        print(f"Message sent successfully to {phone_number}")
    except Exception as e:
        print(f'Error sending message to {phone_number}: {str(e)}')
        import traceback
        traceback.print_exc()

@csrf_exempt
def send_message(request):
    try:
        message = request.POST.get('message', '')  # Get 'message' with default value ''
        start_hours = int(request.POST.get('hours', 0))  # Get 'hours' with default value 0
        start_minutes = int(request.POST.get('minutes', 0))  # Get 'minutes' with default value 0
        csv_file = request.FILES.get('csv')

        # Decode the content manually
        csv_content = csv_file.read().decode('utf-8', errors='replace')

        # Use StringIO to create a file-like object for csv.reader
        from io import StringIO
        text_csv_file = StringIO(csv_content)

        # Read phone numbers from the CSV file
        phone_numbers = []
        with csv_file.open(mode='rb') as file:
            csv_content = re.sub(rb'[^\x00-\x7F]+', b'', file.read())
            text_csv_file = TextIOWrapper(io.BytesIO(csv_content), encoding='utf-8')

            reader = csv.DictReader(text_csv_file)
            for row in reader:
                if 'phone_number' in row:
                    phone_number = row['phone_number']
                    if not phone_number.startswith('+'):
                        phone_number = '+91' + phone_number

                    phone_numbers.append(phone_number)

        # Get the current time and calculate send_time for the first contact
        now = datetime.datetime.now()
        send_time = now.replace(hour=start_hours, minute=start_minutes, second=0, microsecond=0) + datetime.timedelta(seconds=5)

        # Call the existing function for each phone number
        for phone_number in phone_numbers:
            try:
                # Send text message
                send_whatsapp_message(phone_number, message, send_time)

                # Increment send_time for the next contact
                send_time += datetime.timedelta(minutes=1)

            except Exception as e:
                print(f'Error sending message to {phone_number}: {str(e)}')

        return JsonResponse({'result': 'Messages sent successfully'})
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'result': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
