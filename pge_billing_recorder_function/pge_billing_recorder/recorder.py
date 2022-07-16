import datetime
from decimal import Decimal

from .configuration import Sheets
from sheets import SheetsApi


class Recorder:

    def __init__(self, config: Sheets):
        self.config = config

    def record(
        self,
        billing_cycle_day: int,
        number_of_billing_days: int,
        last_read_date: str,
        bill_to_date_amount: Decimal,
        projected_amount: Decimal,
        min_projected_amount: Decimal,
        max_projected_amount: Decimal,
        billing_progress: int,
        last_payment_amount: Decimal,
        total_current_charges: Decimal,
        kwh: int,
        bill_date: str,
        due_date: str,
        billing_period_start_date: str,
        billing_period_end_date: str
    ):
        sheets_api = SheetsApi(vars(self.config.credentials))
        billing_spreadsheet = self.config.billing_spreadsheet

        existing_billing_data = sheets_api.read_from_sheet(
            billing_spreadsheet.id,
            {
                'grid_range': {
                    'sheet_id': billing_spreadsheet.sheet_id,
                    'start_row_index': 0,
                    'end_row_index': 999999,
                    'start_column_index': billing_spreadsheet.data_start_column,
                    'end_column_index': billing_spreadsheet.data_exclusive_end_column
                }
            }
        )
        values = existing_billing_data[0]['valueRange']['values']
        next_row_to_write = len(values)
        last_recorded_billing_data = values[-1]
        print(f'Last billing data entry found on row {next_row_to_write}: {last_recorded_billing_data}')

        # Record the billing data, adding the following data
        # Timestamp, Billing Cycle Day, Number of Billing Days, Last Read Date, Bill to Date Amount
        # Projected Amount, Min Projected Amount, Max Projected Amount, Billing Progress,
        # Last Amt, Current Amt, Current kWh Total, Issue Date, Due Date, Period Start, Period End
        timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
        sheets_api.write_to_sheet(
            billing_spreadsheet.id,
            {
                'data_filter': {
                    'grid_range': {
                        'sheet_id': billing_spreadsheet.sheet_id,
                        'start_row_index': next_row_to_write,
                        'end_row_index': next_row_to_write + 1,
                        'start_column_index': billing_spreadsheet.data_start_column,
                        'end_column_index': billing_spreadsheet.data_exclusive_end_column
                    }
                },
                'major_dimension': 'ROWS',
                'values': [
                    [
                        timestamp, 
                        billing_cycle_day, 
                        number_of_billing_days, 
                        last_read_date, 
                        str(bill_to_date_amount),
                        str(projected_amount), 
                        str(min_projected_amount), 
                        str(max_projected_amount), 
                        billing_progress,
                        str(last_payment_amount),
                        str(total_current_charges),
                        kwh,
                        bill_date,
                        due_date,
                        billing_period_start_date,
                        billing_period_end_date
                    ]
                ]
            }
        )
        print('Billing data recording completed')
