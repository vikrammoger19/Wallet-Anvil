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
    open_form('pay')

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
