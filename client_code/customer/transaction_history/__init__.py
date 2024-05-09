from ._anvil_designer import transaction_historyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transaction_history(transaction_historyTemplate):
    def __init__(self, user=None, **properties):
        # Initialize self.user as a dictionary 
        self.user = user
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Convert LiveObjectProxy to dictionary
        user_dict = dict(self.user)

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)

        if phone_number:
            # Get the username using the 'get_username' server function
            username = anvil.server.call('get_username', phone_number)
            self.label_1.text = f"Welcome to Green Gate Financial, {username}"

            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(phone=phone_number)

            # Group transactions by date
            grouped_transactions = {}
            for item in items:
                date_str = item['date'].strftime("%Y-%m-%d")  # Extract date in YYYY-MM-DD format
                if date_str not in grouped_transactions:
                    grouped_transactions[date_str] = {'date': date_str, 'transactions': []}
                grouped_transactions[date_str]['transactions'].append({'fund': item['fund'], 'receiver_phone': item['receiver_phone']})

            # Create a list of dictionaries for repeating_panel_1
            repeating_panel_1_items = []
            for date_info in grouped_transactions.values():
                repeating_panel_1_items.append({'date': date_info['date']})
                for transaction in date_info['transactions']:
                    repeating_panel_1_items.append({'fund': transaction['fund'], 'receiver_phone': transaction['receiver_phone']})

            self.repeating_panel_1.items = repeating_panel_1_items

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
    
    def link_13_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("Home")
    
    def link_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.service",user=self.user)
    
    def button_3_click(self, **event_args):
        open_form('customer', user=self.user)

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('customer',user=self.user)

    def link_24_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('about_us')

    def link_25_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('product')

    def primary_color_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
