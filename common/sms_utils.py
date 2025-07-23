import vonage # Import Vonage
from django.conf import settings

def send_sms(to_phone_number, message_body):
    api_key = settings.VONAGE_API_KEY
    api_secret = settings.VONAGE_API_SECRET
    vonage_phone_number = settings.VONAGE_PHONE_NUMBER

    if not api_key or not api_secret or not vonage_phone_number:
        print("Vonage credentials not configured. Skipping SMS.")
        return

    client = vonage.Client(key=api_key, secret=api_secret)
    sms = vonage.Sms(client)

    try:
        responseData = sms.send_message(
            {
                "from": vonage_phone_number,
                "to": to_phone_number,
                "text": message_body,
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print(f"SMS sent successfully! Message ID: {responseData['messages'][0]['message-id']}")
        else:
            print(f"Error sending SMS: {responseData['messages'][0]['error-text']}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
