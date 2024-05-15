from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    anvil.server.call('update_active_status')
  def link_16_click(self, **event_args):
    pass

  def button_3_click(self, **event_args):
    open_form('signup')

  def button_1_click(self, **event_args):
    open_form('signup')

  def button_2_click(self, **event_args):
    open_form('signup')

  def home_click(self, **event_args):
    open_form('Home')

  def about_us_click(self, **event_args):
    open_form('about_us')

  def products_click(self, **event_args):
    open_form('product')

  def contact_click(self, **event_args):
    open_form('contact_us')

  def help_click(self, **event_args):
    open_form('help')

  def button_4_click(self, **event_args):
    open_form('login')

  