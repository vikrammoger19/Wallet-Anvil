from ._anvil_designer import Device_CompatibilityTemplate
from anvil import *
import anvil.server


class Device_Compatibility(Device_CompatibilityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
