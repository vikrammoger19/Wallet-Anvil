from ._anvil_designer import report_issueTemplate
from anvil import *
import anvil.users
import anvil.server
from ..login_issue import login_issueTemplate
from ... import contact_us

class report_issue(report_issueTemplate):
  def _init_(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
# from ._anvil_designer import report_issueTemplate
# from anvil import *
# import anvil.server
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

  def link_1_click(self, **event_args):
    open_form('contact_us')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("help")

  def link_2_click(self, **event_args):
     open_form("MessageUs")

class login_issue(login_issueTemplate):
  def _init_(self, **properties):
    self.init_components(**properties)
  #   self.card_1.visible = False
  #   self.card_3.visible = False
  #   self.card_5.visible = False
    

  # def link_8_click(self, **event_args):
  #   self.card_1.visible = not self.card_1.visible
  #   self.card_3.visible = False
  #   self.card_5.visible = False

  # def link_13_click(self, **event_args):
  #   self.card_3.visible = not self.card_3.visible
  #   self.card_1.visible = False
  #   self.card_5.visible = False

  # def link_15_click(self, **event_args):
  #   self.card_5.visible = not self.card_5.visible
  #   self.card_1.visible = False
  #   self.card_3.visible = False

  # def link_16_click(self, **event_args):
  #   self.card_5.visible = False
  #   self.card_1.visible = False
  #   self.card_3.visible = False

  def link_1_click(self, **event_args):
    open_form('contact_us.issues_1')

  def link_2_click(self, **event_args):
    if self.user is None:
      alert("Please Login to send us a message.")
    else:
      open_form("customer.service")

  def button_3_click(self, **event_args):
    open_form('Login')