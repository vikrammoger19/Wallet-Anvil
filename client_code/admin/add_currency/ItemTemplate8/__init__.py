from ._anvil_designer import ItemTemplate8Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate8(ItemTemplate8Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.user_count_displayed = False

  def view_user_click(self, **event_args):
        if not self.user_count_displayed:
            selected_currency = self.item
            currency_code = selected_currency['currency_code']

            # Assuming 'currency_type' is the column name in 'wallet_currency' datatable
            currency_type_matches = app_tables.wallet_users_balance.search(currency_type=currency_code)

            # Count the number of occurrences of the currency type
            count_of_users = len(currency_type_matches)

            # Update the button text with the count of users
            self.view_user.text = f"{count_of_users} Users"
            self.user_count_displayed = True
        else:
            # Reset button text to default 'view user'
            self.view_user.text = "view number of user"
            self.user_count_displayed = False
