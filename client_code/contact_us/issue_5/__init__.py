from ._anvil_designer import issue_5Template
from anvil import *
import anvil.server


class issue_5(issue_5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
