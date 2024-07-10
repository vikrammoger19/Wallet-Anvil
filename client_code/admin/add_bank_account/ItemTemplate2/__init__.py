from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, bank_record=None, delete_callback=None, **properties):
        self.init_components(**properties)
        self.bank_record = bank_record
        self.delete_callback = delete_callback

        if bank_record:
            self.text_box_1.text = bank_record['admins_add_bank_names']
        

    def button_1_click(self, **event_args):
        """This method is called when the delete button is clicked"""
        if self.delete_callback:
            self.delete_callback(self.bank_record)