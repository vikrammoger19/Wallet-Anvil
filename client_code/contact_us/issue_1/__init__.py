from ._anvil_designer import issue_1Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class issue_1(issue_1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    #self.card_1.visible = False
    # self.card_3.visible = False
    # self.card_5.visible = False
  
  # def link_8_click(self, **event_args):
  #   #self.card_1.visible = not self.card_1.visible
  #   self.card_3.visible = False
  #   self.card_5.visible = False

  # def link_13_click(self, **event_args):
  #   self.card_3.visible = not self.card_3.visible
  #   #self.card_1.visible = False
  #   self.card_5.visible = False

  # def link_15_click(self, **event_args):
  #   self.card_5.visible = not self.card_5.visible
  #   self.card_1.visible = False
  #   self.card_3.visible = False

  # def link_16_click(self, **event_args):
  #   self.card_5.visible = False
  #   #self.card_1.visible = False
  #   self.card_3.visible = False

  def link_1_click(self, **event_args):
    open_form('contact_us')

  def link_2_click(self, **event_args):
    open_form('contact_us.issue_1.login_issue')
        
  def link_3_click(self, **event_args):
    open_form('contact_us.issue_1.report_issue')