from ._anvil_designer import add_currencyTemplate
from anvil import *
import anvil.server

class add_currency(add_currencyTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
