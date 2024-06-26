from ._anvil_designer import walletTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, get_open_form
import random

class wallet(walletTemplate):
    global  count
    def __init__(self, user=None, **properties):
        self.init_components(**properties)
        self.user = user
        
        #self.label_1.text = f"Welcome to Green Gate Financial, {user['users_username']}"
        self.bank_details_visible = False
        self.label_bank_details_error = Label(text="", role="alert")
        self.label_bank_name.visible = False
        self.drop_down_2.visible = False
        self.label_account_number.visible = False
        self.textbox_account_number.visible = False
        self.label_ifsc_code.visible = False
        self.textbox_ifsc_code.visible = False
        self.label_bank_details_error.visible = False
        self.button_save_bank_details.visible = False
        self.label_3.visible=False
        self.label_4.visible=False
        self.label_5.visible=False
        self.text_box_1.visible=False
        self.text_box_2.visible=False
        self.drop_down_1.visible=False
       
    def button_add_bank_details_click_click(self, **event_args):
       # Toggle the visibility of bank details labels and textboxes
        self.bank_details_visible = not self.bank_details_visible
        self.label_bank_name.visible = self.bank_details_visible
        self.drop_down_2.visible = self.bank_details_visible
        self.label_account_number.visible = self.bank_details_visible
        self.textbox_account_number.visible = self.bank_details_visible
        self.label_ifsc_code.visible = self.bank_details_visible
        self.textbox_ifsc_code.visible = self.bank_details_visible
        self.button_save_bank_details.visible = self.bank_details_visible
        self.label_3.visible=self.bank_details_visible
        self.label_4.visible=self.bank_details_visible
        self.label_5.visible=self.bank_details_visible
        self.text_box_1.visible=self.bank_details_visible
        self.text_box_2.visible=self.bank_details_visible
        self.drop_down_1.visible=self.bank_details_visible
        self.drop_down_2.items = anvil.server.call('get_all_banks_name')
        
        # self.label_bank_details_error.text = ""
       
    def button_save_bank_details_click(self, **event_args):
      bank_name = self.drop_down_2.selected_value
      account_number = self.textbox_account_number.text
      ifsc_code = self.textbox_ifsc_code.text
      account_holder_name = self.text_box_1.text
      branch_name = self.text_box_2.text
      account_Type = self.drop_down_1.selected_value

      search_data=app_tables.wallet_users_account.get(
        # users_account_number=int(account_number),
        users_account_bank_name=bank_name
      )
      
      if search_data == None:
        if bank_name and account_number and ifsc_code and account_holder_name and branch_name and account_Type:
          # Save the bank details to the 'accounts' table
          
          new_account = app_tables.wallet_users_account.add_row(
              users_account_phone= self.user['users_phone'],
              users_account_number=int(account_number),
              users_account_bank_name=bank_name, 
              users_account_ifsc_code=ifsc_code,
              users_account_holder_name = account_holder_name,
              users_account_branch_name = branch_name,
              users_account_type = account_Type,
              users_account_status_confirm=True
          )
        
          anvil.alert("Bank details saved successfully.", title="", large=True)
        else:
          anvil.alert("Please fill in all bank details", title="", large=True)
        open_form('customer.wallet',user= self.user)
      else:
        anvil.alert("Bank name already exists.", title="Duplicate Bank Name", large=True)
        
    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.walletbalance",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transactions",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.Viewprofile",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.wallet",user=self.user)

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.withdraw',user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('customer.auto_topup',user=self.user)





