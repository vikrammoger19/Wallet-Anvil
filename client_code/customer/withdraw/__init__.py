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
    self.label_1.text = f"Welcome to Green Gate Financial, {username}"
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
    cur= self.drop_down_2.selected_value
    if self.user :
      entered_amount = ''.join(filter(str.isdigit, str(self.text_box_2.text)))
      money_value = float(entered_amount) if entered_amount else 0.0
     # Check if a balance row already exists for the user
      existing_balance = app_tables.wallet_users_balance.get(users_balance_phone=self.user['users_phone'],users_balance_currency_type=cur) 
      if existing_balance['users_balance'] >=money_value:
        existing_balance['users_balance'] -= money_value
        new_transaction = app_tables.wallet_users_transaction.add_row(
                users_transaction_phone=self.user['users_phone'],
                users_transaction_fund=money_value,
                users_transaction_currency=cur,
                users_transaction_date=current_datetime,
                users_transaction_type="Withdrawn",
                users_transaction_status="Wallet-Withdrawn",
                users_transaction_receiver_phone=self.user['users_phone']
            )
        self.label_2.text = "Money Withdrawn successfully to the account."
        
      else:
        anvil.alert("Insufficient balance. Please add funds.")
        print("fund illa")
    else:
      self.label_2.text = "Error: No matching accounts found for the user or invalid account number."
      print("enaitho gottilla")
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
    open_form("customer_page",user=self.user)

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
