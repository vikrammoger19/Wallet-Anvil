from ._anvil_designer import helpTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class help(helpTemplate):
  def __init__(self,user=None,**properties):
        self.init_components(**properties)
        self.user = user

  def button_1_click(self, **event_args):
      query = self.text_area_1.text
      # Fetch user information from the "users" table
      user_info = app_tables.wallet_users.get(users_phone=self.user['users_phone'])

      if user_info is not None:
          # Update the "Services" table with the query and user information
          app_tables.wallet_users_service.add_row(
              users_service_username=user_info['users_username'],
              users_service_phone=user_info['users_phone'],
              users_service_query=query,
              users_service_email = user_info['users_email']
          )
          alert("Your query has been submitted, and our Technical Executive will get in touch with you")
      else:
          alert("User information not found.")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.deposit",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transfer",user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.withdraw",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer_page", user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")

  # def link_8_click(self, **event_args):
  #   """This method is called when the link is clicked"""
  #   open_form("customer.service",user=self.user)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.interaction',user=self.user)
  def link_1_copy_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.report_bug',user=self.user)

  def link_26_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('FAQ')

  
