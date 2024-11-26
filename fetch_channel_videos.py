import requests
import pandas as pd

API_KEY = "" # Your YouTube Data API v3 Key
CHANNEL_ID = "" # Target channel ID

# Get channel's "uploads" playlist ID
def get_uploads_playlist_id():
	url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_ID}&key={API_KEY}"
	response = requests.get(url).json()
	return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

# Get all the videos in the playlist (Including Shorts)
def get_playlist_videos(playlist_id):
	videos = []
	next_page_token = None

	while True:
		url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={playlist_id}&maxResults=50&pageToken={next_page_token or ''}&key={API_KEY}"
		response = requests.get(url).json()
		for item in response['items']:
			videos.append({
				'title': item['snippet']['title'],
				'video_id': item['contentDetails']['videoId'],
				'published_at': item['snippet']['publishedAt']
			})
		next_page_token = response.get('nextPageToken')
		if not next_page_token:
			break
	return videos

# Get views of each video
def get_video_stats(videos):
	for video in videos:
		url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet&id={video['video_id']}&key={API_KEY}"
		response = requests.get(url).json()
		stats = response['items'][0]['statistics']
		video['views'] = int(stats['viewCount'])
		video['likes'] = int(stats.get('likeCount', 0))
		video['is_short'] = "Shorts" if response['items'][0]['snippet']['categoryId'] == "23" else "Regular"
	return videos

# Save into Excel
def save_to_excel(videos):
	df = pd.DataFrame(videos)
	df = df.sort_values(by='views', ascending=False)  # Order by Views
	df.to_excel("youtube_videos_sorted.xlsx", index=False, engine='openpyxl')
	print("數據已保存到 youtube_videos_sorted.xlsx")

# Main function
if __name__ == "__main__":
	playlist_id = get_uploads_playlist_id()
	videos = get_playlist_videos(playlist_id)
	videos_with_stats = get_video_stats(videos)
	save_to_excel(videos_with_stats)
