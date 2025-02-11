# logger_setup.py
import logging

# Configure the root logger to log only to the console
logging.basicConfig(
    level=logging.DEBUG,  # Set your desired level (DEBUG, INFO, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Only logs to the console
)

# Optionally, you can create a convenience logger:
logger = logging.getLogger(__name__)