from ._anvil_designer import raise_a_complaintTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class raise_a_complaint(raise_a_complaintTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    #email = anvil.server.call('email')

    
    self.text_box_1.text = {user['email']}
    
