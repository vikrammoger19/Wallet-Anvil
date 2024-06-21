from ._anvil_designer import Wallet_IssueTemplate
from anvil import *
import anvil.server


class Wallet_Issue(Wallet_IssueTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
