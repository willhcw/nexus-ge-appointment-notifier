import json
import logging
from notifier.monitor import monitor_appointments

# Set up logging
debug_enabled = False

if debug_enabled:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(), # Log to console
            logging.FileHandler("appointment_debug.log", mode="w") # Log to file
        ]
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(), # Log to console
            logging.FileHandler("appointment.log", mode="w") # Log to file
        ]
    )

def load_config():
    """Load configuration from config.json file."""
    with open("config.json") as f:
        return json.load(f)
    
if __name__ == "__main__":
    logging.info("Application started.")
    config = load_config()
    monitor_appointments(config)