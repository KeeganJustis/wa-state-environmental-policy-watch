import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import *


from datetime import date



def get_current_date() -> str:
    """Get the current date as a string.

    Returns:
        str: The current date formatted as MM-DD-YYYY.
    """
    try:
        current_date = date.today()
        return current_date.strftime("%m-%d-%Y-")
    except Exception as e:
        # Log error and re-raise to be handled by caller
        print(f"Error getting current date: {e}")
        raise



def send_summary(summary):


    try:
        message = Mail(
            from_email='keeganjustis@gmail.com',
            to_emails='keeganjustis@gmail.com',
            subject=f'Washington State Plastic Legislation Update {get_current_date()}',    
            html_content=summary
            )
        api_key = os.environ.get('SENDGRID_API_KEY')
        sg = sendgrid.SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

