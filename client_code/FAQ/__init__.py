from ._anvil_designer import FAQTemplate
from anvil import *
import anvil.server

class FAQ(FAQTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Initialize visibility of labels
        self.labels = [self.label_21, self.label_22, self.label_23, self.label_34, self.label_35,
                       self.label_36, self.label_37, self.label_38, self.label_39, self.label_40,
                       self.label_41, self.label_42, self.label_43, self.label_44, self.label_45]
        for label in self.labels:
            label.visible = False

    def link_click(self, link_index):
        # Close all labels
        for label in self.labels:
            label.visible = False
        # Open the clicked label
        self.labels[link_index].visible = True

    def link_1_click(self, **event_args):
        self.link_click(0)

    def link_2_click(self, **event_args):
        self.link_click(1)

    def link_3_click(self, **event_args):
        self.link_click(2)

    def link_4_click(self, **event_args):
        self.link_click(3)

    def link_5_click(self, **event_args):
        self.link_click(4)

    def link_6_click(self, **event_args):
        self.link_click(5)

    def link_7_click(self, **event_args):
        self.link_click(6)

    def link_8_click(self, **event_args):
        self.link_click(7)

    def link_9_click(self, **event_args):
        self.link_click(8)

    def link_10_click(self, **event_args):
        self.link_click(9)

    def link_11_click(self, **event_args):
        self.link_click(10)

    def link_12_click(self, **event_args):
        self.link_click(11)

    def link_13_click(self, **event_args):
        self.link_click(12)

    def link_14_click(self, **event_args):
        self.link_click(13)

    def link_15_click(self, **event_args):
        self.link_click(14)

    def link_16_click(self, **event_args):
        open_form('contact_us')

    def button_3_click(self, **event_args):
         open_form('Login')

    def link_17_click(self, **event_args):
        open_form('about_us')

    def link_18_click(self, **event_args):
        pass

    def link_19_click(self, **event_args):
        open_form('FAQ')

    def link_20_click(self, **event_args):
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
