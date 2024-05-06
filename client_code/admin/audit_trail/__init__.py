from ._anvil_designer import audit_trailTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class audit_trail(audit_trailTemplate):
  def __init__(self,user=None, **properties):
    # Set Form properties and Data Bindings.
    self.user=user
    self.init_components(**properties)
    actions_data = app_tables.actions.search()
        # Set the fetched data as the items for the repeating panel
    self.repeating_panel_1.items = actions_data
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis',user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management', user= self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.admin_add_user',user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail', user = self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    serves_data = app_tables.actions.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data,user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    show_users_form = open_form('admin.show_users',user=self.user)

  def link_8_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')
