from ._anvil_designer import adminTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server


class admin(adminTemplate):
  def __init__(self, user=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = user
    if user is not None:
            self.label_2.text = user['username']

  def link_1_click(self, **event_args):
    open_form('admin.report_analysis')

  def link_2_click(self, **event_args):
    open_form('admin.account_management')

  def link_3_click(self, **event_args):
    open_form('admin.transaction_monitoring')

  def link_4_click(self, **event_args):
    open_form('admin.admin_add_user')

  def link_5_click(self, **event_args):
    open_form('admin.audit_trail')

  def link_6_click(self, **event_args):
    open_form('admin.user_support')

  def link_7_click(self, **event_args):
    open_form('admin.show_users')

  def link_9_click(self, **event_args):
    open_form('Home')

  def link_10_click(self, **event_args):
    open_form('admin.add_currency')
