from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import random

import re

class signup(signupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.card_4.visible = False
    self.phone_card.visible = False
    self.aadhar_card.visible = False
    self.pan_card.visible= False 
    self.pass_card.visible = False 

  def primary_color_1_click(self, **event_args):
        existing_user = anvil.server.call('get_user_by_phone', str(self.text_box_3.text).strip())

        if existing_user:
            self.card_4.visible = True
            self.text_box_3.text = ''
        else:
            count = 0
            phone_number = str(self.text_box_3.text).strip()

            if self.validate_phone_number(phone_number):

            else:
                self.phone_card.visible = True
                self.label_15.text = "Invalid Phone Number"
                self.label_15.foreground = "#990000"
                self.text_box_3.text = ''
                self.text_box_3.focus()
                
            aadhar = int(self.text_box_7.text)
            if len(str(aadhar)) == 12:

            else:
                self.aadhar_card.visible = True
                self.label_16.text = "Please verify the entered Aadhar details"
                self.label_16.foreground = "#990000"
                self.text_box_7.text = ''
                self.text_box_7.focus()
                
            converted_text = self.text_box_8.text 
            if self.is_pan_card_detail(converted_text):

            else:
                self.pan_card.visible = True
                self.label_14.text = "Please verify the entered pan card details"
                self.label_14.foreground = "#990000"
                self.text_box_8.text = ''
                self.text_box_8.focus()

            password = self.text_box_5.text
            confirm_password = self.text_box_6.text

            if self.validate_password(password) and self.validate_password(confirm_password) and password == confirm_password:
                count += 1
                self.label_17.text = "Passwords matched and valid"
                self.label_17.foreground = "#008000"
            else:
                self.pass_card.visible = True
                if password != confirm_password:
                    self.label_17.text = "Passwords don't match"
                else:
                    self.label_17.text = "Password should have at least one character, one number, and one symbol."
                self.label_17.foreground = "#FF0000"
                self.text_box_5.text = ''
                self.text_box_5.focus()
                self.text_box_6.text = ''
                self.text_box_6.focus()
