import os
import io
import csv
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
from xvfbwrapper import Xvfb  # Import Xvfb from xvfbwrapper

app = Flask(__name__)

# Create a virtual display
vdisplay = Xvfb()

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
        # Start the virtual display
        vdisplay.start()

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

        # Rest of your code...

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
    finally:
        # Stop the virtual display in the finally block to ensure it stops even if an exception occurs
        vdisplay.stop()

if __name__ == '__main__':
    app.run(debug=True)
