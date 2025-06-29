# main.py
import os
import random
import logging
import schedule
import time

from config import VIDEOS_TO_UPLOAD_PER_RUN
from gcs_handler import (
    list_video_blobs,
    download_blob_to_local,
    load_state,
    is_already_uploaded,
    mark_as_uploaded,
)
from openai_handler import generate_metadata_for_short
from youtube_handler import init_youtube_client, upload_short

# Create a 'logs' folder if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
logging.basicConfig(
    filename="logs/main.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)


def post_shorts():
    """
    Main routine to:
    1) Load state.json.
    2) Initialize the YouTube client.
    3) Fetch and shuffle a list of blobs (video files) from GCS.
    4) Attempt to upload up to VIDEOS_TO_UPLOAD_PER_RUN items.
    5) For each video:
       - Download locally
       - Generate a title, description, and tags using GPT
       - Upload to YouTube
       - Update state
       - Remove the local file
    """
    logging.info("Starting post_shorts routine...")
    state = load_state()
    youtube = init_youtube_client()

    blobs = list_video_blobs()
    random.shuffle(blobs)

    count_uploaded = 0
    for blob in blobs:
        if count_uploaded >= VIDEOS_TO_UPLOAD_PER_RUN:
            break

        blob_name = blob.name
        if is_already_uploaded(state, blob_name):
            # Already uploaded
            continue

        local_path = download_blob_to_local(blob)
        file_base = os.path.splitext(os.path.basename(blob_name))[0]

        # Generate metadata: title, description, tags
        title, description, tags = generate_metadata_for_short(file_base)

        # Upload to YouTube
        video_id = upload_short(youtube, local_path, title, description, tags)
        if video_id:
            mark_as_uploaded(state, blob_name, video_id)
            logging.info(f"Uploaded {blob_name} => video_id={video_id}")
            count_uploaded += 1
        else:
            logging.warning(f"Failed to upload {blob_name}")

        # Remove local file
        if os.path.exists(local_path):
            os.remove(local_path)

    if count_uploaded == 0:
        logging.info("No new videos to upload.")
    else:
        logging.info(f"Uploaded {count_uploaded} new Shorts.")


def run_scheduled():
    """
    This function is called by schedule at specific times.
    It simply calls post_shorts().
    """
    logging.info("Running scheduled tasks...")
    post_shorts()


def main():
    """
    Main entry point:
    1) Schedules the run_scheduled() to happen every day at 10:00.
    2) Immediately runs post_shorts() once.
    3) Enters an infinite loop where schedule runs pending tasks every 30s.
    """
    logging.info("Starting main...")

    # Example: run daily at 10:00
    schedule.every().day.at("10:00").do(run_scheduled)

    # Run once immediately
    post_shorts()

    # Keep running to catch scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
