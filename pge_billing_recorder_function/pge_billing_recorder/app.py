import os

from .configuration import Configuration
from portlandgeneral import PortlandGeneralApi
from .recorder import Recorder


def lambda_handler(event, context):
    """Lambda function reacting to EventBridge events

    Parameters
    ----------
    event: dict, required
        Event Bridge Scheduled Events Format

        Event doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html#schedule-event-type

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    """

    dry_run = os.environ.get('RUN_MODE') == 'test'
    print(f'Running in {"dry run" if dry_run else "production"} mode')

    config = Configuration()
    pge_api = PortlandGeneralApi()
    pge_api.login(config.pge.username, config.pge.password)

    info = pge_api.get_account_info()
    account_numbers = [group.default_account.account_number for group in info.groups]
    first_account_number = account_numbers[0]

    details = pge_api.get_account_details(first_account_number, info.encrypted_person_id)
    first_account_detail = details[0]

    tracker = pge_api.get_energy_tracker_info(
        first_account_detail.encrypted_account_number,
        first_account_detail.encrypted_person_id
    )

    print('Recording billing data')
    recorder = Recorder(config.sheets)
    recorder.record(
        tracker.details.billing_cycle_day,
        tracker.details.number_of_billing_days,
        tracker.details.last_read_date,
        tracker.details.bill_to_date_amount,
        tracker.details.projected_amount,
        tracker.details.min_projected_amount,
        tracker.details.max_projected_amount,
        tracker.details.billing_progress,
        first_account_detail.bill_info.last_payment_amount,
        first_account_detail.bill_info.bill_details.total_current_charges,
        first_account_detail.bill_info.bill_details.kwh,
        first_account_detail.bill_info.bill_details.bill_date,
        first_account_detail.bill_info.bill_details.due_date,
        first_account_detail.bill_info.bill_details.billing_period_start_date,
        first_account_detail.bill_info.bill_details.billing_period_end_date
    )

    # We got here successfully!
    return True
