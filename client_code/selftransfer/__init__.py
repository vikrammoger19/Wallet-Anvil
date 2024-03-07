from ._anvil_designer import selftransferTemplate
from anvil import *
import anvil.server

class selftransfer(selftransferTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
