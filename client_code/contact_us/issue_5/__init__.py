from ._anvil_designer import issue_5Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server


class issue_5(issue_5Template):
  def _init_(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    open_form("contact_us")

  def button_3_click(self, **event_args):
    open_form("Login")

  def link_8_click(self, **event_args):
    open_form("Home")

  def link_16_click(self, **event_args):
    open_form("contact_us")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("contact_us.issue_4.Failed_Transaction")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("contact_us.issue_4.Misssing_Transaction")