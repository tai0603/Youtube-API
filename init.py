import googleapiclient.discovery

# Initialize YouTube API Service
api_service_name = "youtube"
api_version = "v3"
api_key = "YOUR_API_KEY"

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
