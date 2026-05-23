from pathlib import Path
from typing import Any

from shared.logger import logger


def error_message_detail(error: Exception, error_details: Any) -> str:
    """
    Create detailed error message with
    filename, line number, and error details.
    """

    _, _, exc_tb = error_details.exc_info()

    if exc_tb is None:
        return str(error)

    file_name = Path(exc_tb.tb_frame.f_code.co_filename).name

    line_number = exc_tb.tb_lineno

    return f"Error in [{file_name}] " f"line [{line_number}] " f": {str(error)}"


class CustomException(Exception):
    """
    Custom exception class for centralized
    application error handling.
    """

    def __init__(self, error_message: Exception, error_details: Any) -> None:

        self.error_message = error_message_detail(error_message, error_details)

        logger.error(self.error_message, exc_info=True)

        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message
