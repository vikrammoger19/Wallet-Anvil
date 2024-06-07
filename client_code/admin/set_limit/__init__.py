from ._anvil_designer import set_limitTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class set_limit(set_limitTemplate):
  def __init__(self, user= None, user_data=None, **properties):
        # Initialize the base class
        self.init_components(**properties)
        self.user= user
        # Access the user_data passed from the calling form
        self.user_data = user_data
        if self.user is not None:
            print("DEBUG: Before accessing 'email'")
            self.name = self.user['users_email']
            print(self.name)
            print("DEBUG: After accessing 'email'")
        self.check_profile_pic()
    # Any code you write here will run before the form opens.

  def check_profile_pic(self):
        print(self.user)
        print(self.user['users_email'],type(self.user['users_email']))
        user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
        if user_data:
          existing_img = user_data['users_profile_pic']
          if existing_img != None:
            self.image_2.source = existing_img
          else: 
            print('no pic')
        else:
          print('none')
        
        # Now you can access the username or any other user data
            
  def outlined_button_1_click(self, **event_args):
    username = self.user_data['users_username']
    new_limit = self.text_box_1.text
        
    # Call the server function and update the user's limit
    setter = anvil.server.call('user_detail', username, new_limit)
        
    # Log changes to 'actions' table
    changes_made = [f"Limit updated to {new_limit} by admin"]
    if self.user is not None:
            self.log_action(username, changes_made, self.name)
    else:
      print("it's none - not logging action")
    

  def log_action(self, username, changes,email):
        # Retrieve last_login from the 'users' table
        user = app_tables.wallet_users.get(users_username=username)
        last_login = None
        
        if user and user['last_login']:
            last_login = user['users_last_login']
        # Log actions to 'actions' table if changes were made
        if changes:
            print("reached changes")
            current_datetime = datetime.now()
            app_tables.actions.add_row(
                username=username,
                last_login=last_login,
                changes=", ".join(changes),
                date=current_datetime,
                admin_email= email
            )

  def link_8_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def link_10_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.user_support',user=self.user)

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_3_click(self, **event_args):
    open_form('admin.account_management',user=self.user)

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
    serves_data = app_tables.sevices.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data,user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    show_users_form = open_form('admin.show_users',user=self.user)

  def drop_down_2_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    options_list = ['Daily', 'Monthly', 'Annually']
    self.drop_down_2.items = []
    self.drop_down_2.items = options_list

  def primary_color_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
    
    
