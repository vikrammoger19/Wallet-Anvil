from ._anvil_designer import notificationsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class notifications(notificationsTemplate):
  def __init__(self,user=None, **properties):
    # Set Form properties and Data Bindings.
    self.user=user
    self.init_components(**properties)
    items=[]
    self.repeating_panel_1.items=items
    an=anvil.server.call('get_notifications',self.user['users_phone'])
    so=sorted(an,key=lambda x:x['users_notification_date_time'],reverse=True)
    # length=0
    if so:
      for i in so:
        # column3=ColumnPanel(border='white',background='#87cefa')
        # if i['users_notification_read'] is None or i['users_notification_read'] is not True:
        a=i['users_notification_text']
        b=i['users_notification_date_time'] #.strftime("%a-%I:%M %p")
        c=i['users_notification_read']
        pic=i['users_notification_sender']
        items.append({'text':a,
                    'date':b,
                      'phone':self.user['users_phone'],
                      'read':c,
                     'sender_phone':pic})
      
      if len(items)>0:
        # self.label_2.text=len(items)
        self.repeating_panel_1.items=items
      else:
        label=Label(text='No notifications',background='',font_size=20,border='white')
        self.repeating_panel_1.visible=False
        self.column_panel_3.add_component(label)
        
      # else:
        # self.label_2.text=0
    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer',user=self.user)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.transactions',user=self.user)

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.deposit',user=self.user)

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.transfer',user=self.user)

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.withdraw',user=self.user)

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.auto_topup',user=self.user)

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.Viewprofile',user=self.user)

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('customer.settings',user=self.user)
