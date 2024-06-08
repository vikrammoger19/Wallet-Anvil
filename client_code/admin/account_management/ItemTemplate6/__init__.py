from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate6(ItemTemplate6Template):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user

    # Set data bindings for label_3
    self.label_3.text = self.get_status_text()
    self.label_3.foreground = self.get_status_color()
    self.check_profile_pic()
  
  def check_profile_pic(self):
        # print(self.user)
        # print(self.user['users_email'],type(self.user['users_email']))
        # user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
        if self.item['users_profile_pic'] is not None:
            self.image_1.source =self.item['users_profile_pic']
        else:
          print('none')
  
  def get_status_text(self):
    # Return "Inactive" if self.item['inactive'] is True, otherwise "Active"
    return "Inactive" if self.item['users_inactive'] else "Active"
  
  def get_status_color(self):
    # Return "red" if self.item['inactive'] is True, otherwise "green"
    return "red" if self.item['users_inactive'] else "green"

  def button_1_click(self, **event_args):
    # Access the data for the selected user
    selected_user = self.item  # Assuming you have set the 'item' property of the repeating panel to the user row
    
    # Extract the phone number from the second text box
    phone_number = selected_user['users_phone']  # Assuming 'phone_number' is the key for the phone number in your data
    
    # Open the admin_view form and pass the phone number
    open_form('admin.admin_view',user =self.user, phone_number=phone_number)
