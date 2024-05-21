from ._anvil_designer import customer_pageTemplate
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
from anvil import *

class customer_page(customer_pageTemplate):
    def __init__(self, user=None, **properties):
        # Initialize the form
        self.init_components(**properties)
        self.user = user
        user_dict = dict(self.user)
        self.refresh_data()

        # Assuming user has a 'phone' attribute
        phone_number = user_dict.get('phone', None)
        if phone_number:
            # Search transactions based on the user's phone number
            items = app_tables.wallet_users_transaction.search(phone=phone_number)
        
            # Sort transactions by date in descending order
            sorted_transactions = sorted(items, key=lambda x: x['date'], reverse=True)
        
            # Check if there are any transactions
            if not sorted_transactions:
                self.repeating_panel_2.items = [{
                    'fund': "",
                    'receiver_username': "You're a new user, make some activity!",
                    'transaction_text': "",
                    'transaction_time': "",
                    'fund_color': "black"
                }]
            else:
                # Process transactions as before
                self.repeating_panel_2_items = []
                max_history_entries = 5  # Maximum number of history entries to display
                for transaction in sorted_transactions:
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
                    if transaction_type == 'Credit':
                        transaction_text = "Received"
                        fund_display = "+" + str(fund)
                        fund_color = "green"
                    elif transaction_type == 'Debit':
                        transaction_text = "Sent"
                        fund_display = "-" + str(fund)
                        fund_color = "red"
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
        
                self.repeating_panel_2.items = self.repeating_panel_2_items

    def inr_balance(self, balance, currency_type):
        # Iterate through the iterator to find the balance for the specified currency_type
        for row in balance:
            if row['currency_type'] == currency_type:
                return row['balance']  # Return the balance for INR
        return '0'  # Fallback in case the currency_type is not found

    def link_10_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form("customer.transaction_history", user=self.user)

    def init_graph(self):
        # Create an empty figure
        fig = go.Figure()
      
        # Update plot with the empty figure
        self.plot_1.data = fig.data
        self.plot_1.layout = fig.layout

    def refresh_data(self):
        # Get the user's phone number
        phone_number = self.user['phone']
  
        # Call the server function to get transactions data
        transactions = anvil.server.call('get_transactions')
  
        # DEBUG: Print the number of transactions retrieved from the server
        print("Number of transactions retrieved:", len(transactions))
  
        # Filter transactions to include only those involving the user's phone number
        filtered_transactions = [t for t in transactions if t['phone'] == phone_number or t['receiver_phone'] == phone_number]
  
        # DEBUG: Print the number of transactions after filtering
        print("Number of transactions after filtering:", len(filtered_transactions))
  
        # Filter transactions to include only 'Credit' and 'Debit' types
        filtered_transactions = [t for t in filtered_transactions if t['transaction_type'] in ['Credit', 'Debit']]
  
        # Organize data for plotting (aggregate by date and type)
        data_for_plot = {'Credit': {}, 'Debit': {}}  # Separate dictionaries for Credit and Debit transactions
        for transaction in filtered_transactions:
            date = transaction['date'].strftime("%Y-%m-%d")  # Format date as string for grouping
  
            trans_type = transaction['transaction_type']
            fund = transaction['fund']  # Retrieve the 'fund' field
  
            if date not in data_for_plot[trans_type]:
                data_for_plot[trans_type][date] = 0
  
            # Ensure fund is a string or a number before conversion
            if isinstance(fund, (int, float)):
                money_amount = fund
            elif isinstance(fund, str):
                # Extract numeric value from the 'fund' field
                try:
                    money_amount = float(fund)
                except ValueError:
                    money_amount = 0  # Handle cases where conversion to float fails
            else:
                money_amount = 0  # Default to 0 if 'fund' is neither a string nor a number
  
            # Aggregate transaction amounts by date and type
            if trans_type in data_for_plot:
                data_for_plot[trans_type][date] += money_amount
  
        # DEBUG: Print the data for plotting
        print("Data for plotting:", data_for_plot)
  
        # Plot the data
        categories = list(set(data_for_plot['Credit'].keys()) | set(data_for_plot['Debit'].keys()))  # Combine dates from Credit and Debit transactions
        categories.sort()  # Sort the dates for a proper time series plot
        credit_values = [data_for_plot['Credit'].get(date, 0) for date in categories]  # Get credit values for each date or 0 if date not present
        debit_values = [data_for_plot['Debit'].get(date, 0) for date in categories]    # Get debit values for each date or 0 if date not present
  
        self.plot_1.data = [
            {'x': categories, 'y': debit_values, 'type': 'bar', 'name': 'Debit', 'marker': {'color': 'gray'}},
            {'x': categories, 'y': credit_values, 'type': 'bar', 'name': 'Credit', 'marker': {'color': 'lightblue'}}
        ]
  
        self.plot_1.visible = True

    def link_2_click(self, **event_args):
        open_form('customer.walletbalance', user=self.user)

    def link_3_click(self, **event_args):
        open_form('customer.transaction_history', user=self.user)

    def link_4_click(self, **event_args):
        open_form('customer.transfer', user=self.user)

    def link_5_click(self, **event_args):
        open_form('customer.withdraw', user=self.user)

    def link_7_click(self, **event_args):
        open_form('customer.Viewprofile', user=self.user)

    def link_6_click(self, **event_args):
        open_form('customer.auto_topup', user=self.user)

    def link_9_click(self, **event_args):
        open_form('Home', user=self.user)
