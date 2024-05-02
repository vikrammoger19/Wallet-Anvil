from ._anvil_designer import ItemTemplate12Template
from anvil import *
import anvil.server


class ItemTemplate12(ItemTemplate12Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
