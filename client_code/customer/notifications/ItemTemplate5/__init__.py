from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate5(ItemTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.link1_clicked=True
    if self.item['read']:
      self.column_panel_1.background='#efeff0'
    else:
      self.column_panel_1.background='#87cefa'

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

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    
    self.column_panel_1.background='#efeff0'
    self.link_1.visible=False
    self.link_clicked=True
    a=anvil.server.call('get_notification_details',self.item['phone'],self.label_1.text,self.item['date'])
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.link1_clicked:
      self.link_1.border='#87cefa'
      self.link1_clicked=False
      self.link_1.visible=True
      
    else:
      self.link_1.visible=False
      self.link_1.border=''
      self.link1_clicked=True
