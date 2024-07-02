from ._anvil_designer import default_currencyTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
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
        # else:
        #   self.default_currency = 'INR'
        # self.phone = self.user['users_phone']
        self.populate_balances()
        self.check()
        # self.set_default_currency(self.default_currency,self.phone)

    def populate_balances(self):
      try:
          # Retrieve balances for the current user
          user_phone = self.user['users_phone']
          user_balances = app_tables.wallet_users_balance.search(users_balance_phone=user_phone)
  
          # Print the retrieved data
          print("Retrieved balances:", user_balances)
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          country_label_index = 50  # Start from label_50 for country
          image_index = 1
  
          # Iterate over user balances and update card components
          for balance in user_balances:
              currency_type = balance['users_balance_currency_type']
              balance_amount = round(balance['users_balance'], 2)  # Round to 2 decimal places
  
              # Lookup the currency icon, symbol, and country in the wallet_currency table
              currency_record = app_tables.wallet_admins_add_currency.get(admins_add_currency_code=currency_type)
              currency_icon = currency_record['admins_add_currency_icon'] if currency_record else None
              country = currency_record['admins_add_currency_country'] if currency_record else None
  
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              label_balance = getattr(self, f'label_{label_index + 1}', None)
              label_country = getattr(self, f'label_{country_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              if card and label_curr_type and label_balance and image_icon and label_country:
                  print('yes coming')
                  # Update card components with balance data
                  label_curr_type.text = currency_type
                  label_balance.text = f"{balance_amount:.2f}"  # Format to 2 decimal places
                  label_balance.icon = f"fa:{currency_type.lower()}"
                  label_country.text = country
                  image_icon.source = currency_icon
                  card.background="#efeff0"
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

    def check(self):
      users=app_tables.wallet_users.get(users_phone=self.user['users_phone'])
      try:
        if users['users_defaultcurrency'] is not None:
          currency=users['users_defaultcurrency']
          card_index = 1
          label_index = 1  # Start from label_1
          # country_label_index = 50  # Start from label_50 for country
          # image_index = 1
          user_balances = app_tables.wallet_users_balance.search(users_balance_phone=self.user['users_phone'])
          # Iterate over user balances and update card components
          for balance in user_balances:
            card = getattr(self, f'card_{card_index}', None)
            label_curr_type = getattr(self, f'label_{label_index}', None)
            # if card and label_curr_type :
            if label_curr_type.text == users['users_defaultcurrency']:
              card.background='#87cefa'
            else:
              card.background='#efeff0'
                # Increment indices for the next iteration
            card.visible = True
            card_index += 1
            label_index += 2
            
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
            
      except Exception as e:
        print(e)
  
    # Event handlers for each radio button
    def link_1_click(self, **event_args):
        # phone = app_tables.wallet_users.get()["phone"]
        
        self.set_default_currency(self.label_1.text,1)
        # open_form("customer.ItemTemplate17")

    def link_2_click(self, **event_args):
        currency=self.label_3.text
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency(currency,2)

    def link_3_click(self, **event_args):
        currency=self.label_5.text
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency(currency,3)

    def link_4_click(self, **event_args):
        currency=self.label_7.text
        # phone = app_tables.wallet_users.get()["phone"]
        self.set_default_currency(currency,4)
      
    def link_9_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_9.text
      self.set_default_currency(currency,5)

    def link_11_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_11.text
      self.set_default_currency(currency,6)

    def link_12_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_13.text
      self.set_default_currency(currency,7)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_15.text
      self.set_default_currency(currency,8)

    def link_14_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_17.text
      self.set_default_currency(currency,9)

    def link_15_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_19.text
      self.set_default_currency(currency,10)

    def link_16_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_21.text
      self.set_default_currency(currency,11)

    def link_17_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_23.text
      self.set_default_currency(currency,12)

    def link_18_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_25.text
      self.set_default_currency(currency,13)

    def link_19_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_27.text
      self.set_default_currency(currency,14)

    def link_20_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_29.text
      self.set_default_currency(currency,15)

    def link_21_click(self, **event_args):
      """This method is called when the link is clicked"""
      currency=self.label_31.text
      self.set_default_currency(currency,16)
    
      
    # Function to set default currency and update card backgrounds
    def set_default_currency(self, currency,index):
        # Update background color of all cards to #80c1ff
      
        users=app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        try:
          if users['users_defaultcurrency'] is not None:
            # currency=users['users_defaultcurrency']
            card_index = 1
            label_index = 1  # Start from label_1
            # country_label_index = 50  # Start from label_50 for country
            # image_index = 1
            user_balances = app_tables.wallet_users_balance.search(users_balance_phone=self.user['users_phone'])
            # Iterate over user balances and update card components
            for balance in user_balances:
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              # if card and label_curr_type :
              if index==card_index:
                card.background='#87cefa'
              else:
                card.background='#efeff0'
                  # Increment indices for the next iteration
              card.visible = True
              card_index += 1
              label_index += 2
              
    
            # Set visibility of remaining cards to False if no data
            while card_index <= 12:
                card = getattr(self, f'card_{card_index}', None)
                if card:
                    card.visible = False
                card_index += 1
        except Exception as e:
          print(e)

        # Update background color of the selected card to #148EF

        # Update default currency
        self.default_currency = currency
        print('currency',currency)
        #store the currency to data tables
        def_curr = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        def_curr.update(users_defaultcurrency=self.default_currency)
        print('yes updating')

    # def button_1_click(self, **event_args):
    #   """This method is called when the button is clicked"""
    #   open_form('customer.settings',user=self.user)

    def link_2_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.walletbalance', user=self.user)

    def link_3_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transactions', user=self.user)

    def link_10_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.deposit', user=self.user)

    def link_4_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.transfer', user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw', user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.auto_topup', user=self.user)

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.settings', user=self.user)

    def link_1_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer", user=self.user)
      pass

    def link_8_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.wallet", user=self.user)

    def link_8_copy_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("help", user=self.user)
    
