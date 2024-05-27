from ._anvil_designer import ItemTemplate19Template
from anvil import *
import anvil.server


class ItemTemplate19(ItemTemplate19Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
