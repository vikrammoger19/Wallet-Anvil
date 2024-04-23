from ._anvil_designer import signupTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
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
            self.text_box_3.text=''
        else:
            count=0
            phone_number = str(self.text_box_3.text).strip()
        
            if self.validate_phone_number(phone_number):
              count=count+1
        
            else:
              self.phone_card.visible = True
              self.label_15.text ="Invalid Phone Number"
              self.label_15.foreground = "#990000"
              self.text_box_3.text=''
              self.text_box_3.focus()
            aadhar= int(self.text_box_7.text)
            if len(str(aadhar)) == 12:
              count=count+1
      
            else:
              self.aadhar_card.visible = True
              self.label_16.text ="Please verify the entered Aadhar details"
              self.label_16.foreground = "#990000"
              self.text_box_7.text=''
              self.text_box_7.focus()
            converted_text = self.text_box_8.text 
            if self.is_pan_card_detail(converted_text):
              
              count=count+1
            else:
              self.pan_card.visible = True
              self.label_14.text ="Please verify the entered pan card details"
              self.label_14.foreground = "#990000"
              self.text_box_8.text=''
              self.text_box_8.focus()

            if self.text_box_5.text != '':
              if self.text_box_5.text != self.text_box_6.text:
                self.pass_card.visible = True
                self.label_17.text = "Passwords doesn't match"
                self.label_17.foreground = "#990000"
                self.text_box_5.text =''
                self.text_box_5.focus()
                self.text_box_6.text =''
                self.text_box_6.focus()
              elif self.text_box_5.text == self.text_box_6.text:
                self.label_17.text = "Password matched"
                self.label_4.foreground = "#008000"
      
                count=count+1 
         
            if count==4:
              anvil.server.call(
                'add_info', 
                self.text_box_1.text, 
                self.text_box_2.text,
                self.drop_down_1.selected_value,
                self.text_box_3.text,
                self.text_box_7.text,
                self.text_box_8.text,
                self.text_box_6.text
              )
              alert ("Thank you "+ self.text_box_1.text + ", for signing up! Your account has been successfully created")
              open_form('login')
