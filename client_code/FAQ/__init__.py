from ._anvil_designer import FAQTemplate
from anvil import *
import anvil.server

class FAQ(FAQTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.card_2.visible= True
    self.label_21.visible = False
    self.label_22.visible = False
    self.label_23.visible = False
    self.label_34.visible = False
    self.label_35.visible = False
    self.label_36.visible = False
    self.label_37.visible = False
    self.label_38.visible = False
    self.label_39.visible = False
    self.label_40.visible = False
    self.label_41.visible = False
    self.label_42.visible = False
    self.label_43.visible = False
    self.label_44.visible = False
    self.label_45.visible = False
    

  def link_8_click(self, **event_args):
    self.card_1.visible = not self.card_1.visible
    self.card_3.visible = False
    self.card_5.visible = False

  def link_13_click(self, **event_args):
    self.card_3.visible = not self.card_3.visible
    self.card_1.visible = False
    self.card_5.visible = False
   

  def link_15_click(self, **event_args):
    self.card_5.visible = not self.card_5.visible
    self.card_1.visible = False
    self.card_3.visible = False
    
  def link_1_click(self, **event_args):
    self.label_21.visible = not self.label_21.visible
    
  def link_2_click(self, **event_args):
    self.label_22.visible = not self.label_22.visible

  def link_3_click(self, **event_args):
    self.label_23.visible = not self.label_23.visible
    
  def link_4_click(self, **event_args):
    self.label_34.visible = not self.label_34.visible
    
  def link_5_click(self, **event_args):
    self.label_35.visible = not self.label_35.visible
    
  def link_6_click(self, **event_args):
    self.label_36.visible = not self.label_36.visible
    
  def link_7_click(self, **event_args):
    self.label_37.visible = not self.label_37.visible
    
  def link_12_click(self, **event_args):
    self.label_38.visible = not self.label_38.visible
    
  def link_14_click(self, **event_args):
    self.label_39.visible = not self.label_39.visible
    
  def link_18_click(self, **event_args):
    self.label_40.visible = not self.label_40.visible
    
  def link_19_click(self, **event_args):
    self.label_41.visible = not self.label_41.visible
    
  def link_20_click(self, **event_args):
    self.label_42.visible = not self.label_42.visible
    
  def link_21_click(self, **event_args):
    self.label_43.visible = not self.label_43.visible
    
  def link_22_click(self, **event_args):
    self.label_44.visible = not self.label_44.visible
    
  def link_23_click(self, **event_args):
    self.label_45.visible = not self.label_45.visible

  def link_16_click(self, **event_args):
    open_form('contact_us')

  def button_3_click(self, **event_args):
     open_form('Login')

  def link_24_click(self, **event_args):
    open_form('about_us')

  def link_25_click(self, **event_args):
    pass

  def link_26_click(self, **event_args):
    open_form('FAQ')

  def link_27_click(self, **event_args):
    open_form('contact_us')

  def home_click(self, **event_args):
    open_form('Home')

  def about_us_click(self, **event_args):
    open_form('about_us')

  def products_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def contact_click(self, **event_args):
    open_form('contact_us')

  def help_click(self, **event_args):
    pass

  def button_1_click(self, **event_args):
    open_form('Login')

  def button_2_click(self, **event_args):
    open_form('Signup')

  

 


    





    
