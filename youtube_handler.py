# youtube_handler.py
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import YOUTUBE_CREDENTIALS_FILE


def init_youtube_client():
    """
    טוען אישורי OAuth (מהקובץ 'token.json') ויוצר אובייקט YouTube באמצעות googleapiclient.
    """
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = Credentials.from_authorized_user_file(YOUTUBE_CREDENTIALS_FILE, scopes)
    youtube = build("youtube", "v3", credentials=creds)
    return youtube


def upload_short(youtube, local_video_path, title, description, tags):
    """
    מעלה סרטון (local_video_path) כ-Short (סרטון קצר) כך שהוא יתפרסם מיד כציבורי.

    בהעלאה זו:
      - מוגדר status עם "privacyStatus": "public", כך שהסרטון יהיה גלוי לכל באופן מיידי.
      - שדה 'publishAt' לא נכלל, ולכן אין תזמון להופעת הסרטון.

    הפונקציה מחזירה את ה-video_id במקרה של הצלחה, או None אם ההעלאה נכשלה.
    """
    # הגדרת נתוני ה-snippet של הסרטון
    snippet = {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": "22",  # למשל, People & Blogs
    }

    # הגדרת הסטטוס כך שהסרטון יהיה ציבורי מיד
    status = {
        "privacyStatus": "public",  # הסרטון יהיה ציבורי באופן מיידי
        "selfDeclaredMadeForKids": False,
        # אין שדה publishAt – הסרטון לא מתוזמן
    }

    # יצירת גוף הבקשה להעלאת הסרטון
    request_body = {
        "snippet": snippet,
        "status": status,
    }

    # עוטף את קובץ הווידאו לשידור
    media = MediaFileUpload(local_video_path, chunksize=-1, resumable=True)

    # יוצר את הבקשה להעלאת הסרטון
    request = youtube.videos().insert(
        part="snippet,status", body=request_body, media_body=media
    )
    try:
        response = request.execute()
        return response.get("id")
    except Exception as e:
        print(f"Error uploading video: {e}")
        return None
