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
    open_form('admin.admin_view', phone_number=phone_number)
