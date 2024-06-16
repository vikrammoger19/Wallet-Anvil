from ._anvil_designer import transferTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transfer(transferTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['users_phone'])
        #self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        currencies=anvil.server.call('get_user_currency',self.user['users_phone'])
        self.drop_down_2.items= [str(row['users_balance_currency_type']) for row in currencies]
        self.display()
     

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value

    def button_1_click(self, **event_args):
      current_datetime = datetime.now()
      receiver_phone_number = float(self.text_box_2.text)
      transfer_amount = float(self.text_box_3.text)
      cur = self.drop_down_2.selected_value
      depositor_phone_number = self.user['users_phone']
      
      
      
      # Use the entered phone number to identify the receiver's account
      receiver_balance = app_tables.wallet_users_balance.get(users_balance_phone=receiver_phone_number, users_balance_currency_type=cur)
      depositor_balance = app_tables.wallet_users_balance.get(users_balance_phone=depositor_phone_number, users_balance_currency_type=cur)
      
      if depositor_balance:
          depositor = app_tables.wallet_users.get(users_phone=depositor_phone_number)
          
          users_daily_limit = depositor['users_daily_limit']
          users_user_limit = depositor['users_user_limit']
          
          if transfer_amount > users_daily_limit:
              anvil.alert("Daily limit exceeded.")
          elif transfer_amount > users_user_limit:
              anvil.alert("Monthly limit exceeded.")
          else:
              money_value = transfer_amount if transfer_amount else 0.0
              if depositor_balance['users_balance'] >= money_value:
                  if receiver_balance:
                      depositor_balance['users_balance'] -= money_value
                      receiver_balance['users_balance'] += money_value
                  else:
                      receiver = app_tables.wallet_users.get(users_phone=receiver_phone_number)
                      if receiver:
                          depositor_balance['users_balance'] -= money_value
                          app_tables.wallet_users_balance.add_row(
                              users_balance_currency_type=cur,
                              users_balance=money_value,
                              users_balance_phone=receiver_phone_number
                          )
                      else:
                          anvil.alert("User does not exist")
                          return
                  
                  new_transaction = app_tables.wallet_users_transaction.add_row(
                      users_transaction_phone=depositor_phone_number,
                      users_transaction_fund=money_value,
                      users_transaction_currency=cur,
                      users_transaction_date=current_datetime,
                      users_transaction_type="Debit",
                      users_transaction_status="transferred-to",
                      users_transaction_receiver_phone=receiver_phone_number
                  )
                  new_transaction = app_tables.wallet_users_transaction.add_row(
                      users_transaction_phone=receiver_phone_number,
                      users_transaction_fund=money_value,
                      users_transaction_currency=cur,
                      users_transaction_date=current_datetime,
                      users_transaction_type="Credit",
                      users_transaction_status="received-from",
                      users_transaction_receiver_phone=depositor_phone_number
                  )
  
                  # Update the limits after successful transaction
                  depositor['users_daily_limit'] -= money_value
                  depositor['users_user_limit'] -= money_value
  
                  self.label_4.text = "Money transferred successfully to the account."
              else:
                  anvil.alert("Insufficient balance. Please add funds.")
      else:
          self.label_4.text = "Error: No matching accounts found for the user or invalid account number."
  
      open_form('customer.transfer', user=self.user)
          
    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

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
      open_form("customer.service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

  





