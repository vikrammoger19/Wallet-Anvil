from ._anvil_designer import banned_formTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class banned_form(banned_formTemplate):
    def __init__(self, user=None, **properties):
        # Initialize the form
        self.init_components(**properties)
        self.user = user
        
        if user is not None:
              user1= user['users_username']
              self.label_1.text= f"Hi {user1}, your account has been banned because of suspicious activity."
       
