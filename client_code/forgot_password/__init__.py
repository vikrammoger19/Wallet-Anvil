from ._anvil_designer import forgot_passwordTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random

class forgot_password(forgot_passwordTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Get the email entered by the user
        user_email = self.text_box_1.text
        
        # Query the wallet_users table to check if the email exists
        matching_users = app_tables.wallet_users.search(email=user_email)
        
        if matching_users:
            # Email exists, generate OTP and send it
            otp = self.generate_otp()
            self.send_otp_email(user_email, otp)
            # Optionally, you can inform the user that the OTP has been sent
            alert("OTP has been sent to your email.")
        else:
            # Email doesn't exist, display an error message
            alert("Email not found. Please enter a valid email address.")
    
    def generate_otp(self):
        # Generate a 6-digit OTP
        otp = ''.join(random.choice('0123456789') for _ in range(6))
        return otp
    
    def send_otp_email(self, recipient_email, otp):
        # Compose email message
        subject = "Your One Time Password (OTP)"
        message = f"Your OTP is: {otp}"
        
        # Send email
        anvil.email.send(
            to=recipient_email,
            subject=subject,
            text=message
        )
