from googleapiclient.discovery import build
import pandas as pd
import re
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# ---------------------------
# LOAD ENV VARIABLES
# ---------------------------
load_dotenv()  # Loads .env file

API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not API_KEY or not CHANNEL_ID:
    raise ValueError("Missing YOUTUBE_API_KEY or CHANNEL_ID in environment")

# ---------------------------
# CONFIG
# ---------------------------
MAX_VIDEOS = 100
MAX_COMMENTS_PER_VIDEO = 300
KIDS = ["Leland", "Leanna", "London"]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
CURRENT_CSV = os.path.join(BASE_PATH, "kid_current.csv")
CURRENT_JSON = os.path.join(BASE_PATH, "kid_current.json")
HISTORY_CSV = os.path.join(BASE_PATH, "kid_history.csv")

# ---------------------------
# LOGGING SETUP
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# INIT YOUTUBE API
# ---------------------------
youtube = build("youtube", "v3", developerKey=API_KEY)

# ---------------------------
# FETCH VIDEOS
# ---------------------------
def get_videos():
    logging.info("Fetching videos...")
    video_ids = []
    next_page_token = None

    while len(video_ids) < MAX_VIDEOS:
        request = youtube.search().list(
            part="id",
            channelId=CHANNEL_ID,
            maxResults=50,
            order="date",
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            video_ids.append(item["id"]["videoId"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    logging.info(f"Found {len(video_ids)} videos")
    return video_ids[:MAX_VIDEOS]

# ---------------------------
# FETCH COMMENTS + COUNT
# ---------------------------
def analyze_comments(video_ids):
    logging.info("Analyzing comments...")
    counts = {kid: 0 for kid in KIDS}
    total_mentions = 0
    seen_comments = set()

    for vid in video_ids:
        next_page_token = None
        fetched = 0

        while fetched < MAX_COMMENTS_PER_VIDEO:
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=vid,
                    maxResults=100,
                    pageToken=next_page_token,
                    textFormat="plainText"
                )
                response = request.execute()
                items = response.get("items", [])
                if not items:
                    break

                for item in items:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"].lower()
                    if comment in seen_comments:
                        continue
                    seen_comments.add(comment)
                    fetched += 1

                    # Clean comment and count mentions
                    comment_clean = re.sub(r"[^\w\s]", "", comment)
                    for kid in KIDS:
                        if re.search(rf"\b{re.escape(kid.lower())}\b", comment_clean):
                            counts[kid] += 1
                            total_mentions += 1
                            break

                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break

            except Exception as e:
                logging.warning(f"Error fetching comments for video {vid}: {e}")
                break

    logging.info("Comment analysis complete")
    return counts, total_mentions

# ---------------------------
# SAVE CURRENT SNAPSHOT
# ---------------------------
def save_current(counts, total_mentions):
    logging.info("Saving current snapshot...")
    data = []

    for kid, count in counts.items():
        percent = (count / total_mentions * 100) if total_mentions > 0 else 0
        data.append({
            "Kid": kid,
            "Mentions": count,
            "Consensus %": round(percent, 2)
        })

    df = pd.DataFrame(data).sort_values(by="Consensus %", ascending=False)
    df.to_csv(CURRENT_CSV, index=False)
    df.to_json(CURRENT_JSON, orient="records", indent=4)
    logging.info(f"Saved current data to {CURRENT_CSV}")
    return df

# ---------------------------
# APPEND HISTORY
# ---------------------------
def append_history(df):
    logging.info("Updating history file...")
    today = datetime.now().strftime("%Y-%m-%d")
    df["Date"] = today

    if os.path.exists(HISTORY_CSV):
        history_df = pd.read_csv(HISTORY_CSV)
        history_df = pd.concat([history_df, df], ignore_index=True)
    else:
        history_df = df

    history_df.to_csv(HISTORY_CSV, index=False)
    logging.info("History updated")

# ---------------------------
# MAIN
# ---------------------------
def main():
    logging.info("Starting Kid Popularity Backend Engine")
    videos = get_videos()
    counts, total_mentions = analyze_comments(videos)
    df = save_current(counts, total_mentions)
    append_history(df)
    logging.info("Backend run complete")
    print("\nFinal Results:")
    print(df)

if __name__ == "__main__":
    main()