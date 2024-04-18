from ._anvil_designer import interactionTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ._anvil_designer import interactionTemplate
from anvil.tables import app_tables  # Import app_tables directly from your data tables module
import datetime  # Import the datetime module

class interaction(interactionTemplate):
    def __init__(self, user_data=None, phone_number=None, user=None, **properties):
        self.user = user
        self.phone_number = phone_number
        self.init_components(**properties)
        
        # Fetch and filter transactions data
        print("User:", self.user)
        print("Phone Number:", self.phone_number)
        self.update_panels()
        

    def text_box_1_pressed_enter(self):
        """This method is called when the user presses Enter in this text box"""
        # Get the input from the text box
        user_input = self.text_box_1.text

        # Determine if the input is a number or text
        try:
            fund = float(user_input)  # Try to convert the input to a number
            is_number = True
        except ValueError:
            is_number = False

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Store the input in the appropriate columns
        if is_number:
            # Store it in the "fund" column
            app_tables.wallet_users_transaction.add_row(
                fund=fund,
                message=None,
                phone=self.user,
                receiver_phone=self.phone_number,
                transaction_status="success",
                transaction_type="debit",
                date=current_datetime  # Store the current date and time
            )
        else:
            # Store it in the "message" column
            app_tables.wallet_users_transaction.add_row(
                fund=None,
                message=user_input,
                phone=self.user,
                receiver_phone=self.phone_number,
                transaction_type=None,
                date=current_datetime  # Store the current date and time
            )

        # After adding a new transaction, update the panels
        self.update_panels()

    def update_panels(self):
      transactions = app_tables.wallet_users_transaction.search()
      panel1_items = []
      panel2_items = []
      
      for transaction in transactions:
          if transaction['receiver_phone'] == self.phone_number and transaction['phone'] == self.user:
              panel1_items.append(transaction)
          elif transaction['receiver_phone'] == self.user and transaction['phone'] == self.phone_number:
              panel2_items.append(transaction)
      
      self.repeating_panel_1.items = panel1_items
      self.repeating_panel_2.items = panel2_items
      
      self.update_labels(self.repeating_panel_1)
      self.update_labels(self.repeating_panel_2)
  

        
        
    
    def update_labels(self, repeating_panel):
      for item in repeating_panel.items:
          components = repeating_panel.get_components()
          if len(components) >= 2:
              label_1 = components[0]
              label_2 = components[1]
              if 'fund' in item:
                  label_1.text = f"Fund: {item['fund']}"
              elif 'message' in item:
                  label_1.text = f"Message: {item['message']}"
              
              if 'date' in item:
                  label_2.text = f"Date: {item['date']}"
              else:
                  label_2.text = "Date not available"
          else:
              print("Not enough components in the panel")
  
      # Adjust labels based on the repeating panel
      for item in repeating_panel.items:
          text_1 = ""
          text_2 = ""
          if 'fund' in item:
              text_1 = f"Fund: {item['fund']}"
          elif 'message' in item:
              text_1 = f"Message: {item['message']}"
          
          if 'date' in item:
              text_2 = f"Date: {item['date']}"
          else:
              text_2 = "Date not available"
  
          components = repeating_panel.get_components()
          if len(components) >= 2:
              label_1 = components[0]
              label_2 = components[1]
              label_1.text = text_1
              label_2.text = text_2
          else:
              print("Not enough components in the panel")