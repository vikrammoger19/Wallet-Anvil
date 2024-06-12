from ._anvil_designer import settingsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class settings(settingsTemplate):
  def __init__(self,user = None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    # Any code you write here will run before the form opens.

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.default_currency',user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.default_currency')

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('help',user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_8_click(self, **event_args):
    open_form('Reset_password', user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.deposit",user=self.user)

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transfer",user=self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.withdraw",user=self.user)

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.service",user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")
  
