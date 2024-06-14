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
    self.user=user
    self.label_1.text = self.item['receiver_username']

    # Any code you write here will run before the form opens.
