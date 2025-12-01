import requests

# Your Discogs token
TOKEN = "msAmudCGRYzQRTnDCdeIPrLVqFuvKSnqBUsEogOj"

# Test with one of your albums
artist = "Radiohead"
album = "OK Computer"

# Search for the release
search_url = f"https://api.discogs.com/database/search"
params = {
    'q': f'{artist} {album}',
    'type': 'release',
    'format': 'CD',
    'token': TOKEN
}

print(f"Searching for: {artist} - {album}\n")
response = requests.get(search_url, params=params)

if response.status_code == 200:
    data = response.json()
    results = data.get('results', [])
    
    if results:
        # Get the first result
        first_result = results[0]
        print(f"Found: {first_result.get('title')}")
        print(f"Year: {first_result.get('year')}")
        print(f"Label: {', '.join(first_result.get('label', []))}")
        print(f"Format: {', '.join(first_result.get('format', []))}")
        print(f"Resource URL: {first_result.get('resource_url')}\n")
        
        # Fetch detailed info
        detail_url = first_result.get('resource_url')
        detail_response = requests.get(detail_url, params={'token': TOKEN})
        
        if detail_response.status_code == 200:
            detail_data = detail_response.json()
            
            print("=== TRACKLIST ===")
            tracklist = detail_data.get('tracklist', [])
            for track in tracklist:
                position = track.get('position', '')
                title = track.get('title', '')
                duration = track.get('duration', 'N/A')
                print(f"{position}. {title} - {duration}")
            
            print("\n=== ARTISTS ===")
            artists = detail_data.get('artists', [])
            for artist in artists:
                print(f"- {artist.get('name')}")
            
            print("\n=== OTHER DATA AVAILABLE ===")
            print(f"Genres: {', '.join(detail_data.get('genres', []))}")
            print(f"Styles: {', '.join(detail_data.get('styles', []))}")
            print(f"Country: {detail_data.get('country', 'N/A')}")
            print(f"Released: {detail_data.get('released', 'N/A')}")
            print(f"Notes: {detail_data.get('notes', 'N/A')[:100]}...")
            
            # Check for images
            images = detail_data.get('images', [])
            if images:
                print(f"\nCover images available: {len(images)}")
                print(f"Primary image: {images[0].get('uri')}")
        else:
            print(f"Error fetching details: {detail_response.status_code}")
    else:
        print("No results found")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
