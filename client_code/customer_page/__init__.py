from ._anvil_designer import customer_pageTemplate
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objs as go
import datetime


class customer_page(customer_pageTemplate):
  def __init__(self, user=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user = user
        now = datetime.datetime.now()
        formatted_date = now.strftime('%a, %d-%b, %Y')
        self.label_11.text = formatted_date
