import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window

# Import the necessary modules from pyjnius
from jnius import autoclass, cast
from android.permissions import request_permissions, check_permission, Permission

# Set background color for the app window
Window.clearcolor = (1, 1, 1, 1)  # White background

class DropBox(BoxLayout):
    def __init__(self, app, **kwargs):
        super(DropBox, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.label = Label(text='Drag and drop your contact spreadsheet here', size_hint_y=None, height=100, color=(0, 0, 0, 1))
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.label.text = 'Drop the file here...'
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if hasattr(touch, 'file_'):
                print("File dropped:", touch.file_)  # Debugging output
                self.app.load_contacts(touch.file_)
                self.label.text = 'File dropped! Loading...'
            return True


class BulkMessageApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.status_label = Label(text='Welcome to the Bulk Messaging App!', size_hint_y=None, height=50, color=(0, 0, 0, 1))
        self.layout.add_widget(self.status_label)

        # Drag and drop area for uploading contacts
        self.drop_box = DropBox(app=self)
        self.layout.add_widget(self.drop_box)

        # Button to upload contacts
        self.upload_btn = Button(text='Upload Contact Spreadsheet', size_hint_y=None, height=50, background_color=(1, 0.84, 0, 1), color=(0, 0, 0, 1))
        self.upload_btn.bind(on_release=self.open_filechooser)
        self.layout.add_widget(self.upload_btn)

        # Template input
        self.template_input = TextInput(hint_text='Enter your message template (e.g., Hello [Name])', size_hint_y=None, height=100, multiline=False, background_color=(0.9, 0.9, 0.9, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.template_input)

        # Send messages button
        self.send_btn = Button(text='Send Bulk Messages', size_hint_y=None, height=50, background_color=(0, 0.5, 1, 1), color=(1, 1, 1, 1))
        self.send_btn.bind(on_release=self.send_messages)
        self.layout.add_widget(self.send_btn)

        # Request necessary permissions on app start
        Clock.schedule_once(self.request_permissions, 1)

        return self.layout

    def request_permissions(self, *args):
        """Request necessary permissions using pyjnius and android library."""
        try:
            # Permissions needed for SMS functionality
            permissions = [Permission.SEND_SMS, Permission.RECEIVE_SMS, Permission.READ_SMS, Permission.RECEIVE_BOOT_COMPLETED]

            # Request permissions using the `request_permissions` function from the `android.permissions` module
            request_permissions(permissions, self.permission_callback)
        except Exception as e:
            self.status_label.text = f"Failed to request permissions: {e}"
            print(f"Failed to request permissions: {e}")

    def permission_callback(self, permissions, results):
        """Callback function to handle permission results."""
        if all(results):
            self.status_label.text = "All permissions granted!"
            print("All permissions granted!")
        else:
            self.status_label.text = "Some permissions were denied."
            print("Some permissions were denied.")

    def open_filechooser(self, instance):
        filechooser = FileChooserIconView()
        self.popup = Popup(title="Choose a file", content=filechooser, size_hint=(0.9, 0.9))
        filechooser.bind(on_submit=self.load_contacts_from_filechooser)
        self.popup.open()

        # Schedule the popup to close after 10 seconds if no file is selected
        Clock.schedule_once(self.dismiss_filechooser_popup, 10)

    def load_contacts_from_filechooser(self, filechooser, selection, touch):
        if selection:
            file_path = selection[0]
            print("Selected file:", file_path)  # Debugging output
            self.load_contacts(file_path)
            # Cancel the timeout if a file is selected
            Clock.unschedule(self.dismiss_filechooser_popup)

    def load_contacts(self, file_path):
        try:
            if not file_path.endswith('.csv'):
                raise ValueError("Please drop a CSV file or upload a CSV file.")
            with open(file_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                self.contacts = list(reader)
                self.drop_box.label.text = f'Loaded {len(self.contacts)} contacts.'
                print("Contacts loaded successfully:", self.contacts)  # Debugging output
                self.show_confirmation_popup()  # Show confirmation popup
                self.popup.dismiss()  # Dismiss the file chooser popup immediately after loading
        except Exception as e:
            self.drop_box.label.text = f'Error loading contacts: {str(e)}'
            print("Error loading contacts:", str(e))  # Debugging output

    def show_confirmation_popup(self):
        print("Attempting to show confirmation popup...")  # Debugging output
        self.popup_confirmation = Popup(title='Success',
                                        content=Label(text='Contacts successfully updated for blast!', color=(0, 0, 0, 1)),
                                        size_hint=(0.7, 0.4))
        self.popup_confirmation.open()
        print("Confirmation popup displayed.")  # Debugging output

        # Schedule the popup to close after 3 seconds
        Clock.schedule_once(self.dismiss_confirmation_popup, 3)

    def dismiss_confirmation_popup(self, dt):
        if hasattr(self, 'popup_confirmation'):
            self.popup_confirmation.dismiss()
            print("Confirmation popup dismissed after 3 seconds.")  # Debugging output

    def dismiss_filechooser_popup(self, dt):
        if self.popup:
            self.popup.dismiss()
            print("File chooser popup dismissed after 10 seconds.")  # Debugging output

    def send_messages(self, instance):
        template = self.template_input.text
        if not hasattr(self, 'contacts'):
            self.drop_box.label.text = 'Please upload contacts first.'
            return

        for contact in self.contacts:
            message = self.populate_template(template, contact)
            self.simulate_send_sms(contact['Phone Number'], message)

        self.drop_box.label.text = 'Bulk messages sent successfully!'

    def populate_template(self, template, contact):
        message = template
        for key in contact:
            placeholder = f'[{key}]'
            message = message.replace(placeholder, contact[key])
        return message

    def simulate_send_sms(self, phone_number, message):
        # Note: Sending SMS will need actual Android API integration, which can't be simulated here.
        print(f'Sending message to {phone_number}: {message}')  # Simulate SMS sending


if __name__ == '__main__':
    BulkMessageApp().run()
