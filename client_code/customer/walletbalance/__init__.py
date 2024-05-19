from ._anvil_designer import walletbalanceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class walletbalance(walletbalanceTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user

        username = anvil.server.call('get_username', self.user['phone'])
        self.label_6.text = f"Welcome to Green Gate Financial, {username}"

        # Populate balances for the current user
        self.populate_balances()

    def populate_balances(self):
        try:
            # Retrieve balances for the current user
            user_phone = self.user['phone']
            user_balances = app_tables.wallet_users_balance.search(phone=user_phone)

            # Print the retrieved data
            print("Retrieved balances:", user_balances)

            # List to hold items for the repeating panel
            items = []

            for balance in user_balances:
                currency_type = balance['currency_type']
                balance_amount = balance['balance']

                # Lookup the currency icon in the wallet_currency table
                currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
                currency_icon = currency_record['currency_icon'] if currency_record else None

                # Create a dictionary for each item
                item = {
                    'currency_type': currency_type,
                    'balance': balance_amount,
                    'currency_icon': currency_icon  # Use 'currency_icon' as the key
                }

                items.append(item)

            # Set the items property of the RepeatingPanel
            self.repeating_panel_1.items = items
            print("Items set for repeating panel:", self.repeating_panel_1.items)

        except Exception as e:
            # Print any exception that occurs during the process
            print("Error occurred during population of balances:", e)

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('customer.deposit', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer.deposit', user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer.transfer', user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer.withdraw', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer.service', user=self.user)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer', user=self.user)

    def link_13_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('Home')
