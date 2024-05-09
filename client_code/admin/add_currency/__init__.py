from ._anvil_designer import add_currencyTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_currency(add_currencyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.flow_panel_1.visible = False
    self.refresh_users()

  def refresh_users(self, country_filter=None):
    if country_filter:
      self.country_type_filter = [user for user in app_tables.wallet_currency.search()
                                  if user['country'].lower().startswith(country_filter.lower())]
    else:
      self.country_type_filter = [user for user in app_tables.wallet_currency.search()]
    self.repeating_panel_1.items = self.country_type_filter

  def button_1_click(self, **event_args):
    country_filter = self.textbox_search.text
    self.refresh_users(country_filter)

  def textbox_search_pressed_enter(self, **event_args):
    country_filter = self.textbox_search.text
    self.refresh_users(country_filter)

  def button_2_click(self,add_country=None, **event_args):
    self.flow_panel_1.visible = True

  def button_3_click(self, **event_args):
    country_name = self.text_box_1.text.strip()
    currency_code = self.text_box_2.text.strip()
    if country_name and currency_code:
        country_name = country_name.capitalize()
        print(country_name)
        if len(currency_code)==3 and currency_code.isalpha():
            existing_country = app_tables.wallet_currency.search(country=country_name) 
            if len(existing_country) == 0: 
                new_currency = app_tables.wallet_currency.add_row(country=country_name, currency_code=currency_code.upper())
                self.refresh_users()
                self.text_box_1.text = ''
                self.text_box_2.text = ''
                self.flow_panel_1.visible = False
                alert('Currency added sucessfully')
            else:
              alert('Country already exists')
        else:
          alert('Invalid Currency Code')
    else:
      alert('Please fill the required fields.')

  def link_8_copy_click(self, **event_args):
    open_form('admin')

