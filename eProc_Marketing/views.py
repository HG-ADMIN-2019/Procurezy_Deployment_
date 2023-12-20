import io
import csv
import os
import re
import datetime
import time
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import pywhatkit as kit
from io import TextIOWrapper
from io import StringIO

from django.views.decorators.csrf import csrf_exempt
from flask.app import Flask

app = Flask(__name__)


def index(request):
    context = {
        'inc_nav': True,
        'inc_footer': True,
        'is_slide_menu': True,
        'is_configuration_active': True
    }
    return render(request, 'marketing.html', context)


def send_whatsapp_message(phone_number, message, image_path, send_time):
    try:
        # Check if either message or image is missing
        if not message and not image_path:
            print("Both message and image are missing. Nothing to send.")
            return

        # Get the current time
        now = datetime.datetime.now()

        # Calculate the delay until the scheduled time
        delay = (send_time - now).total_seconds()

        # If the scheduled time is in the future, wait until it's time to send
        if delay > 0:
            print(f"Waiting for {delay} seconds until the scheduled send time.")
            time.sleep(delay)

        # Send the completed message (either text or image or both)
        if message or image_path:
            kit.sendwhats_image(phone_number, image_path, caption=message)

            # Wait for a few seconds before moving on
            time.sleep(5)

            print(f"Message sent successfully to {phone_number}")

    except Exception as e:
        print(f'Error sending message to {phone_number}: {str(e)}')
        import traceback
        traceback.print_exc()


@csrf_exempt
def send_message(request):
    global image_path
    try:
        message = request.POST['message']
        start_hours = int(request.POST['hours'].strip('"'))
        start_minutes = int(request.POST['minutes'])
        csv_file = request.FILES['csv']
        image_file = request.FILES.get('image')

        # Save the image to the specified directory if provided
        if image_file:
            image_path = os.path.join(settings.MEDIA_ROOT, 'image.jpg')
            with open(image_path, 'wb') as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

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

        # Calculate the interval between each contact (adjust as needed)
        interval = datetime.timedelta(minutes=1)

        # Get the current time and calculate send_time for the first contact
        now = datetime.datetime.now()
        send_time = now.replace(hour=start_hours, minute=start_minutes, second=0, microsecond=0) + datetime.timedelta(
            seconds=5)

        # Call the existing function for each phone number
        for phone_number in phone_numbers:
            try:
                # Send both text message and image at the same time
                send_whatsapp_message(phone_number, message, image_path, send_time)

                # Increment send_time for the next contact
                send_time += interval

                # Handle hour transition
                if send_time.minute >= 60:
                    send_time = send_time.replace(hour=send_time.hour + 1, minute=send_time.minute % 60)

            except Exception as e:
                print(f'Error sending message to {phone_number}: {str(e)}')

        return JsonResponse({'result': 'Messages sent successfully'})
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'result': f'Error: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
