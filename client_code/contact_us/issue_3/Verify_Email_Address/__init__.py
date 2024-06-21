from ._anvil_designer import Verify_Email_AddressTemplate
from anvil import *
import anvil.server


class Verify_Email_Address(Verify_Email_AddressTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
