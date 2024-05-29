from ._anvil_designer import transactionsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class transactions(transactionsTemplate):
  def __init__(self,user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    self.users_balance()
    self.link11_clicked = True
    self.link12_clicked = False
    self.link13_clicked = False
    self.link14_clicked = False
    self.link15_clicked = False
    self.repeating_panel_items = []
    #users transactions all
    self.all_transactions()
    # Any code you write here will run before the form opens.

  def date_picker_1_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.date_filter()

  def date_picker_2_change(self, **event_args):
    """This method is called when the selected date changes"""
    print(self.date_picker_2.date)
    self.date_filter()

  def users_balance(self):
    phone = self.user['users_phone']
    users_details = app_tables.wallet_users.get(users_phone=phone)
    default_currency = 'INR'
    try:
      if users_details['users_defaultcurrency']:
        default_currency = users_details['users_defaultcurrency']
      users_balance = app_tables.wallet_users_balance.get(users_balaphone=phone,currency_type=default_currency)
      print('yes in')
      try:
        if users_balance:
          if int(users_balance['balance']) :
            self.label_4.text = f"{users_balance['balance']:.2f}"
            self.label_4.icon = f'fa:{default_currency.lower()}'
        else:
            self.label_4.text = '0'
                
      except Exception as e:
        print(e)
        try:
          if users_balance:
            if float(users_balance['balance']):
              self.label_4.text = f"{float(users_balance['balance']):.2f}"
              self.label_4.icon = f'fa:{default_currency.lower()}'
          else:
            self.label_4.text = '0'
          
        except Exception as e:
          print(e)
    except Exception as e:
      print(e)

    
  def all_transactions(self):
    items = app_tables.wallet_users_transaction.search(phone=self.user['phone'])
    self.grouped_transactions = {}
    print('yes')
    if items:
      for item in items:
          print('yes1')
          # Extract date in YYYY-MM-DD format without time
          date_str = item['date'].strftime("%Y-%m-%d")
          if date_str not in self.grouped_transactions:
              self.grouped_transactions[date_str] = {'date': item['date'], 'transactions': []}
          self.grouped_transactions[date_str]['transactions'].append(item)
    else:
      return

    # Sort dates in descending order
    sorted_dates = sorted(self.grouped_transactions.keys(), reverse=True)

    # Create a list of dictionaries for repeating_panel_1
    # repeating_panel_items = []
    for date_str in sorted_dates:
        date_info = self.grouped_transactions[date_str]
        for transaction in reversed(date_info['transactions']):
            fund = transaction['fund']
            transaction_type = transaction['transaction_type']
            receiver_phone = transaction['receiver_phone']
            transaction_time = transaction['date'].strftime("%I:%M %p")
            
            # Fetch username from wallet_user table using receiver_phone
            receiver_user = app_tables.wallet_users.get(phone=receiver_phone)
            if receiver_user:
                receiver_username = receiver_user['username']
            else:
                receiver_username = self.user['username']
            
            if transaction_type == 'Credit' or transaction_type == 'Deposited':
                fund_display = "+" + str(fund)
                fund_color = "green"
            elif transaction_type == 'Debit' or transaction_type == 'Withdrawn':
                fund_display = "-" + str(fund)
                fund_color = "red"
            else:
                fund_display = str(fund)
                fund_color = "black"
            
            # Append transaction details with username instead of receiver_phone
            self.repeating_panel_items.append({'date': date_info['date'].strftime("%Y-%m-%d"),
                                            'fund': fund_display,
                                            'transaction_status': transaction['transaction_status'],
                                            'transaction_type':transaction['transaction_type'],
                                            'receiver_username': receiver_username,
                                            'currency_type':transaction['currency'],
                                            'transaction_time':transaction_time,
                                            'fund_color': fund_color})

    self.repeating_panel_3.items = self.repeating_panel_items
    
  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    #all transactions linked
    """This method is called when the button is clicked"""
    self.link_11.foreground = '#148efe'
    self.link_12.foreground = 'black'
    self.link_13.foreground = 'black'
    self.link_14.foreground = 'black'
    self.link_15.foreground = 'black'
    self.link11_clicked = True
    self.link12_clicked = False
    self.link13_clicked = False
    self.link14_clicked = False
    self.link15_clicked = False
    all=[]
    for i in range(len(self.repeating_panel_items)):
      all.append({'date': self.repeating_panel_items[i]['date'],
                                          'fund': self.repeating_panel_items[i]['fund'],
                                          'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                          'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                          'currency_type':self.repeating_panel_items[i]['currency_type'],
                                          'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                          'fund_color': self.repeating_panel_items[i]['fund_color']})
    self.repeating_panel_3.items = all

  def link_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.link_11.foreground = 'black'
    self.link_12.foreground = '#148efe'
    self.link_13.foreground = 'black'
    self.link_14.foreground = 'black'
    self.link_15.foreground = 'black'
    self.link11_clicked = False
    self.link12_clicked = True
    self.link13_clicked = False
    self.link14_clicked = False
    self.link15_clicked = False
    received=[]
    #all transactions that are received from 
    for i in range(len(self.repeating_panel_items)):
          if  self.repeating_panel_items[i]['transaction_type'] == 'Credit' :
            received.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
    self.repeating_panel_3.items = received


  def link_13_click(self, **event_args):
  
    """This method is called when the button is clicked"""
    self.link_11.foreground = 'black'
    self.link_12.foreground = 'black'
    self.link_13.foreground = '#148efe'
    self.link_14.foreground = 'black'
    self.link_15.foreground = 'black'
    self.link11_clicked = False
    self.link12_clicked = False
    self.link13_clicked = True
    self.link14_clicked = False
    self.link15_clicked = False
    transfer=[]
    #all transactions that are transfered to
    for i in range(len(self.repeating_panel_items)):
          if  self.repeating_panel_items[i]['transaction_type'] == 'Debit' :
            transfer.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
    self.repeating_panel_3.items = transfer

  def link_14_click(self, **event_args):
    """This method is called when the link is clicked"""
    
    self.link_11.foreground = 'black'
    self.link_12.foreground = 'black'
    self.link_13.foreground = 'black'
    self.link_14.foreground = '#148efe'
    self.link_15.foreground = 'black'
    self.link11_clicked = False
    self.link12_clicked = False
    self.link13_clicked = False
    self.link14_clicked = True
    self.link15_clicked = False
    withdraw=[]
    for i in range(len(self.repeating_panel_items)):
          if  self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn' :
            withdraw.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
    self.repeating_panel_3.items = withdraw

  def link_15_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.link_11.foreground = 'black'
    self.link_12.foreground = 'black'
    self.link_13.foreground = 'black'
    self.link_14.foreground = 'black'
    self.link_15.foreground = '#148efe'
    self.link11_clicked = False
    self.link12_clicked = False
    self.link13_clicked = False
    self.link14_clicked = False
    self.link15_clicked = True
    deposit=[]
    for i in range(len(self.repeating_panel_items)):
          if  self.repeating_panel_items[i]['transaction_type'] == 'Deposited' :
            deposit.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund':f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
    self.repeating_panel_3.items = deposit
  
  def date_filter(self):
    #filtering by dates in all transactions 
    if self.link11_clicked :
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      all=[]
      if (self.date_picker_1.date and self.date_picker_2.date): 
        
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")):
            all.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = all 
      elif (self.date_picker_1.date):
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) :
            all.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = all
      else:
        print('None')
    #filtering by dates in received
    if self.link12_clicked :
      self.link11_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      received=[]
      if (self.date_picker_1.date and self.date_picker_2.date): 
        
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['transaction_type'] == 'Credit':
            received.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = received
      elif (self.date_picker_1.date):
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['transaction_type'] == 'Credit' :
            received.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = received
      else:
        print('None')
      
     # filtering by dates in transfered
    if self.link13_clicked :
      self.link11_clicked = False
      self.link12_clicked = False
      self.link14_clicked = False
      self.link15_clicked = False
      transfered=[]
      if (self.date_picker_1.date and self.date_picker_2.date): 
        
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['transaction_type'] == 'Debit':
            transfered.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = transfered
      elif (self.date_picker_1.date):
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['transaction_type'] == 'Debit' :
            transfered.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': self.repeating_panel_items[i]['fund'],
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = transfered
      else:
        print('None')
     # filtering by dates in transfered
    if self.link14_clicked :
      self.link11_clicked = False
      self.link12_clicked = False
      self.link13_clicked = False
      self.link15_clicked = False
      withdraw=[]
      if (self.date_picker_1.date and self.date_picker_2.date): 
        
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn':
            withdraw.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = withdraw
      elif (self.date_picker_1.date):
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn' :
            withdraw.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = withdraw
      else:
        print('None')
    if self.link15_clicked :
      self.link11_clicked = False
      self.link12_clicked = False
      self.link13_clicked = False
      self.link14_clicked = False
      deposit=[]
      if (self.date_picker_1.date and self.date_picker_2.date): 
        
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) <= str(self.repeating_panel_items[i]['date']) <= str(self.date_picker_2.date.strftime("%Y-%m-%d")) and self.repeating_panel_items[i]['transaction_type'] == 'Deposited':
            deposit.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = deposit
      elif (self.date_picker_1.date):
        for i in range(len(self.repeating_panel_items)):
          if  str(self.date_picker_1.date.strftime("%Y-%m-%d")) == str(self.repeating_panel_items[i]['date']) and self.repeating_panel_items[i]['transaction_type'] == 'Deposited' :
            deposit.append({'date': self.repeating_panel_items[i]['date'],
                                                'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = deposit
      else:
        print('None')

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    print(self.drop_down_1.selected_value)
    current_date = datetime.date.today()
    current_date_str = current_date.strftime("%Y-%m-%d")
    print(current_date)
    #all transactions
    if self.link11_clicked:
      if self.drop_down_1.selected_value == 'past 30 days':
        print(30)
        days_30=[]
        past_30_days = current_date - datetime.timedelta(days=30)
        print(past_30_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_30_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  :
              days_30.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_30

      if self.drop_down_1.selected_value == 'past 60 days':
        days_60=[]
        print(60)
        past_60_days = current_date - datetime.timedelta(days=60)
        print(past_60_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_60_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  :
              days_60.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_60
      
      if self.drop_down_1.selected_value == 'past 90 days':
        days_90=[]
        print(90)
        past_90_days = current_date - datetime.timedelta(days=90)
        print(past_90_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_90_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  :
              days_90.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_90


    #received transactions
    if self.link12_clicked:
      if self.drop_down_1.selected_value == 'past 30 days':
        print(30)
        days_30=[]
        past_30_days = current_date - datetime.timedelta(days=30)
        print(past_30_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_30_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Credit') :
              days_30.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_30

      if self.drop_down_1.selected_value == 'past 60 days':
        days_60=[]
        print(60)
        past_60_days = current_date - datetime.timedelta(days=60)
        print(past_60_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_60_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  and (self.repeating_panel_items[i]['transaction_type'] == 'Credit'):
              days_60.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_60
      
      if self.drop_down_1.selected_value == 'past 90 days':
        days_90=[]
        print(90)
        past_90_days = current_date - datetime.timedelta(days=90)
        print(past_90_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_90_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Credit') :
              days_90.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_90

    #transfered
    if self.link13_clicked:
      if self.drop_down_1.selected_value == 'past 30 days':
        print(30)
        days_30=[]
        past_30_days = current_date - datetime.timedelta(days=30)
        print(past_30_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_30_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Debit') :
              days_30.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_30

      if self.drop_down_1.selected_value == 'past 60 days':
        days_60=[]
        print(60)
        past_60_days = current_date - datetime.timedelta(days=60)
        print(past_60_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_60_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  and (self.repeating_panel_items[i]['transaction_type'] == 'Debit'):
              days_60.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_60
      
      if self.drop_down_1.selected_value == 'past 90 days':
        days_90=[]
        print(90)
        past_90_days = current_date - datetime.timedelta(days=90)
        print(past_90_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_90_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Debit') :
              days_90.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_90

    #withdraw details
    if self.link14_clicked:
      if self.drop_down_1.selected_value == 'past 30 days':
        print(30)
        days_30=[]
        past_30_days = current_date - datetime.timedelta(days=30)
        print(past_30_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_30_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn') :
              days_30.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_30

      if self.drop_down_1.selected_value == 'past 60 days':
        days_60=[]
        print(60)
        past_60_days = current_date - datetime.timedelta(days=60)
        print(past_60_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_60_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  and (self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn'):
              days_60.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_60
      
      if self.drop_down_1.selected_value == 'past 90 days':
        days_90=[]
        print(90)
        past_90_days = current_date - datetime.timedelta(days=90)
        print(past_90_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_90_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Withdrawn') :
              days_90.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_90

    #deposited
    if self.link15_clicked:
      if self.drop_down_1.selected_value == 'past 30 days':
        print(30)
        days_30=[]
        past_30_days = current_date - datetime.timedelta(days=30)
        print(past_30_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_30_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Deposited') :
              days_30.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_30

      if self.drop_down_1.selected_value == 'past 60 days':
        days_60=[]
        print(60)
        past_60_days = current_date - datetime.timedelta(days=60)
        print(past_60_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_60_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str)  and (self.repeating_panel_items[i]['transaction_type'] == 'Deposited'):
              days_60.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_60
      
      if self.drop_down_1.selected_value == 'past 90 days':
        days_90=[]
        print(90)
        past_90_days = current_date - datetime.timedelta(days=90)
        print(past_90_days)
        for i in range(len(self.repeating_panel_items)):
            if  str(past_90_days) <= str(self.repeating_panel_items[i]['date']) <= str(current_date_str) and (self.repeating_panel_items[i]['transaction_type'] == 'Deposited') :
              days_90.append({'date': self.repeating_panel_items[i]['date'],
                                                  'fund': f"{self.repeating_panel_items[i]['fund']}",
                                                  'transaction_status': self.repeating_panel_items[i]['transaction_status'],
                                                  'receiver_username': self.repeating_panel_items[i]['receiver_username'],
                                                  'currency_type':self.repeating_panel_items[i]['currency_type'],
                                                  'transaction_time':self.repeating_panel_items[i]['transaction_time'],
                                                  'fund_color': self.repeating_panel_items[i]['fund_color']})
        self.repeating_panel_3.items = days_90

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.withdraw', user=self.user)
    

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.deposit',user = self.user)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.transfer',user = self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer.service",user=self.user)

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("customer_page",user=self.user)

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Home")
    
