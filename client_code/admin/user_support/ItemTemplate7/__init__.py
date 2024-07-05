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
        # Update button text based on users_update status
        try:
            # Fetch the row from wallet_users_service for this specific item
            user_status_row = app_tables.wallet_users_service.get(users_service_phone=self.item['users_service_phone'])
            
            if user_status_row:
                if user_status_row['users_update']:
                    self.button_1.text = 'Solved'
                    self.button_1.foreground = 'green'
                else:
                    self.button_1.text = 'Unsolved'
                    self.button_1.foreground = 'red'
            else:
                print(f"No status row found for phone number: {self.item['users_service_phone']}")
                # Assuming unsolved if no status row found
                self.button_1.text = 'Unsolved'
                self.button_1.foreground = 'red'
        
        except Exception as e:
            print(f"Error fetching status: {e}")
            Notification("Failed to fetch status", title="Error", style="error").show()

    def button_1_click(self, **event_args):
        # Toggle users_update status for this specific item and refresh UI
        try:
            # Fetch the row from wallet_users_service for this specific item
            user_status_row = app_tables.wallet_users_service.get(users_service_phone=self.item['users_service_phone'])
            
            if user_status_row:
                # Update users_update status
                user_status_row['users_update'] = not user_status_row['users_update']
                user_status_row.save()
                
                self.refresh_data()
                self.update_button_status()
                
                if user_status_row['users_update']:
                    Notification("Status updated to Solved", title="Success", style="success").show()
                else:
                    Notification("Status updated to Unsolved", title="Success", style="success").show()
            
            else:
                print(f"No status row found for phone number: {self.item['users_service_phone']}")
                Notification("No status row found", title="Error", style="error").show()
        
        except Exception as e:
            print(f"Error updating status: {e}")
            Notification("Failed to update status", title="Error", style="error").show()

    def refresh_data(self):
        # Implement data refresh logic here if needed
        self.update_button_status()
