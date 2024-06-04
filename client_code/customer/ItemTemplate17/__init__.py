from ._anvil_designer import ItemTemplate17Template
from anvil import *
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
            self.text_box_3.visible = True
            self.text_box_3.text = self.item['transaction_time']
            self.label_1.text = self.item['receiver_username']
            self.label_2.foreground = self.item['fund_color']
            # self.text_box_2.visible= True
            self.image_1.visible = True

 
