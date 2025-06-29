import os
import tempfile
from google.cloud import storage
from config import GCS_BUCKET_NAME, PROJECT_ID, STATE_FILE


def init_storage_client():
    """
    Initializes the GCS client using the specified PROJECT_ID.
    """
    return storage.Client(project=PROJECT_ID)


def list_video_blobs():
    """
    Returns a list of video blobs from GCS that have one of the valid extensions: .mp4, .mov, or .avi.
    """
    client = init_storage_client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    valid_exts = (".mp4", ".mov", ".avi")
    return [
        blob for blob in bucket.list_blobs() if blob.name.lower().endswith(valid_exts)
    ]


def download_blob_to_local(blob):
    """
    Downloads the video file to the system's temporary directory and returns the full local path.
    This method uses tempfile.gettempdir() for cross-platform compatibility.
    """
    temp_dir = (
        tempfile.gettempdir()
    )  # e.g., on Windows: C:\Users\username\AppData\Local\Temp
    local_path = os.path.join(temp_dir, os.path.basename(blob.name))
    blob.download_to_filename(local_path)
    return local_path


def load_state():
    """
    Loads the state from STATE_FILE (if it exists) and returns the content as a Python dictionary.
    """
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        import json

        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    """
    Saves the provided state dictionary to STATE_FILE in JSON format.
    """
    import json

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def mark_as_uploaded(state, blob_name, video_id):
    """
    Marks a blob (video file) as uploaded in the state dictionary,
    storing the video_id and the current timestamp.
    Then saves the updated state.
    """
    import datetime

    state[blob_name] = {
        "uploaded": True,
        "video_id": video_id,
        "uploaded_at": datetime.datetime.now().isoformat(),
    }
    save_state(state)


def is_already_uploaded(state, blob_name):
    """
    Returns True if the given blob_name is already marked as uploaded (in the state),
    False otherwise.
    """
    return state.get(blob_name, {}).get("uploaded")
