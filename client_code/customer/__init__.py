from ._anvil_designer import customerTemplate
from anvil import open_form
import datetime

class customer(customerTemplate):
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user  # Set the user attribute
        now = datetime.now()
        if now != self.user['last_login']:
            if self.user['daily_limit'] is None:
                self.user['user_limit'] = 100000
            else:
                self.user['user_limit'] = self.user['daily_limit']
            self.user['last_login'] = now
            self.user.update()

        if user:
            # Use the information from the logged-in user
            self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"

    def button_1_click(self, **event_args):
        # Open the Viewprofile form and pass the user information
        open_form('Viewprofile', user=self.user)

    def button_2_click(self, **event_args):
      open_form('wallet', user=self.user)
