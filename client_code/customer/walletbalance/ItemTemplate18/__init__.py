from ._anvil_designer import ItemTemplate18Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate18(ItemTemplate18Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Ensure item is properly initialized before binding
        self.item = properties.get('item', {})
        print("Initializing ItemTemplate18 with item:", self.item)
        
        # Bind data to UI components
        self._initialize_bindings()

    def _initialize_bindings(self):
        # Ensure item is properly initialized before binding
        if self.item:
            self.label_1.text = self.item.get('currency_type', '')
            self.label_2.text = str(self.item.get('balance', ''))
            self.image_icon.source = self.item.get('currency_icon', '')  # Using 'currency_icon' as the key
            print(f"Binding item: {self.item}")
        else:
            # Log or print an error if self.item is not properly initialized
            print("Error: self.item is not properly initialized.")
