from ._anvil_designer import MessageUsTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables




class MessageUs(MessageUsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("login")
    # self.number=int(self.phone_number.text)
    # user_info = app_tables.wallet_users.get(users_phone=self.number)

    # if user_info is not None:
    #     # Update the "Services" table with the query and user information
    #     app_tables.wallet_users_service.add_row(
    #         users_service_username=user_info['users_username'],
    #         users_service_phone=user_info['users_phone'],
    #         users_service_query=self.user_query.text
    #     )
    #     alert("Your query has been submitted, and our Technical Executive will get in touch with you")
    # else:
    #     alert("User information not found.")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    # self.main_column_panel.clear()
    open_form("contact_us")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.column_panel_2.visible=False
    self.column_panel_1.visible=True

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.column_panel_1.visible=False
    self.column_panel_2.visible=True

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.users_phone_number=int(self.users_phones_number.text)
    # user_info = app_tables.wallet_users.get(users_phone=self.number)
    self.users_name=self.users_names.text
    self.users_email=self.users_emails.text
    
        # Update the "Services" table with the query and user information
    app_tables.wallet_users_service.add_row(
        users_service_username=self.users_name,
        users_service_phone=self.users_phone_number,
        users_service_email=self.users_email,
        users_service_query=self.users_queries.text
        )
    alert("Your query has been submitted, and our Technical Executive will get in touch with you")