from ._anvil_designer import adminTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class admin(adminTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    if user is not None:
            self.label_2.text = user['username']
