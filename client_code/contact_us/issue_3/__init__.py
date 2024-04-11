from ._anvil_designer import issue_3Template
from anvil import *
import anvil.server

class issue_3(issue_3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
