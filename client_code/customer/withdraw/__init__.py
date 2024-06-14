from ._anvil_designer import withdrawTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class withdraw(withdrawTemplate):
  def __init__(self, user=None, **properties):
    # Initialize self.user as a dictionary
    self.init_components(**properties)
    self.user = user
    # Set Form properties and Data Bindings.
    username = anvil.server.call('get_username', self.user['users_phone'])
    #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
    bank_names = anvil.server.call('get_user_bank_name', self.user['users_phone'])
    
    currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
    self.drop_down_1.items = [str(row['users_account_bank_name']) for row in bank_names]
    self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
    self.display()
    # Any code you write here will run before the form opens.
  def drop_down_1_change(self, **event_args):
    self.display()

  def display(self, **event_args):
    acc = self.drop_down_1.selected_value

  def button_1_click(self, **event_args):
    current_datetime = datetime.now()
    acc = self.drop_down_1.selected_value
    cur = self.drop_down_2.selected_value
    money = float(self.text_box_2.text)
    endpoint = 'convert'
    api_key = 'a2qfoReWfa7G3GiDHxeI1f9BFXYkZ2wT'

    if acc is None or cur is None:
        alert('Please enter bank details')
    else:
        base_currency = 'INR'
        resp = anvil.http.request(f"https://api.currencybeacon.com/v1/{endpoint}?from={base_currency}&to={cur}&amount={money}&api_key={api_key}", json=True)
        money_value = resp['response']['value']
        
        if self.user:
            # Retrieve user data
            user_data = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
            if not user_data:
                self.label_2.text = "Error: No matching accounts found for the user."
                return
            
            users_daily_limit = user_data['users_daily_limit']
            users_user_limit = user_data['users_user_limit']

            # Check the limits
            if money_value > users_daily_limit:
                alert("Daily limit exceeded.", buttons=[("OK", True)], large=True)
                open_form('customer', user=self.user)
                return
            elif money_value > users_user_limit:
                alert("Monthly limit exceeded.", buttons=[("OK", True)], large=True)
                open_form('customer', user=self.user)
                return
            
            # Check if a balance row already exists for the user
            existing_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'], users_balance_currency_type=cur)

            if existing_balance:
                # Update the existing balance
                existing_balance['users_balance'] -= money_value
            else:
                # Add a new row for the user if no existing balance
                app_tables.wallet_users_balance.add_row(
                    users_balance_currency_type=cur,
                    users_balance=money_value,
                    users_balance_phone=self.user['users_phone']
                )

            # Add a new transaction row
            app_tables.wallet_users_transaction.add_row(
                users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_bank_name=acc,
                users_transaction_type="Withdrawn",
                users_transaction_status="Wallet-Withdraw",
                users_transaction_receiver_phone=self.user['users_phone']
            )

            # Update the limits
            user_data['users_daily_limit'] -= money_value
            user_data['users_user_limit'] -= money_value

            self.label_2.text = "Money added successfully to the account."
        else:
            self.label_2.text = "Error: No matching accounts found for the user or invalid account number."

  def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.deposit",user=self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.transfer",user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.service",user=self.user)

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer",user=self.user)

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.service",user=self.user)  # Any code you write here will run before the form opens.

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.withdraw',user=self.user)

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('customer.wallet',user=self.user)

  
