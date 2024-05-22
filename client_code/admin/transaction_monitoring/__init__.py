from ._anvil_designer import transaction_monitoringTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transaction_monitoring(transaction_monitoringTemplate):
    def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.user = user
        self.init_components(**properties)
        
        # Fetch all transactions for the admin
        transactions = anvil.server.call('get_wallet_transactions')
        
        # Group transactions by date
        self.grouped_transactions = {}
        for item in transactions:
            # Extract date in YYYY-MM-DD format without time
            date_str = item['date'].strftime("%Y-%m-%d")
            if date_str not in self.grouped_transactions:
                self.grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
            self.grouped_transactions[date_str]['transactions'].append(item)
        
        # Sort dates in descending order
        sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)
        
        # Create a list of dictionaries for repeating_panel_1
        self.repeating_panel_1.items = self.create_repeating_panel_items(sorted_dates)

    def create_repeating_panel_items(self, sorted_dates):
        repeating_panel_1_items = []
        for date_str in sorted_dates:
            date_info = self.grouped_transactions[date_str]
            for transaction in reversed(date_info['transactions']):
                fund = transaction['fund']
                transaction_type = transaction['transaction_type']
                receiver_phone = transaction['receiver_phone']
                
                # Fetch username from wallet_user table using receiver_phone
                receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                if receiver_user:
                    receiver_username = receiver_user['username']
                else:
                    receiver_username = "Unknown"
                
                if transaction_type.lower() == 'credit':
                    fund_display = "+" + str(fund)
                    fund_color = "green"
                elif transaction_type.lower() == 'debit':
                    fund_display = "-" + str(fund)
                    fund_color = "red"
                else:
                    fund_display = str(fund)
                    fund_color = "black"
                
                # Append transaction details with username instead of receiver_phone
                repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                'fund': fund_display,
                                                'transaction_status': transaction['transaction_status'],
                                                'receiver_username': receiver_username,
                                                'fund_color': fund_color})
        return repeating_panel_1_items

    def link_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.report_analysis', user=self.user)

    def link_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.account_management', user=self.user)

    def link_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.transaction_monitoring', user=self.user)

    def link_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.admin_add_user', user=self.user)

    def link_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin.audit_trail', user=self.user)

    def link_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        serves_data = app_tables.wallet_users_service.search()
        # Open the admin.user_support form and pass the serves_data
        user_support_form = open_form('admin.user_support', serves_data=serves_data, user=self.user)

    def link_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        show_users_form = open_form('admin.show_users', user=self.user)

    def link_8_copy_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('admin', user=self.user)

    def button_8_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('Login')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Get the user entered in the textbox
        entered_user = self.textbox_search.text.strip()

        if entered_user:
            # Filter transactions based on the entered user
            self.update_transactions_by_receiver(entered_user)

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        receiver_phone = self.text_box_1.text.strip()
        if receiver_phone:
            # Display transactions for the entered receiver's phone number
            self.update_transactions_by_receiver(receiver_phone)

    def drop_down_4_change(self, **event_args):
        """This method is called when an item is selected"""
        selected_option = self.drop_down_4.selected_value
        
        if selected_option == "Type":
            # Show dropdown and card for Type
            self.drop_down_3.visible = True
            self.card_3.visible = True
            self.label_13.visible = True
            # Hide other elements
            self.label_5.visible = False
            self.label_2.visible = False
            self.drop_down_1.visible = False
            self.drop_down_2.visible = False
            self.label_3_copy_2.visible = False
        elif selected_option == "Date":
            # Show elements for Date
            self.label_5.visible = True
            self.label_2.visible = True
            self.label_3_copy_2.visible = True
            self.drop_down_1.visible = True
            self.drop_down_2.visible = True
            self.card_3.visible = True
            # Hide other elements
            self.drop_down_3.visible = False
            self.label_13.visible = False
        elif selected_option == "filter":
            self.drop_down_3.visible = False
            self.card_3.visible = False
            self.label_13.visible = False
            # Hide other elements
            self.label_5.visible = False
            self.label_2.visible = False
            self.drop_down_1.visible = False
            self.drop_down_2.visible = False
            self.label_3_copy_2.visible = False

    def drop_down_3_change(self, **event_args):
        """This method is called when the transaction type dropdown selection changes"""
        selected_transaction_type = self.drop_down_3.selected_value
        
        # Update transactions based on the selected transaction type
        if selected_transaction_type:
            self.update_transactions_by_type(selected_transaction_type)

    def drop_down_1_change(self, **event_args):
        """This method is called when the month dropdown selection changes"""
        selected_month = self.drop_down_1.selected_value
        selected_year = self.drop_down_2.selected_value
        if selected_month and selected_year:
            self.update_repeating_panel(selected_month, selected_year)

    def drop_down_2_change(self, **event_args):
        """This method is called when the year dropdown selection changes"""
        selected_month = self.drop_down_1.selected_value
        selected_year = self.drop_down_2.selected_value
        if selected_month and selected_year:
            self.update_repeating_panel(selected_month, selected_year)

    def update_repeating_panel(self, selected_month, selected_year):
        """Update the repeating panel with transactions for the selected month and year"""
        repeating_panel_1_items = []
        selected_month = int(selected_month)
        selected_year = int(selected_year)
        for date_str, date_info in self.grouped_transactions.items():
            date = date_info['date']
            if date.month == selected_month and date.year == selected_year:
                for transaction in reversed(date_info['transactions']):
                    fund = transaction['fund']
                    transaction_type = transaction['transaction_type']
                    receiver_phone = transaction['receiver_phone']
                    
                    # Fetch username from wallet_user table using receiver_phone
                    receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                    if receiver_user:
                        receiver_username = receiver_user['username']
                    else:
                        receiver_username = "Unknown"
                    
                    if transaction_type.lower() == 'credit':
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction_type.lower() == 'debit':
                        fund_display = "-" + str(fund)
                        fund_color = "red"
                    else:
                        fund_display = str(fund)
                        fund_color = "black"
                        
                    # Append transaction details with username instead of receiver_phone
                    repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                    'fund': fund_display,
                                                    'transaction_status': transaction['transaction_status'],
                                                    'receiver_username': receiver_username,
                                                    'fund_color': fund_color})
        self.repeating_panel_1.items = repeating_panel_1_items

    def update_transactions_by_receiver(self, receiver_phone):
        
        receiver_phone_number = int(receiver_phone)  # Convert string to integer
        """Update the transaction history based on the receiver's phone number"""
        receiver_user = app_tables.wallet_users.get(phone=receiver_phone_number)
        if receiver_user:
            receiver_username = receiver_user['username']
        else:
            receiver_username = "Unknown"
    
        items = app_tables.wallet_users_transaction.search(receiver_phone=receiver_phone_number)
        # Rest of the method remains the same...
        grouped_transactions = {}
        for item in items:
            # Extract date in YYYY-MM-DD format without time
            date_str = item['date'].strftime("%Y-%m-%d")
            if date_str not in grouped_transactions:
                grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
            grouped_transactions[date_str]['transactions'].append(item)

        # Sort dates in descending order
        sorted_dates = sorted(grouped_transactions.keys(), reverse=True)

        # Create a list of dictionaries for repeating_panel_1
        repeating_panel_1_items = []
        for date_str in sorted_dates:
            date_info = grouped_transactions[date_str]
            # repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d")})  # Format date without time
            for transaction in reversed(date_info['transactions']):
                fund = transaction['fund']
                transaction_type = transaction['transaction_type']
                if transaction_type == 'credit':
                    fund_display = "+" + str(fund)
                    fund_color = "forestgreen"
                elif transaction_type == 'debit':
                    fund_display = "-" + str(fund)
                    fund_color = "red"
                else:
                    fund_display = str(fund)
                    fund_color = "black"
                repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),'fund': fund_display,'transaction_status':transaction['transaction_status'], 'receiver_username': receiver_username, 'fund_color': fund_color})

        self.repeating_panel_1.items = repeating_panel_1_items


    def update_transactions_by_type(self, transaction_type):
        """Update the repeating panel with transactions for the given transaction type"""
        repeating_panel_1_items = []
        for date_str, date_info in self.grouped_transactions.items():
            for transaction in date_info['transactions']:
                if transaction['transaction_type'] == transaction_type:
                    fund = transaction['fund']
                    receiver_phone = transaction['receiver_phone']
                    receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                    if receiver_user:
                        receiver_username = receiver_user['username']
                    else:
                        receiver_username = "Unknown"
                    
                    if transaction_type.lower() == 'credit':
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction_type.lower() == 'debit':
                        fund_display = "-" + str(fund)
                        fund_color = "red"
                    else:
                        fund_display = str(fund)
                        fund_color = "black"
                    
                    repeating_panel_1_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                                    'fund': fund_display,
                                                    'transaction_status': transaction['transaction_status'],
                                                    'receiver_username': receiver_username,
                                                    'fund_color': fund_color})
        self.repeating_panel_1.items = repeating_panel_1_items
