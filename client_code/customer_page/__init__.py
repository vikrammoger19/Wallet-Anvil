from ._anvil_designer import customer_pageTemplate
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class customer_page(customer_pageTemplate):
    def __init__(self, user=None, **properties):
        # Initialize the form
        self.init_components(**properties)
        self.user = user
        user_dict = dict(self.user)

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)
        if phone_number:
            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(phone=phone_number)

            # Group transactions by date
            self.grouped_transactions = {}
            for item in items:
                # Extract date in YYYY-MM-DD format without time
                date_str = item['date'].strftime("%Y-%m-%d")
                if date_str not in self.grouped_transactions:
                    self.grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
                self.grouped_transactions[date_str]['transactions'].append(item)

            # Sort dates in descending order
            sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)

            # Create a list of dictionaries for repeating_panel_2
            self.repeating_panel_2_items = []
            max_history_entries = 5  # Maximum number of history entries to display
            for date_str in sorted_dates:
                date_info = self.grouped_transactions[date_str]
                for transaction in reversed(date_info['transactions']):
                    fund = transaction['fund']
                    transaction_type = transaction['transaction_type']
                    receiver_phone = transaction['receiver_phone']
                    transaction_time = transaction['date'].strftime("%a-%I:%M %p")  # Concatenate day with time (e.g., Mon-06:20 PM)

                    # Fetch username from wallet_user table using receiver_phone
                    receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
                    if receiver_user:
                        receiver_username = receiver_user['username']
                    else:
                        receiver_username = "Unknown"

                    # Set the transaction text and color based on transaction type
                    if transaction_type == 'credit':
                        transaction_text = "Received"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction_type == 'debit':
                        transaction_text = "Sent"
                        fund_display = "-" + str(fund)
                        fund_color = "blue"
                    else:
                        transaction_text = "Unknown"
                        fund_display = str(fund)
                        fund_color = "black"

                    # Append transaction details with username, transaction text, time, and day
                    self.repeating_panel_2_items.append({
                        'fund': fund_display,
                        'receiver_username': receiver_username,
                        'transaction_text': transaction_text,
                        'transaction_time': transaction_time,
                        'fund_color': fund_color
                    })

                    # Limit the maximum number of history entries to display
                    if len(self.repeating_panel_2_items) >= max_history_entries:
                        break
                if len(self.repeating_panel_2_items) >= max_history_entries:
                    break

            self.repeating_panel_2.items = self.repeating_panel_2_items

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.transaction_history",user=self.user)
