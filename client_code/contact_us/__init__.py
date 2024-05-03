from ._anvil_designer import contact_usTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class contact_us(contact_usTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
  def link_8_click(self, **event_args):
    open_form('Home')

  def link_1_click(self, **event_args):
    open_form('contact_us.issue_1')

  def link_3_click(self, **event_args):
    open_form('contact_us.issue_2')

  def link_4_click(self, **event_args):
    open_form('contact_us.issue_3')

  def link_5_click(self, **event_args):
    open_form('contact_us.issue_4')

  def home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def about_us_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('about_us')

  def products_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('product')

  def help_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('help')

