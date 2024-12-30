import requests
import time
import random
import logging
from datetime import datetime
from notifier.notifier import send_email, send_telegram

def is_valid_date(date_string):
    """Check if the date string is a valid date."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def check_appointment(location_id, program, limit, start_date=None, end_date=None):
    """Check for available appointments for the specified location and program."""

    # Validate start_date
    if start_date and is_valid_date(start_date):
        if not end_date or not is_valid_date(end_date):
            end_date = start_date

        # Construct URL for a specific date range
        url = f"https://ttp.cbp.dhs.gov/schedulerapi/locations/{location_id}/slots"
        url += f"?startTimestamp={start_date}T00:00:00&endTimestamp={end_date}T23:59:59"
        logging.debug(f"Requesting URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            # Filter slots where "active" is 1
            return [slot["timestamp"] for slot in response.json() if slot.get("active") == 1]
        
    else:
        # Default URL for soonset slots
        url = f"https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit={limit}&locationId={location_id}"
        logging.debug(f"Requesting URL: {url}")

        response = requests.get(url)
        if response.status_code == 200:
            # Return startTimestamps for active slots
            return [slot["startTimestamp"] for slot in response.json() if slot.get("active")]
    
    # Return an empty list if no results
    return []

def monitor_appointments(config):
    """Monitor appointments for specified locations and programs."""
    logging.info("Starting appointment monitoring...")    
    programs = config["programs"]
    locations = config["locations"]
    check_interval = config["check_interval"]
    notifications = config["notifications"]
    limit = config.get("limit", 1)
    start_date = config.get("start_date")
    end_date = config.get("end_date")

    # Print configuration
    configuration = f"""
======= Configuration =======
Configuration:
Programs: {programs}
Locations: {locations}
Check Interval: {check_interval}
Notifications: {notifications}
Limit: {limit}
Start Date: {start_date}
End Date: {end_date}
============================
"""
    logging.info(configuration)

    while True:
        messages = []
        for program in programs:
            for location_id in locations.get(program, []):
                slots = check_appointment(location_id, program, limit, start_date, end_date)
                if slots:
                    message = f"\n*** [{program.upper()}] Available slots at {location_id}:"
                    messages.append(message)
                    message_length = len(message)
                    for index, slot in enumerate(slots, start=1):
                        message = (
                            f"{index}. {slot}"
                        )
                        messages.append(message)

                else:
                    logging.info(f"No available slots for {program.upper()} at location {location_id}.")

        # If there are available slots, Print all available slots
        if messages:
            logging.info("\n".join(messages))

            # Send notifications only if there are available slots
            notification_message = "\n".join(messages)
            if notifications.get("email") and notification_message:
                send_email(f"Appointment Found", notification_message),
            if notifications.get("telegram") and notification_message:
                send_telegram(notification_message)

        time.sleep(random.randint(*check_interval))