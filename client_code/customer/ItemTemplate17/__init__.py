from ._anvil_designer import ItemTemplate17Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate17(ItemTemplate17Template):
  def __init__(self, **properties):
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        if self.item['receiver_username'] == "You're a new user, make some activity!":
            self.label_2.visible = False
            self.text_box_1.visible = False
            self.text_box_3.visible = False
            # self.text_box_2.visible= False
            self.image_1.visible =False
            self.label_1.text = self.item['receiver_username']
        else:
            self.label_2.visible = True
            
            try:
              if int(self.item['fund']) :
                self.label_2.text = f"{(self.item['fund'])}"
              
            except Exception as e:
              print(e)
              try:
                if float(self.item['fund']):
                  self.label_2.text = f"{float(self.item['fund']):.2f}"
              except Exception as e:
                print(e)
            self.label_2.icon = f"fa:{self.item['default_currency'].lower()}"
            self.label_2.icon_align = 'left'
            self.text_box_1.visible = True
            self.text_box_1.text = self.item['transaction_text']
            self.text_box_1.foreground = self.item['fund_color']
            self.text_box_3.visible = True
            self.text_box_3.text = self.item['transaction_time']
            name=''
            self.label_1.text = f"{self.item['receiver_username']}"
            if self.item['transaction_text'] == 'Sent':
              name='Sent to'
              self.label_1.text = f"{name} {self.item['receiver_username']}"
            elif self.item['transaction_text'] == 'Received':
              name='Payment from'
              self.label_1.text = f"{name} {self.item['receiver_username']}"
            elif self.item['transaction_text'] == 'Deposit':
              name=self.item['bank_name']
              self.label_1.text = f"{name}"
            elif self.item['transaction_text'] == 'Withdrawn':
              name=self.item['bank_name']
              self.label_1.text = f"{name}"
            elif self.item['transaction_text'] == 'Auto Topup':
              name='Auto Topup by'
              self.label_1.text = f"{name} {self.item['receiver_username']}"
              
            self.label_2.foreground = self.item['fund_color']
            # self.text_box_2.visible= True
            self.image_1.visible = True
            self.image_1.source = self.item['profile_pic']

 
