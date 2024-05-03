from ._anvil_designer import productTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class product(productTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def about_us_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('about_us')

  def contact_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('contact_us')

  def help_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('help')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
