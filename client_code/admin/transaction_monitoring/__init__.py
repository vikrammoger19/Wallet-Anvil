from ._anvil_designer import transaction_monitoringTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class transaction_monitoring(transaction_monitoringTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    transactions = anvil.server.call('get_wallet_transactions')
        # Assuming you have a repeating panel named repeating_panel_1
    self.repeating_panel_1.items = transactions

    # Any code you write here will run before the form opens.
