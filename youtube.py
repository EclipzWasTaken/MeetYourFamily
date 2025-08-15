import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Step 1: Authenticate and get credentials
def get_authenticated_service():
    credentials = None
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

# Step 2: Upload function
def upload_video(file_path, title, description, category_id="22", privacy_status="private"):
    youtube = get_authenticated_service()

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print("Upload complete! Video ID:", response["id"])

# Step 3: Use the function
if __name__ == "__main__":
    upload_video("MeetYourFamily.mp4", "Say Hello to Your New Celebrity Family 😎✨ (You’ve Been Adopted)", 
                 "Ever wonder what it’s like to have famous parents, iconic siblings, and a drama-packed group chat? Well, " \
                 "guess what... you’re in the family now. Let’s meet your celebrity relatives — and yes, one of them definitely cries at award shows."
                 "#YourFamousFamily #CelebrityDNA #WelcomeToTheClique", privacy_status="public")
