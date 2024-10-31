import requests
import json
import os
from urllib.parse import urlparse
from vars import *
import logging

#declare some variables before populating them


# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#for events images function
event_json_file = './data/events_info.json'
event_dl_directory = './data/attach/event/covers/'

#Events cover pics
def download_event_images(event_json_file, event_dl_directory):
    if not os.path.exists(event_json_file):
        return
    # Create the directory if it doesn't exist
    if not os.path.exists(event_dl_directory):
        os.makedirs(event_dl_directory)

    # Load the JSON data from the file
    with open(event_json_file, 'r') as f:
        data = json.load(f)

    # Iterate through each event in the 'events' key
    for event in data.get('events', []):
        event_id = event.get('id')
        cover_url = event.get('cover', {}).get('source')


        # Download the cover photo if it exists
        if cover_url:
            cover_filename = os.path.join(event_dl_directory, f"{event_id}_cover.jpg")
            try:
                response = requests.get(cover_url)
                with open(cover_filename, 'wb') as cover_file:
                    cover_file.write(response.content)
                print(f"Downloaded cover photo for event {event_id}")
            except Exception as e:
                print(f"Error downloading cover photo for event {event_id}: {e}")
                
#Groups main cover pic and icon
json_file = './data/groups_info.json'
download_directory = './data/attach/group/covers/'

def download_group_images(json_file, download_directory):
    if not os.path.exists(json_file): 
        return  # Return early if the data is not valid or key is missing
    
    # Create the directory if it doesn't exist
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Load the JSON data from the file
    if os.path.exists(json_file): 
        with open(json_file, 'r') as f:
            data = json.load(f)

    # Iterate through each group in the 'groups' key
    for group in data.get('groups', []):
        group_id = group.get('id')
        cover_url = group.get('cover', {}).get('source')
        icon_url = group.get('icon')

        # Download the cover photo if it exists
        if cover_url:
            cover_filename = os.path.join(download_directory, f"{group_id}_cover.jpg")
            try:
                response = requests.get(cover_url)
                with open(cover_filename, 'wb') as cover_file:
                    cover_file.write(response.content)
                print(f"Downloaded cover photo for group {group_id}")
            except Exception as e:
                print(f"Error downloading cover photo for group {group_id}: {e}")

        # Download the icon if it exists
        if icon_url:
            icon_filename = os.path.join(download_directory, f"{group_id}_icon.png")
            try:
                response = requests.get(icon_url)
                with open(icon_filename, 'wb') as icon_file:
                    icon_file.write(response.content)
                print(f"Downloaded icon for group {group_id}")
            except Exception as e:
                print(f"Error downloading icon for group {group_id}: {e}")

# Example usage:



#Member Main Profile pics

#for below function
json_file_path = "./data/members_info.json"  # Path to your JSON file
save_directory = "./data/attach/profiles/"  # Directory where you want to save the images

def download_member_pictures_from_file(json_file_path, save_directory):
    # Read JSON data from file
    if not os.path.exists(json_file_path):
        
        return
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    
    # Assuming your file has a "members" key that holds a list of members
    members = data.get("members", [])

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for member in members:
        member_id = member.get('id')
        picture_data = member.get('picture', {}).get('data', {})

    #if not picture_data.get('is_silhouette', True):  # Check if it's a real picture, not a silhouette
        picture_url = picture_data.get('url')
        
        if picture_url:
            # Get the image content
            try:
                response = requests.get(picture_url, stream=True)
                if response.status_code == 200:
                    # Define the file path (using member_id as the filename)
                    file_extension = picture_url.split('.')[-1].split('?')[0]  # Get file extension
                    file_path = os.path.join(save_directory, f"{member_id}.jpg")
                    
                    # Save the image to the specified file path
                    with open(file_path, 'wb') as image_file:
                        for chunk in response.iter_content(1024):
                            image_file.write(chunk)
                    
                    print(f"Downloaded profile picture for member {member_id}.")
                else:
                    print(f"Failed to download picture for member {member_id}. HTTP Status Code: {response.status_code}")
            except Exception as e:
                print(f"Error downloading picture for member {member_id}: {e}")
    #else:
        #print(f"Member {member_id} has a silhouette or no picture.")

# Example usage


#For below function:

if os.path.exists('./data/member_posts.json'):
    with open('./data/member_posts.json', 'r') as f:
        json_data = json.load(f)


if os.path.exists('./data/group_posts.json'):    
    with open('./data/group_posts.json', 'r') as f:
        json_data_groups = json.load(f)

folder_path_m_posts = r'./data/attach/m_posts'
folder_path_g_posts = r'./data/attach/g_posts'

