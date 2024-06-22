from ._anvil_designer import set_limitTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class set_limit(set_limitTemplate):
    
    def __init__(self, user=None, user_data=None, **properties):
        # Initialize the base class
        self.init_components(**properties)
        self.user = user
        self.user_data = user_data
        
        # Debugging statements
        if self.user is not None:
            print("DEBUG: User is present")
            self.name = self.user['users_email']
            print(f"DEBUG: User's email: {self.name}")
        else:
            print("DEBUG: User is None")
        
        if self.user_data is not None:
            print(f"DEBUG: User data received: {self.user_data['users_username']}")
        else:
            print("DEBUG: User data is None")
    
    def primary_color_1_click(self, **event_args):
        username = self.user_data['users_username']
        new_limit = float(self.text_box_1.text)
        limit_type = self.drop_down_2.selected_value

        # Determine which limit to update based on the selection
        if limit_type == 'Daily':
            field_to_update = 'users_daily_limit'
        elif limit_type == 'Monthly':
            field_to_update = 'users_user_limit'
        else:
            anvil.alert("Invalid limit type selected")
            return

        # Call the server function to update the user's limit
        setter = anvil.server.call('update_user_limit', username, field_to_update, new_limit)
        
        # Log changes to 'actions' table
        changes_made = [f"{field_to_update} updated to {new_limit} by admin"]
        if self.user is not None:
            self.log_action(username, changes_made, self.name)
        else:
            print("DEBUG: self.user is None - not logging action")
    
    def log_action(self, username, changes, email):
        # Retrieve last_login from the 'users' table
        user = app_tables.wallet_users.get(users_username=username)
        last_login = None
        
        if user and user['users_last_login']:
            last_login = user['users_last_login']
        
        # Log actions to 'actions' table if changes were made
        if changes:
            print("DEBUG: Changes to be logged")
            current_datetime = datetime.now()
            app_tables.wallet_admins_actions.add_row(
                admins_actions_name=self.user['users_username'],
                admins_actions_username=username,
                # last_login=last_login,
                admins_actions=", ".join(changes),
                admins_actions_date=current_datetime,
                # admin_email= email
            )

    def link_5_click(self, **event_args):
          """This method is called when the link is clicked"""
          openform('admin.acco', user=self.user)
      
      
    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)
  
    def link_10_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.user_support', user=self.user)
  
    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')
  
    def button_3_click(self, **event_args):
        open_form('admin.account_management', user=self.user)
  
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
        serves_data = app_tables.services.search()
        user_support_form = open_form('admin.user_support', serves_data=serves_data, user=self.user)
  
    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        show_users_form = open_form('admin.show_users', user=self.user)
  
    def drop_down_2_show(self, **event_args):
        """This method is called when the DropDown is shown on the screen"""
        options_list = ['Daily', 'Monthly']
        self.drop_down_2.items = options_list

    def primary_color_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('admin.account_management',user=self.user)
