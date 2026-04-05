import sys
from src.logger import logger

def error_message_detail(error, error_details) -> str:
    """
    Build a detailed error message including file name, line number, and the error.
    """

    _, _, exc_tb = error_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Exception in [{file_name}] at line [{line_number}]: {error}"

class CustomException(Exception):
    """
    Custom exception class that automatically logs errors
    with detailed messages and full traceback.
    """

    def __init__(self, error_message, error_details):
        self.error_message = error_message_detail(error_message, error_details)
        # Initialize parent Exception
        super().__init__(self.error_message)

        logger.error(f"{self.error_message}", exc_info=True)