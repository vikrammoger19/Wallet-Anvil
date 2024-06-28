from ._anvil_designer import forgot_passwordTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
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
        matching_users = app_tables.wallet_users.search(users_email=user_email)
        
        if matching_users:
            # Email exists, inform the user to enter new password
            alert("Email found. Please enter a new password.")
            
            # Show text_box_3 and text_box_4
            self.text_box_3.visible = True
            self.text_box_4.visible = True
            self.label_4.visible = False
            
            # Uncomment the following lines to enable OTP functionality in the future
            # otp = anvil.server.call('generate_otp')
            # anvil.server.call('send_otp_email', user_email, otp)
            # alert("OTP has been sent to your email.")
            # self.text_box_2.visible = True
            
        else:
            # Email doesn't exist, display an error message
            alert("Email not found. Please enter a valid email address.")
    
    # Uncomment this method to enable OTP functionality in the future
    # def text_box_2_pressed_enter(self, **event_args):
    #     entered_otp = self.text_box_2.text
    #     stored_otp = anvil.server.call('get_stored_otp')
    #     if entered_otp == stored_otp:
    #         self.label_4.text = "OTP is valid"
    #         self.label_4.foreground = "#008000"  # Green color
    #         self.text_box_3.visible = True
    #         self.text_box_4.visible = True
    #         self.label_4.visible = True
    #     else:
    #         self.label_4.text = "Invalid OTP. Please try again."
    #         self.label_4.foreground = "#FF0000"  # Red color
    #         self.text_box_3.visible = False
    #         self.text_box_4.visible = False

  
    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("login")

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("signup")

  
    def primary_color_1_click(self, **event_args):
        if self.text_box_3.visible and self.text_box_4.visible:
            if self.text_box_3.text == self.text_box_4.text:
                new_password = self.text_box_4.text
                if (
                    len(new_password) >= 8
                    and any(char.isdigit() for char in new_password)
                    and any(char.isalpha() for char in new_password)
                    and any(not char.isalnum() for char in new_password)
                ):
                    user_email = self.text_box_1.text
                    matching_users = app_tables.wallet_users.search(users_email=user_email)
                    if matching_users and len(matching_users) > 0:
                        matching_users[0]['users_password'] = new_password
                        matching_users[0].update()
                        alert("Password updated successfully!")
                        open_form('login')
                    else:
                        alert("Email not found. Please enter a valid email address.")
                else:
                    self.label_5.visible= True
                    self.label_5.text = "Password must contain at least 8 characters, including at least one letter, one digit, and one special character."
                    self.label_5.foreground = "#FF0000"
            else:
                self.label_5.visible=True
                self.label_5.text = "Passwords don't match"
                self.label_5.foreground = "#FF0000"
        else:
            alert("Please complete all previous steps before updating the password.")
