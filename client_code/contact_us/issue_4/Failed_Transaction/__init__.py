from ._anvil_designer import Failed_TransactionTemplate
from anvil import *
import anvil.server


class Failed_Transaction(Failed_TransactionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
