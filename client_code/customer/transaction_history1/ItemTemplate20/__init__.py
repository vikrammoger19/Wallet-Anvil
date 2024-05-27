from ._anvil_designer import ItemTemplate20Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime


class ItemTemplate20(ItemTemplate20Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_1.text = self.item['receiver_username']
    self.label_5.text = f"at {self.item['transaction_time']}"
    
    #date string
    try:
    # Parse the date string
      date_obj = datetime.datetime.strptime(self.item['date'], "%Y-%m-%d")
      date_string = f"{date_obj.day} {date_obj.strftime('%B')} {date_obj.year}"
      self.label_2.text = date_string
    except Exception as e:
      print("Invalid date format. Please use DD-MM-YYYY.")
      print(e)
      return None

    #time string
    
    
    
    try:
      print(self.item['fund'])
      if int(self.item['fund']) :
        self.label_3.text = f"{self.item['fund']}"          
    except Exception as e:
      print(e)
      try:
        print(self.item['fund'])
        if float(self.item['fund']):
          
          self.label_3.text = f"{float(self.item['fund']):.2f}"
      except Exception as e:
        print(e)
    self.label_3.icon = f"fa:{self.item['currency_type'].lower()}"
    self.label_3.foreground = self.item['fund_color']
    
    
    if self.item['transaction_status'] == 'transfered-to':
      self.label_4.text = 'Transfer'
    if self.item['transaction_status'] == 'recieved-from':
      self.label_4.text = 'Received'
    if self.item['transaction_status'] == 'Wallet-Topup':
      self.label_4.text='Topup'
    if self.item['transaction_status'] == 'Wallet-Withdrawn':
      self.label_4.text = 'Withdraw'
    self.label_4.foreground = self.item['fund_color']

    # Any code you write here will run before the form opens.
