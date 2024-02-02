# from ._anvil_designer import adminTemplate
# from anvil import *
# import anvil.server
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class admin(adminTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     # Any code you write here will run before the form opens.

from ._anvil_designer import adminTemplate
from anvil import *
#import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class admin(adminTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    if user is not None:
            self.label_5.text = f"Welcome to Green Gate Financial, {user['username']}"
    else:
        self.label_5.text = "Welcome to Green Gate Financial (User data not available)"
    

  
  def link_1_click(self, **event_args):
    open_form('Home')

  def button_1_click(self, **event_args):
        # Open the show_users form and pass the user data
        show_users_form = open_form('admin.show_users')

  def button_5_click(self, **event_args):
    open_form('admin.account_management', user= self.user)

  def link_8_click(self, **event_args):
   open_form('admin')

  def button_2_click(self, **event_args):
    open_form('admin.transaction_monitoring')

  


  def button_7_click(self, **event_args):
    open_form('admin.audit_trail', user = self.user)

  def button_3_click(self, **event_args):
    open_form('admin.report_analysis')
   

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    serves_data = app_tables.sevices.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_6_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('admin.admin_add_user')
