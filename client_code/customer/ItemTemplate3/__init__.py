from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link_clicked=True
    self.label_1.text=self.item['text']
    self.label_2.text=f'{self.item["date"].strftime( "%Y-%m-%d")} at {self.item["date"].strftime("%I:%M %p")}' #%a-
    try:
      pics=app_tables.wallet_users.get(users_phone=self.item['sender_phone'])
      if pics['users_profile_pic'] is not None:
        self.image_1.source=pics['users_profile_pic']
      else:
        self.image_1.source='_/theme/account.png'
    except Exception as e:
      print(e)
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.link_clicked:
      self.link_1.visible=True
      self.spacer_3.visible=True
      self.link_clicked=False
    else:
      self.link_1.visible=False
      self.link_clicked=True
      self.spacer_3.visible=False
      

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.column_panel_1.background='#efeff0'
    self.link_1.visible=False
    self.spacer_3.visible=False
    
    self.link_clicked=True
    # details=app_tables.wallet_users_notifications.search()
    # print('date text',self.label_2.text)
    # print(self.item['date'])
    a=anvil.server.call('get_notification_details',self.item['phone'],self.label_1.text,self.item['date'])
    # Any code you write here will run before the form opens.
