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

        username = anvil.server.call('get_username', self.user['users_phone'])
        self.label_656.text = f"{username}"

        # Populate balances for the current user
        self.populate_balances()

    def populate_balances(self):
        try:
            # Retrieve balances for the current user
            user_phone = self.user['phone']
            user_balances = app_tables.wallet_users_balance.search(phone=user_phone)

            # Print the retrieved data
            print("Retrieved balances:", user_balances)

            # Initialize index for card and components
            card_index = 1
            label_index = 1  # Start from label_1
            country_label_index = 50  # Start from label_50 for country
            image_index = 1

            # Iterate over user balances and update card components
            for balance in user_balances:
                currency_type = balance['currency_type']
                balance_amount = balance['balance']

                # Lookup the currency icon, symbol, and country in the wallet_currency table
                currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
                currency_icon = currency_record['currency_icon'] if currency_record else None
                country = currency_record['country'] if currency_record else None
               

                # Get card and components for the current index
                card = getattr(self, f'card_{card_index}', None)
                label_curr_type = getattr(self, f'label_{label_index}', None)
                label_balance = getattr(self, f'label_{label_index + 1}', None)
                label_country = getattr(self, f'label_{country_label_index}', None)
                image_icon = getattr(self, f'image_icon_{image_index}', None)

                if card and label_curr_type and label_balance and image_icon and label_country:
                    # Update card components with balance data
                    label_curr_type.text = currency_type
                    label_balance.text = f"{balance_amount} "
                    label_balance.icon = f"fa:{currency_type.lower()}"
                    label_country.text = country
                    image_icon.source = currency_icon

                    # Set card visibility to True
                    card.visible = True

                    # Increment indices for the next iteration
                    card_index += 1
                    label_index += 2
                    country_label_index += 1
                    image_index += 1

            # Set visibility of remaining cards to False if no data
            while card_index <= 12:
                card = getattr(self, f'card_{card_index}', None)
                if card:
                    card.visible = False
                card_index += 1

        except Exception as e:
            # Print any exception that occurs during the process
            print("Error occurred during population of balances:", e)

    def fetch_and_display_balance(self, currency_type):
        if not currency_type:
            # If the text box is empty, display all balances
            self.populate_balances()
            return
        
        try:
            # Convert the currency type to uppercase
            currency_type = currency_type.upper()
            
            # Retrieve balance for the entered currency type
            user_phone = self.user['phone']
            balance_record = app_tables.wallet_users_balance.get(phone=user_phone, currency_type=currency_type)
            
            if balance_record:
                balance_amount = balance_record['balance']
                
                # Lookup the currency icon, symbol, and country in the wallet_currency table
                currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
                currency_icon = currency_record['currency_icon'] if currency_record else None
                country = currency_record['country'] if currency_record else None
                

                # Update card_1 components with balance data
                self.label_1.text = currency_type
                self.label_2.text = f"{balance_amount}"
                self.label_2.icon = f"fa:{currency_type.lower()}"
                self.label_50.text = country
                self.image_icon_1.source = currency_icon

                # Set card_1 visibility to True
                self.card_1.visible = True
            else:
                # If no balance found, hide card_1
                self.card_1.visible = False

            # Hide all other cards
            for i in range(2, 13):
                card = getattr(self, f'card_{i}', None)
                if card:
                    card.visible = False

        except Exception as e:
            # Print any exception that occurs during the process
            print("Error occurred during fetching and displaying balance:", e)

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        currency_type = self.text_box_1.text.strip().upper()  # Convert to uppercase
        self.fetch_and_display_balance(currency_type)

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('customer.deposit', user=self.user)

    # Other link click methods omitted for brevity

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
        open_form('customer_page', user=self.user)

    def link_13_click(self, **event_args):
        """This method is called when the link is clicked"""
        open_form('Home')
