from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server


class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_1.text = self.item['admin_action_username']
    self.label_2.text = self.item['admin_action']
    self.label_3.text = self.item['date']
    self.label_4.text=self.item['admin_name']
    self.image_1.source = self.item['profile_pic']
    self.label_5.text=self.item['time']
    # Any code you write here will run before the form opens.
