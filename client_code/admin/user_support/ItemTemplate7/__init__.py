from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.label_1.text = self.item['users_service_username']
    self.label_2.text = self.item['users_service_phone']
    self.label_3.text = self.item['users_service_email']
    self.text_area_1.text = self.item['users_service_query']
    


