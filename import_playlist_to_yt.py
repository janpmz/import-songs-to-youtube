from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# HOW TO:
# Songs to import are in songs.txt in the format <interpret> - <songtitle>
# Install claude-cli and open it in the folder of your MP3 player.
# Then ask claude to find all songs in all folders and create a file "songs.txt" with the songtitles in the format <interpret> - <songtitle> (without file path).
# Tell it to do its best to figure out the correct interpret and title.

# OAuth scope: full YouTube account access
SCOPES = ["https://www.googleapis.com/auth/youtube"]

def main():
    # 1. Login & authenticate
    flow = InstalledAppFlow.from_client_secrets_file("client_secret_336269071909-stpgj3tkdqg2odp1ovvhfipovbgo68tg.apps.googleusercontent.com.json", SCOPES)
    creds = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=creds)

    # 2. Create a new playlist
    playlist_title = "Imported Playlist"
    playlist = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_title,
                "description": "Imported from songs.txt"
            },
            "status": {"privacyStatus": "private"}
        }
    ).execute()

    playlist_id = playlist["id"]
    print(f"Created playlist: {playlist_title} ({playlist_id})")

    # 3. Read songs from file
    with open("songs.txt", "r", encoding="utf-8") as f:
        songs = [line.strip() for line in f if line.strip()]

    # 4. Search and add each song
    for song in songs:
        search = youtube.search().list(
            part="snippet",
            q=song,
            maxResults=1,
            type="video"
        ).execute()

        if search["items"]:
            video_id = search["items"][0]["id"]["videoId"]
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print(f"Added: {song}")
        else:
            print(f"No results for: {song}")

if __name__ == "__main__":
    main()
