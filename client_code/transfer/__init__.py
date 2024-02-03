from ._anvil_designer import transferTemplate
from anvil import *
#import anvil.users
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
        username = anvil.server.call('get_username', self.user['phone'])
        self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        currencies=anvil.server.call('get_user_currency',self.user['phone'])
        self.drop_down_2.items= [str(row['currency_type']) for row in currencies]
        self.display()
        # Any code you write here will run before the form opens.

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value

    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        receiver_phone_number = self.text_box_2.text
        transfer_amount = self.text_box_3.text
        cur=self.drop_down_2.selected_value
        
        # Use the phone number of the depositor to identify their account
        depositor_phone_number = self.user['phone']
        depositor_balance = anvil.server.call('get_balance_using_phone_number', depositor_phone_number, self.drop_down_2.selected_value)

        # Use the entered phone number to identify the receiver's account
        receiver_balance = anvil.server.call('get_balance_using_phone_number', receiver_phone_number, self.drop_down_2.selected_value)

        # Check if 'balance' is not None and not an empty string
        if receiver_balance['balance'] is not None:
            recieve = float(receiver_balance['balance'])
        else:
            recieve = 0.0  # or set a default value based on your application logic

        if receiver_balance['balance'] is None:
            anvil.server.call('update_balance_trasaction', receiver_phone_number, str(0), cur)
        
        if (transfer_amount < 5) or (transfer_amount > 50000):
            self.label_4.text = "Transfer amount should be between 5 and 50000 for a transfer Funds." 
        else:
            # if float(depositor_balance['balance']) < transfer_amount:
            #     self.label_4.text = "Insufficient Funds in E-Wallet."
             
                # calculating the money to be added in the receiver's end
                transfer_final_receive_amount = recieve + transfer_amount
                # calculating the money to be deducted in the depositor's end
                transfer_depositor_amount_final = float(depositor_balance['balance']) - transfer_amount
                # setting the value
                anvil.server.call('update_balance_trasaction', depositor_phone_number, str(transfer_depositor_amount_final), cur)
                anvil.server.call('update_balance_trasaction', receiver_phone_number, str(transfer_final_receive_amount))
                # Updating the daily limit
                # answer = float(self.user['limit']) - transfer_amount
                # anvil.server.call('update_daily_limit', self.user['username'], str(answer))
                self.label_4.text = "Money transferred successfully"

                app_tables.wallet_users_transaction.add_row(
                  phone=depositor_phone_number,
                  fund=transfer_amount,
                  date=current_datetime,
                  transaction_type="Debit",
                  transaction_status="Transfer",
                  receiver_phone=int(receiver_phone_number)
                     
                )
          
    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("service",user=self.user)

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





