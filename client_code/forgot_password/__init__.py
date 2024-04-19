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
        
        # Check if the email exists in the database
        matching_users = app_tables.wallet_users.search(email=user_email)
        
        if matching_users:
            # Email exists, generate OTP
            otp = anvil.server.call('generate_otp')
            
            # Call the server function to send OTP via email
            anvil.server.call('send_otp_email', user_email, otp)
            
            # Inform the user that the OTP has been sent
            alert("OTP has been sent to your email.")
            
            # Hide text_box_2 and label_4, and show text_box_3
            self.text_box_2.visible = True
            
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
            
            # Hide text_box_3 and show text_box_4
            self.text_box_3.visible = True
            self.text_box_4.visible = True
            self.label_4.visible = True
        else:
            # OTP is invalid, display a message
            self.label_4.text = "Invalid OTP. Please try again."
            self.label_4.foreground = "#FF0000"  # Red color
            self.text_box_3.visible = False
            self.text_box_4.visible = False

    def primary_color_1_click(self, **event_args):
    # Check if both text_box_3 and text_box_4 are visible
      if self.text_box_3.visible and self.text_box_4.visible:
          # Check if passwords match
          if self.text_box_3.text == self.text_box_4.text:
              # Check if the new password meets the criteria
              new_password = self.text_box_4.text
              if (
                  len(new_password) >= 8
                  and any(char.isdigit() for char in new_password)
                  and any(char.isalpha() for char in new_password)
                  and any(not char.isalnum() for char in new_password)
              ):
                  # Password meets criteria, update the password
                  user_email = self.text_box_1.text
                  matching_users = app_tables.wallet_users.search(email=user_email)
                  if matching_users and len(matching_users) > 0:
                      matching_users[0]['password'] = new_password
                      matching_users[0].update()
                      alert("Password updated successfully!")
                      open_form('Login')
                  else:
                      alert("Email not found. Please enter a valid email address.")
              else:
                  # Password doesn't meet criteria, display error message
                  self.label_5.text = "Password must contain at least 8 characters, including at least one letter, one digit, and one special character."
                  self.label_5.foreground = "#FF0000"
          else:
              # Passwords don't match, display error message
              self.label_5.text = "Passwords don't match"
              self.label_5.foreground = "#FF0000"
      else:
          # If both text_box_3 and text_box_4 are not visible, display an error message
          alert("Please complete all previous steps before updating the password.")
