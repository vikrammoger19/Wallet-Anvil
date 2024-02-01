from ._anvil_designer import withdrawTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class withdraw(withdrawTemplate):
  def __init__(self, user=None, **properties):
    # Initialize self.user as a dictionary
    self.init_components(**properties)
    self.user = user
    # Set Form properties and Data Bindings.
    username = anvil.server.call('get_username', self.user['phone'])
    self.label_1.text = f"Welcome to Green Gate Financial, {username}"
    user_account_numbers = anvil.server.call('get_user_account_numbers', self.user['phone'])
    self.drop_down_1.items = list(map(str, user_account_numbers)) if user_account_numbers is not None else []
    self.display()
    # Any code you write here will run before the form opens.