#POSTS images#
def download_media(json_data, folder_path, posts_key):
    base_url = "https://scontent.fsyd3-1.fna.fbcdn.net/v/t39.30808-6/"
    
    if not json_data:
        return  # Return early if the data is not valid or key is missing

    posts = json_data.get(posts_key, [])
    
    
    for item in posts:      
        if 'subject_id' in item:
            post_id = item['subject_id']

            # Process the media in the main post
            if 'media' in item:
                media_src = item['media'].get('image', {}).get('src')
                if media_src:
                    download_file(media_src, post_id, base_url, folder_path, main=True)
                else:
                    print(f"'image' not found in media for subject_id: {post_id}")
                                   
            # Process the video in the main post (at the same level as media)
            # DEBUG: Print the type of the item to check for videos
            '''
            item_type = item.get('type')
            if item.get('type') == 'video':
                media = item.get('media')  # Retrieve media; this can be None
                if isinstance(media, dict) and 'source' in media:
                    video_source = media['source']
                    print(f"Video source URL: {video_source}")
                    # Proceed with your download function
                    download_file(video_source, post_id, base_url, folder_path)  # Modify as per your download logic
                else:
                    print(f"No video source found for subject_id: {item.get('subject_id')}")
            '''
            # Process subattachments if they exist
            if 'subattachments' in item:
                for sub in item['subattachments']['data']:
                    # Ensure 'media' exists in the subattachment before accessing
                    if 'media' in sub:
                        media_src = sub['media'].get('image', {}).get('src')
                        media_vsrc = sub['media'].get('source')
                        if media_src:
                            download_file(media_src, post_id, base_url, folder_path)
                        if media_vsrc:
                            download_file(media_vsrc, post_id, base_url, folder_path)                            

                        # Check for video or other file types if needed
                        media_src = sub['media'].get('video', {}).get('src')
                        if media_src:
                            download_file(media_src, post_id, base_url, folder_path)
                        media_src2 = sub['media'].get('video', {}).get('source')
                        if media_src2:
                            download_file(media_src2, post_id, base_url, folder_path)                            
        else:
            print("Post item is missing a 'subject_id':", item)


def download_file(media_url, post_id, base_url, folder_path, main=False, file_name=None):
    if base_url in media_url:
        start_index = media_url.index(base_url) + len(base_url)
        end_index = media_url.index('?') if '?' in media_url else len(media_url)

        # Use the provided file_name if given, otherwise construct it
        if file_name is None:
            file_name = f"{post_id}_{media_url[start_index:end_index]}"

        # Ensure the file has a valid extension
        if not os.path.splitext(file_name)[1]:
            file_name += '.jpg'  # Default to .jpg if no extension

        # Append "_main" before the file extension if it's the main media file
        if main:
            name, ext = os.path.splitext(file_name)  # Split into name and extension
            file_name = f"{name}_main{ext}"  # Reconstruct with "_main" before the extension

        # Check for folder existence and create if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the directory
            
        # Combine folder path with filename
        full_path = os.path.join(folder_path, file_name)
        
        if os.path.exists(full_path):
            print(f"You've already got this file saved, skipping: {full_path}")
            return  # Skip downloading
            
        # Download the file
        response = requests.get(media_url)
        if response.status_code == 200:
            with open(full_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {full_path}")
        else:
            print(f"Failed to download {media_url}")



if os.path.exists('./data/member_convos.json'):
    with open('./data/member_convos.json', 'r') as f:
        json_data_convos = json.load(f)



def save_media_from_conversations(json_data, save_directory="./data/attach/convo_media/"):
    
    # Create the save directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    if not os.path.exists('./data/member_convos.json'):
        return  # Return early if the data is not valid or key is missing    

    logger.info("Starting to process conversations...")  # Using logger for consistency
    for conversation in json_data.get("member_convos", []):
        conversation_id = conversation.get("id")
        logger.info(f"Processing conversation ID: {conversation_id}")
        
        # Loop through each message in the conversation
        for message in conversation.get("messages", {}).get("data", []):
            message_id = message.get("id")
            logger.info(f"  Processing message ID: {message_id}")
            
            # Check for media URLs in 'attachments' or other possible keys where URLs are stored
            attachments = message.get("attachments", {}).get("data", [])

            for attachment in attachments:
                logger.debug(f"Attempting to download media for message ID: {message_id}")
                
                # Collect URLs from possible keys in the attachment
                url = attachment.get("url") or attachment.get("preview_url") or attachment.get("image_data", {}).get("url")
                
                if url:
                    logger.debug(f"Found media URL: {url} for message ID: {message_id}")
                else:
                    logger.debug(f"No media URL found for message ID: {message_id}")
                    continue  # Skip this iteration if no URL is found
                
                if url:
                    # Extract unique identifier from the URL for naming
                    url_path = urlparse(url).path
                    url_identifier = url_path.split("/")[-1].split("?")[0]

                    # Get the original file extension from the URL path
                    original_extension = url_identifier.split('.')[-1].lower() if '.' in url_identifier else None

                    # Construct filename
                    filename = f"{conversation_id}_{message_id}_{url_identifier}"


                    file_path = os.path.join(save_directory, filename)

                    # Check if file already exists
                    if os.path.exists(file_path):
                        logger.info(f"    File already exists: {filename}, skipping download.")
                        continue
                    
                    # Download and save the file
                    try:
                        logger.info(f"    Downloading from {url}...")
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            with open(file_path, 'wb') as f:
                                for chunk in response.iter_content(1024):
                                    f.write(chunk)
                            logger.info(f"    Saved {filename}")
                        else:
                            logger.warning(f"    Failed to download {url} - Status Code: {response.status_code}")
                    except requests.RequestException as e:
                        logger.error(f"    Error downloading {url}: {e}")

    logger.info("Finished processing conversations.")





