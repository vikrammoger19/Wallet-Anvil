from ._anvil_designer import interactionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._anvil_designer import interactionTemplate
from anvil.tables import app_tables  # Import app_tables directly from your data tables module
import datetime  # Import the datetime module

class interaction(interactionTemplate):
    def __init__(self, user_data=None, phone_number=None, user=None, **properties):
        self.user = user
        self.phone_number = phone_number
        self.init_components(**properties)
        
        # Fetch and filter transactions data
        transactions = app_tables.wallet_users_transaction.search()
        panel1_items = []
        panel2_items = []
        
        for transaction in transactions:
            if transaction['receiver_phone'] == self.phone_number:
                panel1_items.append(transaction)
            else:
                panel2_items.append(transaction)
        
        self.repeating_panel_1.items = panel1_items
        self.repeating_panel_2.items = panel2_items

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # Get the input from the text box
        user_input = self.text_box_1.text

        # Determine if the input is a number or text
        try:
            fund = float(user_input)  # Try to convert the input to a number
            is_number = True
        except ValueError:
            is_number = False

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Store the input in the appropriate columns
        if is_number:
            # Store it in the "fund" column
            app_tables.wallet_users_transaction.add_row(
                fund=fund,
                message=None,
                phone=self.user,
                receiver_phone=self.phone_number,
                transaction_status="success",
                transaction_type="debit",
                date=current_datetime  # Store the current date and time
            )
        else:
            # Store it in the "message" column
            app_tables.wallet_users_transaction.add_row(
                fund=None,
                message=user_input,
                phone=self.user,
                receiver_phone=self.phone_number,
                transaction_type=None,
                date=current_datetime  # Store the current date and time
            )

        # After adding a new transaction, re-fetch and update the items for the repeating panels
        transactions = app_tables.wallet_users_transaction.search()
        panel1_items = []
        panel2_items = []
        
        for transaction in transactions:
            if transaction['receiver_phone'] == self.phone_number:
                panel1_items.append(transaction)
            else:
                panel2_items.append(transaction)
        
        self.repeating_panel_1.items = panel1_items
        self.repeating_panel_2.items = panel2_items
