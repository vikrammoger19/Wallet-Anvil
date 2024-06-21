from ._anvil_designer import Failed_TransactionTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Failed_Transaction(Failed_TransactionTemplate):
  def _init_(self, **properties):
    self.init_components(**properties)
    # self.card_1.visible = False
    # self.card_3.visible = False
    # self.card_5.visible = False

  # def link_8_click(self, **event_args):
  #   self.card_1.visible = not self.card_1.visible
  #   # self.card_3.visible = False
  #   # self.card_5.visible = False

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
    open_form("contact_us")

  def link_2_click(self, **event_args):
     open_form("MessageUs")

  def button_3_click(self, **event_args):
    open_form("Login")

  def link_3_click(self, **event_args):
    open_form("login")

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("signup")

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transactions")