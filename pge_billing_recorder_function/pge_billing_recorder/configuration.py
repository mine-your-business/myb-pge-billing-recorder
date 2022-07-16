import os


class Configuration:

    def __init__(self):
        self.pge = PortlandGeneral()
        self.sheets = Sheets()


class PortlandGeneral:

    def __init__(self):
        self.username = os.environ.get('PGE_USERNAME')
        self.password = os.environ.get('PGE_PASSWORD')


class SheetsCredentials:

    def __init__(self):
        self.type = os.environ.get('SHEETS_CREDENTIALS_TYPE')
        self.project_id = os.environ.get('SHEETS_CREDENTIALS_PROJECT_ID')
        self.private_key_id = os.environ.get('SHEETS_CREDENTIALS_PRIVATE_KEY_ID')
        self.private_key = os.environ.get('SHEETS_CREDENTIALS_PRIVATE_KEY').replace(r'\n', '\n')
        self.client_email = os.environ.get('SHEETS_CREDENTIALS_CLIENT_EMAIL')
        self.client_id = os.environ.get('SHEETS_CREDENTIALS_CLIENT_ID')
        self.token_uri = os.environ.get('SHEETS_CREDENTILS_TOKEN_URI')
        self.auth_provider_x509_cert_url = os.environ.get('SHEETS_CREDENTIALS_AUTH_PROVIDER_X509_CERT_URL')
        self.client_x509_cert_url = os.environ.get('SHEETS_CREDENTIALS_CLIENT_X509_CERT_URL')


class SheetsBillingSpreadsheet:

    def __init__(self):
        self.id = os.environ.get('SHEETS_BILLING_SPREADSHEET_ID')
        self.sheet_id = os.environ.get('SHEETS_BILLING_SPREADSHEET_SHEET_ID')
        self.data_start_column = os.environ.get('SHEETS_BILLING_SPREADSHEET_DATA_START_COLUMN')
        self.data_exclusive_end_column = os.environ.get('SHEETS_BILLING_SPREADSHEET_DATA_EXCLUSIVE_END_COLUMN')


class Sheets:

    def __init__(self):
        self.credentials = SheetsCredentials()
        self.billing_spreadsheet = SheetsBillingSpreadsheet()
