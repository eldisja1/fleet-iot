import time
from sqlalchemy.exc import OperationalError


def retry_db_operation(operation, max_retries=5, base_delay=1):
    """
    Retry database operation with exponential backoff.
    Only retries for OperationalError.
    """

    for attempt in range(1, max_retries + 1):
        try:
            return operation()
        except OperationalError as e:
            if attempt == max_retries:
                raise

            sleep_time = base_delay * (2 ** (attempt - 1))
            time.sleep(sleep_time)