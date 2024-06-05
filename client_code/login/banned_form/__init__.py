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
        
        # Retrieve the phone number directly from the user object
        phone_number = getattr(self.user, 'users_username', None)
        
        if phone_number:
            # Retrieve the user based on the phone number
            user_record = app_tables.wallet_users.get(users_phone=phone_number)
            
            # Set the username in the label if the user is found
            if user_record:
                self.label_1.text = user_record['users_username']
            else:
                self.label_1.text = "User not found"
        else:
            self.label_1.text = "No phone number provided"
