from ._anvil_designer import helpTemplate
from anvil import *
import anvil.server


class help(helpTemplate):
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

  def products_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('product')

  def contact_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('contact_us')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('login')
