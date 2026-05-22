import sys

from pathlib import Path

from src.logger import logger


def error_message_detail(error, error_details) -> str:
    """
    Create a detailed error message including
    file name, line number, and original error.
    """

    _, _, exc_tb = error_details.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = Path(
        exc_tb.tb_frame.f_code.co_filename
    ).name

    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in script: [{file_name}] "
        f"at line number: [{line_number}] "
        f"Error: [{str(error)}]"
    )

    return error_message


class CustomException(Exception):
    """
    Custom exception class for application-level error handling.
    """

    def __init__(self, error_message, error_details):

        self.error_message = error_message_detail(
            error_message,
            error_details
        )

        super().__init__(self.error_message)

        # Log full traceback
        logger.error(
            self.error_message,
            exc_info=True
        )

    def __str__(self):
        return self.error_message