from ._anvil_designer import audit_trailTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class audit_trail(audit_trailTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.user = user
    self.init_components(**properties)
    self.load_all_actions()
    # Any code you write here will run before the form opens.
    self.check_profile_pic()
  
  def check_profile_pic(self):
        print(self.user)
        print(self.user['users_email'],type(self.user['users_email']))
        user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
        if user_data:
          existing_img = user_data['users_profile_pic']
          if existing_img != None:
            self.image_3_copy.source = existing_img
          else: 
            print('no pic')
        else:
          print('none')
  
  def load_all_actions(self):
    """Load all actions into the repeating panel."""
    actions_data = app_tables.wallet_admins_actions.search()
    self.repeating_panel_2.items = actions_data

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis', user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management', user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring', user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.admin_add_user', user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail', user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    serves_data = app_tables.actions.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data, user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    show_users_form = open_form('admin.show_users', user=self.user)

  def link_8_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin', user=self.user)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Home')

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    username = self.text_box_1.text.strip()
    if username:
      # Perform the search for users based on the entered username
      search_results = app_tables.wallet_admins_actions.search(admins_actions_username=username)
      self.repeating_panel_2.items = search_results
    
      
    else:
      # If the search box is empty, load all actions
      self.load_all_actions()

