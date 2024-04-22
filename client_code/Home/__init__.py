from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def link_16_click(self, **event_args):
    pass

  def button_3_click(self, **event_args):
    open_form('login')

  def button_1_click(self, **event_args):
    open_form('login')
