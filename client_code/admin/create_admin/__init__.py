from ._anvil_designer import create_adminTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re

class create_admin(create_adminTemplate):
  def __init__(self, user=None, **properties):
    self.init_components(**properties)
    self.user = user
    self.label_12.text = datetime.now().strftime('%d %b %Y')
    self.which_admin_created_account = user['username']
    print(self.which_admin_created_account)

  def button_1_click(self, **event_args): 
        date_of_admins_account_created = datetime.now().date()
        existing_admin = anvil.server.call('get_admin_by_phone', str(self.text_box_4.text).strip())

        if existing_admin:
            alert('You have already signed up with this phone number.')
        else:
          count=0
          phone_number = str(self.text_box_4.text).strip()
          if self.validate_phone_number(phone_number):
              count=count+1
              self.label_13.text ="Phone number is correct"
          else:
              self.label_13.text ="Please check the entered phone number"
              self.text_box_4.text=''
              self.text_box_4.focus()
          if self.text_box_5.text != '':
            if self.text_box_5.text != self.text_box_6.text:
              self.label_9.text = "Passwords doesn't match"
              self.text_box_5.text =''
              self.text_box_5.focus()
              self.text_box_6.text =''
              self.text_box_6.focus()
            elif self.text_box_5.text == self.text_box_6.text:
              self.label_9.text = "Password matches"  
        
              if count==1:
                
                anvil.server.call(
                  'add_admins_info',  
                  self.text_box_1.text, 
                  self.text_box_2.text,
                  self.text_box_4.text,
                  self.text_box_5.text,
                )
                print('Admin credentials stored for login')
                app_tables.wallet_admins_create_admin_account.add_row(
                    admins_username=self.text_box_1.text,
                    admins_email=self.text_box_2.text,
                    admins_phone=self.text_box_4.text,
                    admins_password=self.text_box_5.text,
                    admins_date_of_birth=self.date_picker_1.date,
                    admins_gender=self.drop_down_1.selected_value,
                    which_admin_created_account=f'Admin - {self.which_admin_created_account}',
                    date_of_admins_account_created=date_of_admins_account_created,
                    #usertype='admin',
                    admins_last_login=datetime.now()
                  )
                alert (self.text_box_1.text + ' added')
                open_form('admin')

  def validate_button_click(self, **event_args):
    phone_number = str(self.text_box_6.text).strip()  

  def validate_phone_number(self, phone_number):
      pattern = r'^[6-9]\d{9}$'
      if re.match(pattern, str(phone_number)):
          return True  
      else:
          return False  

  def link_8_copy_click(self, **event_args):
    open_form('admin', user=self.user)
