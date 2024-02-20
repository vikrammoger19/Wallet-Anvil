from ._anvil_designer import transaction_monitoringTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class transaction_monitoring(transaction_monitoringTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    transactions = anvil.server.call('get_wallet_transactions')
        # Assuming you have a repeating panel named repeating_panel_1
    self.repeating_panel_1.items = transactions

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.report_analysis')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.account_management')

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.transaction_monitoring')

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.admin_add_user')

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin.audit_trail')

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    serves_data = app_tables.wallet_users_service.search()

    # Open the admin.user_support form and pass the serves_data
    user_support_form = open_form('admin.user_support', serves_data=serves_data)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    show_users_form = open_form('admin.show_users')

  def link_8_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('admin')

  def button_8_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Login')

  def button_1_click(self, **event_args):
    # Get the user entered in the textbox
    entered_user = self.textbox_search.text

    # Convert entered_user to a number if it's a valid numerical value
    try:
        entered_user = int(entered_user)  # Assuming phone numbers are integers
    except ValueError:
        # Handle the case where entered_user is not a valid numerical value
        # You might want to display an error message or handle this case differently
        print("Entered user is not a valid numerical value.")
        return

    # Filter transactions based on the entered user
    filtered_transactions = app_tables.wallet_users_transaction.search(receiver_phone=entered_user)

    # Update the repeating panel with the filtered transactions
    self.repeating_panel_1.items = filtered_transactions
