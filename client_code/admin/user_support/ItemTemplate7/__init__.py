from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
    def __init__(self, item=None, **properties):
        # Initialize component properties
        self.init_components(**properties)
        
        # Store the item data
        self.item = item
        
        # Bind data to UI elements
        self.label_1.text = self.item['users_service_username']
        self.label_2.text = self.item['users_service_phone']
        self.label_3.text = self.item['users_service_email']
        self.text_area_1.text = self.item['users_service_query']
        
        # Fetch profile photo based on phone number
        self.fetch_profile_photo(self.item['users_service_phone'])
        
        # Set button text and color based on users_update status
        self.update_button_status()

    def fetch_profile_photo(self, phone_number):
        # Fetch and display profile photo
        user_row = app_tables.wallet_users.get(users_phone=phone_number)
        
        if user_row:
            try:
                profile_photo = user_row['users_profile_pic']
                if profile_photo:
                    self.image_1.source = profile_photo
                else:
                    self.image_1.source = 'path/to/default/image.png'
            except KeyError:
                self.image_1.source = 'path/to/default/image.png'
        else:
            self.image_1.source = 'path/to/default/image.png'

    def update_button_status(self):
      
          # Display button text based on users_update status
          if self.item.get('users_update'):
              if self.item['users_update']:
                  self.button_1.text = 'Solved'
                  self.button_1.foreground = 'green'
              else:
                  self.button_1.text = 'Unsolved'
                  self.button_1.foreground = 'red'
          else:
              print("No 'users_update' field found in item data.")
              # Assuming unsolved if 'users_update' field is missing or False
              self.button_1.text = 'Unsolved'
              self.button_1.foreground = 'red'
      
     
  
      