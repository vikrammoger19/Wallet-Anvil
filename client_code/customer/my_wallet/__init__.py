from ._anvil_designer import my_walletTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class my_wallet(my_walletTemplate):
  def __init__(self,user = None, **properties):
    # Set Form properties and Data Bindings.
    self.user = user
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.
    currency_data = app_tables.wallet_users_balance.search(phone=self.user['phone'])
    details = [items for items in currency_data]
    self.label_1.text = self.user['username']
    print(self.user['username'])
    self.repeating_panel_1.items = details

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.deposit",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transfer",user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.withdraw",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.service",user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer',user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")
    # Any code you write here will run before the form opens.
