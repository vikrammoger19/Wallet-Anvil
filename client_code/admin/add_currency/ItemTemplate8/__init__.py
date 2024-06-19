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
      currency_code = selected_currency['admins_add_currency_code']
      currency_type_matches = app_tables.wallet_users_balance.search(users_balance_currency_type=currency_code)
      count_of_users = len(currency_type_matches)
      self.view_user.text = f"{count_of_users} Users"
      self.user_count_displayed = True
    else:
      self.view_user.text = "view number of user"
      self.user_count_displayed = False

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass
