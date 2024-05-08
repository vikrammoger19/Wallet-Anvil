from ._anvil_designer import default_currencyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class default_currency(default_currencyTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
    
        # Set INR as the default currency initially
        self.default_currency = 'INR'
        phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('INR',phone)

    # Event handlers for each radio button
    def link_1_click(self, **event_args):
        phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('INR',phone)

    def link_2_click(self, **event_args):
        phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('USD',phone)

    def link_3_click(self, **event_args):
        phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('EUR',phone)

    def link_4_click(self, **event_args):
        phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('GBP',phone)

    # Function to set default currency and update card backgrounds
    def set_default_currency(self, currency, phone):
        # Update background color of all cards to #80c1ff
        self.card_1.background = '#80c1ff'
        self.card_2.background = '#80c1ff'
        self.card_3.background = '#80c1ff'
        self.card_4.background = '#80c1ff'

        # Update background color of the selected card to #148EFE
        if currency == 'INR':
            self.card_1.background = '#165ece'
        elif currency == 'USD':
            self.card_2.background = '#165ece'
        elif currency == 'EUR':
            self.card_3.background = '#165ece'
        elif currency == 'GBP':
            self.card_4.background = '#165ece'

        # Update default currency
        self.default_currency = currency
        #store the currency to data tables
        def_curr = app_tables.wallet_users.get(phone=phone)
        def_curr.update(defaultcurrency=currency)
    
