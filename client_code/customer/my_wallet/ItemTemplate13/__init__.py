from ._anvil_designer import ItemTemplate13Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate13(ItemTemplate13Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    if self.item['balance'] > 0:
      self.label_2.text = self.item['balance']
      self.label_2.icon = f"fa:{self.item['currency_type'].lower()}"

    # Any code you write here will run before the form opens.
