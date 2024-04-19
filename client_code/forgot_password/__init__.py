from ._anvil_designer import forgot_passwordTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random
from anvil import alert
import time

class forgot_password(forgot_passwordTemplate):
    def button_1_click(self, **event_args):
        user_email = self.text_box_1.text
        matching =app_tables.wallet_users.search(useemail=email)
        if user_email==matching:
          self.label_3.text="email is valid"
        else:
          self.label_3.text="email is invalid"
        # Check if the email exists in the database
        if anvil.server.call('validate_email', user_email):
            # Email exists, generate OTP
            otp = anvil.server.call('generate_otp')
            
            # Call the server function to send OTP via email
            anvil.server.call('send_otp_email', user_email, otp)
            
            # Inform the user that the OTP has been sent
            alert("OTP has been sent to your email.")
        else:
            # Email doesn't exist, display an error message
            alert("Email not found. Please enter a valid email address.")
    
    def text_box_2_pressed_enter(self, **event_args):
    # Wait for a short duration before each attempt
      entered_otp = self.text_box_2.text
        
        # Get the stored OTP from the server
      stored_otp = anvil.server.call('get_stored_otp')
        
        # Check if the entered OTP matches the stored OTP
      if entered_otp == stored_otp:
        # OTP is valid, display success message in green color
        self.label_4.text = "OTP is valid"
        self.label_4.foreground = "#008000"  # Green color
      else:
        # OTP is invalid, display a message
        self.label_4.text = "Invalid OTP. Please try again."
        self.label_4.foreground = "#FF0000"  # Red color