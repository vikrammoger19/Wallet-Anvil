from ._anvil_designer import ItemTemplate14Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate14(ItemTemplate14Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if self.item:
        self.text_area_1.text = self.item.get('users_service_query', '')
        self.text_area_2.text = self.item.get('users_conclusion_about_query', '')
        
        # Conditional formatting for users_update
        if self.item.get('users_update', False):
            self.label_1.text = "Solved"
            self.label_1.foreground = "green"
        else:
            self.label_1.text = "Pending"
            self.label_1.foreground = "red"

  