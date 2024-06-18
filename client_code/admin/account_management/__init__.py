from ._anvil_designer import account_managementTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .ItemTemplate6 import ItemTemplate6

class account_management(account_managementTemplate):
  def __init__(self, user= None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.button_100000.visible = False
    self.user =user
    one = self.user['users_username'] 
    print('hi admin1')
    print(one)
    if user is not None:
       self.label_656.text = user['users_username']
    
    #print(mail)
    self.refresh_users()
    ItemTemplate6.user=self.user
    # self.check_profile_pic()
  
  # def check_profile_pic(self):
  #       # print(self.user['users_email'],type(self.user['users_email']))
  #       user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
  #       if user_data:
  #         existing_img = user_data['users_profile_pic']
  #         if existing_img != None:
  #           self.image_3.source = existing_img
  #         else: 
  #           print('no pic')
  #       else:
  #         print('none')

  def refresh_users(self, username_filter=None, status_filter=None):
    # Fetch all users from the table
    users = app_tables.wallet_users.search()

    # Filter users based on customer type
    users = [user for user in users if user['users_usertype'] == 'customer']

    # Filter users based on status if status filter is provided
    if status_filter == "Active":
      users = [user for user in users if user['users_inactive'] is None]
    elif status_filter == "Inactive":
      users = [user for user in users if user['users_inactive'] is True]

    # Filter users based on username if username filter is provided
    if username_filter:
      users = [user for user in users if user['users_username'].lower().startswith(username_filter.lower())]

    # Set items in the repeating panel
    self.repeating_panel_1.items = users
    print(users)
    self.label_5.text = f"Total users: {len(users)}"




  # def button_1_click(self, **event_args):
  #       # Toggle visibility of the repeating panel
  #       self.repeating_panel_1.visible = not self.repeating_panel_1.visible

  def button_2_click(self, **event_args):
        # Handle search button click event to refresh users based on entered username
        username_filter = self.text_box_1.text
        self.refresh_users(username_filter)
# Any code you write here will run before the form opens.

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
    open_form('admin.admin_add_user',user= self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin',user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management', user= self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail',user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.add_currency',user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    serves_data = app_tables.wallet_users_service.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    show_users_form = open_form('admin.show_users',user=self.user)

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    # Get the selected status filter
    status_filter = self.drop_down_1.selected_value

    # Refresh users based on the selected status filter
    self.refresh_users(status_filter=status_filter)


 