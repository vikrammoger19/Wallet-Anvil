from ._anvil_designer import depositTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class deposit(depositTemplate):

    def __init__(self, phone=None, **properties):
        # Initialize self.user as a dictionary
        self.user = {'phone': phone} if phone else {}
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Assuming you have a 'get_username' function in your server module
        username = anvil.server.call('get_username', self.user['phone'])
        self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        user_account_numbers = anvil.server.call('get_user_account_numbers', self.user['phone'])
        self.drop_down_1.items = list(map(str, user_account_numbers)) if user_account_numbers is not None else []
        self.display()

    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        acc = self.drop_down_1.selected_value

        if self.user and 'phone' in self.user:
            entered_amount = ''.join(filter(str.isdigit, str(self.text_box_2.text)))
            money_value = float(entered_amount) if entered_amount else 0.0

            # Check if a balance row already exists for the user
            existing_balance = app_tables.wallet_users_balance.get(phone=self.user['phone'])

            if existing_balance:
                # Update the existing balance
                existing_balance['e_money'] += money_value
            else:
                # Add a new row for the user if no existing balance
                balance = app_tables.wallet_users_balance.add_row(
                    currency_type="INR",  # Replace with the actual currency type
                    e_money=money_value,
                    phone=self.user['phone']
                )

            # Add a new transaction row
            new_transaction = app_tables.wallet_users_transaction.add_row(
                phone=self.user['phone'],
                fund=money_value,
                date=current_datetime,
                transaction_type="Debit",
                transaction_status="Wallet-Topup",
                receiver_phone=None
            )

            self.label_2.text = "Money added successfully to the account."
        else:
            self.label_2.text = "Error: No matching accounts found for the user or invalid account number."

    def drop_down_1_change(self, **event_args):
        self.display()

    def display(self, **event_args):
        acc = self.drop_down_1.selected_value

    def display(self, **event_args):
          acc=self.drop_down_1.selected_value
        
    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("transfer",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("withdraw",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("service",user=self.user)
    def label_7_copy_2_copy(self, **event_args):
      open_form("customer",user=self.user)
