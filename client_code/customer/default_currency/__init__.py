from ._anvil_designer import default_currencyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class default_currency(default_currencyTemplate):
    def __init__(self,user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        
        # Set INR as the default currency initially
        self.default_currency = 'INR'
        users = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
         
        if users['users_defaultcurrency'] != None:
          self.default_currency = users['users_defaultcurrency']
        else:
          self.default_currency = 'INR'
        self.phone = self.user['users_phone']
        self.set_default_currency(self.default_currency,self.phone)

    # Event handlers for each radio button
    def link_1_click(self, **event_args):
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('INR',self.phone)

    def link_2_click(self, **event_args):
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('USD',self.phone)

    def link_3_click(self, **event_args):
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('EUR',self.phone)

    def link_4_click(self, **event_args):
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency('GBP',self.phone)

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
        def_curr = app_tables.wallet_users.get(users_phone=phone)
        def_curr.update(users_defaultcurrency=currency)

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('customer.settings',user=self.user)
    
