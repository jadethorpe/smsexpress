__author__ = "jade.thorpe@gmail.com"
"""
Sms Express - Send text via Twilio
"""
import toga
import csv
import pickle
from toga.style import Pack
from toga.style.pack import COLUMN
from twilio.rest import Client as TwilioRestClient


class smsExpress(toga.App):

    # Menu Bar
    def config_function(self, widget):
        self.label_title = toga.Label(
            "Enter the Twilio configuration information that was provided by your system administrator"
        )
        self.label_account_id = toga.Label(
            "Account ID", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_account_id = toga.MultilineTextInput(
            id="input1", initial=self.creds["account_sid"]
        )
        self.label_api_key = toga.Label(
            "API KEY", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_api_key = toga.MultilineTextInput(
            id="input2", initial=self.creds["api_key"]
        )
        self.label_api_secret = toga.Label(
            "API SECRET", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_api_secret = toga.MultilineTextInput(
            id="input3", initial=self.creds["api_secret"]
        )
        self.label_service_id = toga.Label(
            "Service ID", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_service_id = toga.MultilineTextInput(
            id="input4", initial=self.creds["service_id"], style=Pack(padding_bottom=20)
        )
        btn_save = toga.Button("Save", on_press=self.make_config, style=Pack(flex=1))

        outer_box = toga.Box(
            children=[
                self.label_title,
                self.label_account_id,
                self.input_account_id,
                self.label_api_key,
                self.input_api_key,
                self.label_api_secret,
                self.input_api_secret,
                self.label_service_id,
                self.input_service_id,
                btn_save,
            ],
            style=Pack(flex=1, direction=COLUMN, padding=30),
        )
        self.config_window = toga.Window(title="Twilio Config")
        self.config_window.content = outer_box
        self.config_window.show()

    def do_clear(self, widget, **kwargs):
        self.label.text = "Ready."

    def action_info_dialog(self, widget):
        self.main_window.info_dialog("smsExpress", "Done!")
        self.label.text = "Message Successfully Sent."

    def action_confirm_dialog(self, widget):
        if self.main_window.question_dialog("Ready to Send?", self.textbox.value):
            self.progress.start()
            self.send_sms(self.textbox.value, self.dist_label.text)
            self.progress.stop()
        else:
            self.label.text = "Canceled."

    def action_error_dialog(self, widget):
        self.main_window.error_dialog(
            "smsExpress",
            "Please check the format of you recipient list file.  This should be a CSV file with the column header of phone_number for the phone number column",
        )
        self.label.text = "Oh no!"

    def action_config_dialog(self, widget):
        self.main_window.error_dialog(
            "smsExpress", "Please configure Twilio Settings First"
        )
        self.label.text = "Oh noes..."

    def action_open_file_dialog(self, widget):
        try:
            fname = self.main_window.open_file_dialog(
                title="Choose Recipient List", multiselect=False
            )
            if fname is not None:
                self.dist_label.text = fname
            else:
                self.dist_label.text = "No Recipient List selected!"
        except ValueError:
            self.dist_label.text = "Open file dialog was canceled"

    def make_config(self, widget):
        self.creds = dict()
        self.creds["account_sid"] = self.input_account_id.value.strip()
        self.creds["api_key"] = self.input_api_key.value.strip()
        self.creds["api_secret"] = self.input_api_secret.value.strip()
        self.creds["service_id"] = self.input_service_id.value.strip()
        self.save_config(self.creds)
        return self.creds

    def load_config(self):
        try:
            f = open(".config", "rb")
            self.creds = pickle.load(f)
        except:
            self.creds = dict()
            self.creds["account_sid"] = ""
            self.creds["api_key"] = ""
            self.creds["api_secret"] = ""
            self.creds["service_id"] = ""

    def save_config(self, creds):
        # pickle dictionary
        f = open(".config", "wb")
        pickle.dump(creds, f)
        f.close()

    def startup(self):
        self.load_config()
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)
        self.label_account_id = toga.Label(
            "Account ID", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_account_id = toga.TextInput(
            id="input1", initial=self.creds["account_sid"]
        )
        self.label_api_key = toga.Label(
            "API KEY", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_api_key = toga.TextInput(id="input2", initial=self.creds["api_key"])
        self.label_api_secret = toga.Label(
            "API SECRET", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_api_secret = toga.TextInput(
            id="input3", initial=self.creds["api_secret"]
        )
        self.label_service_id = toga.Label(
            "Service ID", style=Pack(padding_top=20, padding_bottom=10)
        )
        self.input_service_id = toga.TextInput(
            id="input4", initial=self.creds["service_id"], style=Pack(padding_bottom=20)
        )
        btn_save = toga.Button("Save", on_press=self.make_config, style=Pack(flex=1))

        # Label Step 1.
        self.step1 = toga.Label(
            "STEP 1:  Select Recipient List.",
            style=Pack(padding_top=20, padding_bottom=20),
        )

        # Label to show responses.
        self.dist_label = toga.Label(
            "No Recipient List Selected",
            style=Pack(padding_top=10, padding_bottom=20),
        )

        # Label Step 2.
        self.step2 = toga.Label(
            "STEP 2:  Compose Message.", style=Pack(padding_top=20, padding_bottom=20)
        )

        self.textbox = toga.MultilineTextInput(id="message")

        # Label Step 3.
        self.step3 = toga.Label(
            "STEP 3:  Send Message.", style=Pack(padding_top=20, padding_bottom=20)
        )

        # Label to show responses.
        self.label = toga.Label("Ready.", style=Pack(padding_top=20, padding_bottom=20))

        # Buttons
        btn_style = Pack(flex=1)
        btn_open = toga.Button(
            "Choose Recipient List",
            on_press=self.action_open_file_dialog,
            style=btn_style,
        )
        btn_send = toga.Button(
            "Send", on_press=self.action_confirm_dialog, style=btn_style
        )

        # Progress Status
        self.progress = toga.ProgressBar(max=100, value=1)

        # Group
        config_group = toga.Group("Config")
        cmd_config = toga.Command(
            self.config_function, label="Config", group=config_group
        )

        # Outermost box
        box = toga.Box(
            children=[
                self.step1,
                btn_open,
                self.dist_label,
                self.step2,
                self.textbox,
                self.step3,
                btn_send,
                self.label,
                self.progress,
            ],
            style=Pack(flex=1, direction=COLUMN, padding=30),
        )

        # Add the content on the main window
        self.main_window.toolbar.add(cmd_config)
        self.main_window.content = box

        # Show the main window
        self.main_window.show()

    def send_sms(self, message, input_file):
        Message = str(message).strip()
        recipients = []

        # Create Credentials
        _account_sid = self.creds["account_sid"]
        _api_key = self.creds["api_key"]
        _api_secret = self.creds["api_secret"]
        self.service_id = self.creds["service_id"]
        self.client = TwilioRestClient(_api_key, _api_secret, _account_sid)

        try:
            with open(input_file, "rt") as f:
                reader = csv.DictReader(f, delimiter=",", quotechar='"')
                for row in reader:
                    recipient = {}
                    recipient["first_name"] = row["first_name"].strip()
                    recipient["last_name"] = row["last_name"].strip()
                    recipient["phone_number"] = row["phone_number"].strip()
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        "-", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        "(", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        ")", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        "\\", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        "/", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        ".", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        ",", ""
                    )
                    recipient["phone_number"] = recipient["phone_number"].replace(
                        "+1", ""
                    )

                    if len(recipient["phone_number"]) == 11 and recipient[
                        "phone_number"
                    ].startswith("1"):
                        recipient["phone_number"] = recipient["phone_number"][1:]
                    if len(recipient["phone_number"]) < 10:
                        continue
                    if len(recipient["phone_number"]) > 10:
                        continue
                    recipient["phone_number"] = "+1{0}".format(
                        recipient["phone_number"]
                    )
                    recipients.append(recipient)
        except:
            self.action_error_dialog(None)
            return 0
        count = 0
        recipient_list = list()
        for recipient in recipients:
            if recipient["phone_number"]:
                phone_number = recipient["phone_number"]
                recipient_list.append(
                    f'{{"binding_type": "sms", "address": "{phone_number}" }}'
                )
            else:
                pass
            count += 1
            self.progress.value = int(100 * (count / len(recipients)))

        # Usingn passthrough API with Notify to send up to 10,000 messages in bulk
        notification = self.client.notify.services(
            self.service_id
        ).notifications.create(to_binding=recipient_list, body=Message)

        self.action_info_dialog(self.progress)


def main():
    return smsExpress()
