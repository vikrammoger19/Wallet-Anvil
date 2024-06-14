from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # self.label_1.text = self.item['users_service_username']
    # self.label_2.text = self.item['users_service_phone']
    # self.label_3.text = self.item['users_service_email']
    # self.text_area_1.text = self.item['users_service_query']
    

    # Any code you write here will run before the form opens.

  def text_area_1_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass
