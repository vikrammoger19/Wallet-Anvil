from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate7(ItemTemplate7Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Assign the properties to the labels and text area.
        self.label_1.text = self.item['users_service_username']
        self.label_2.text = self.item['users_service_phone']
        self.label_3.text = self.item['users_service_email']
        self.text_area_1.text = self.item['users_service_query']
        
        # Fetch the profile photo based on the phone number from 'wallet_users' table.
        self.fetch_profile_photo(self.item['users_service_phone'])
        
        # Set button text and color based on 'users_update' from 'wallet_users_service' table.
        self.update_button_status()

    def fetch_profile_photo(self, phone_number):
        print(f"Fetching profile photo for phone number: {phone_number}")

        # Query the wallet_users table for the user with the given phone number.
        user_row = app_tables.wallet_users.get(users_phone=phone_number)
        
        if user_row:
            print(f"User row found: {user_row}")
            try:
                profile_photo = user_row['users_profile_pic']
                if profile_photo:
                    print("Profile photo column found.")
                    # If a user is found and has a profile photo, display it.
                    self.image_1.source = profile_photo
                    print(f"Profile photo set: {profile_photo}")
                else:
                    # Log that the profile picture column is missing.
                    self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
                    print("Profile photo column is empty.")
            except KeyError:
                # Log that the profile picture column is missing.
                self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
                print("Profile photo column missing.")
        else:
            # Log that no user was found for the provided phone number.
            self.image_1.source = 'path/to/default/image.png'  # Optional: Add a default image path here
            print("No user found for the provided phone number.")

        # Optionally, you can also provide user feedback in the UI.
        if self.image_1.source == 'path/to/default/image.png':
            Notification("User data is incomplete or missing", title="Error", style="error").show()

    def update_button_status(self):
        try:
            # Fetch status from wallet_users_service
            user_status_row = app_tables.wallet_users_service.get(users_service_phone=self.item['users_service_phone'])
            if user_status_row:
                if user_status_row['users_update']:
                    self.button_1.text = 'Solved'
                    self.button_1.foreground = 'green'
                else:
                    self.button_1.text = 'Unsolved'
                    self.button_1.foreground = 'red'
            else:
                print("No status row found for the provided phone number.")
        except Exception as e:
            print(f"Error fetching status: {e}")
            Notification("Failed to fetch status", title="Error", style="error").show()

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        try:
            # Fetch the corresponding row from app_tables.wallet_users_service
            user_status_row = app_tables.wallet_users_service.get(users_service_phone=self.item['users_service_phone'])
            
            if user_status_row:
                # Update 'users_update' to True in the retrieved row
                user_status_row['users_update'] = True
                user_status_row.save()  # Save the updated row
                
                # Update button text and color
                self.button_1.text = 'Solved'
                self.button_1.foreground = 'green'
                
                # Provide feedback to the user
                Notification("Status updated to Solved", title="Success", style="success").show()
                
                # Refresh data after update
                self.refresh_data()
                
            else:
                # Log if no status row was found
                print("No status row found for the provided phone number.")
                Notification("No status row found", title="Error", style="error").show()
        
        except Exception as e:
            print(f"Error updating status: {e}")
            Notification("Failed to update status", title="Error", style="error").show()

    def refresh_data(self):
        # Implement your data refresh logic here
        print("Refreshing data...")  # Replace with actual logic to refresh data
        # For example, you can re-query the data or update UI components as needed
        self.update_button_status()  # Example: Refreshing button status after update
        self.fetch_profile_photo(self.item['users_service_phone'])  # Example: Refreshing profile photo
