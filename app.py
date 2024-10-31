import subprocess
import os
import sys
import threading
import json
from datetime import datetime, timedelta
import signal

def install_requirements():
    packages = {
        'requests': 'requests',
        'yaml': 'pyyaml',
        'flask': 'Flask',
        'cryptography': 'cryptography'
    }

    for import_name, package_name in packages.items():
        try:
            __import__(import_name)
            print(f"{import_name} is already installed.")
        except ImportError:
            print(f"{import_name} is not installed. Installing...")
            try:
                subprocess.run(['pip', 'install', package_name], check=True)
                print(f"{package_name} installed successfully.")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package_name}. Please install it manually.")
                
#install prerequisites
install_requirements()
from generate_certs import generate_self_signed_cert

# Your main application logic goes here
print("Starting the application...")
from flask import Flask, jsonify, g
import yaml

from vars import edge_id_names, edge_keys


os.makedirs('./data', exist_ok=True)




# Generate SSL certificate if not already present
if not (os.path.exists("certs/cert.pem") and os.path.exists("certs/key.pem")):
    generate_self_signed_cert()

from functions import (
	fetch_data, fetch_and_save, fetch_data_base, get_ids, get_member_ids,
	get_members_info, get_groups_info, get_member_edges,
	get_group_edges, get_events_info, get_event_edges,
	get_survey_info, extract_edge_ids, extract_member_posts,
	extract_group_posts, extract_member_conversations
)

from photo_funcs import (download_media, download_file, download_member_pictures_from_file,
json_data, json_file_path, save_directory, download_group_images, json_file, download_directory,
download_event_images, event_json_file, event_dl_directory, folder_path_m_posts, folder_path_g_posts,
json_data_groups, json_data_convos, save_media_from_conversations
)

def signal_handler(sig, frame):
	print('You pressed Ctrl+C!')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#get returned values from imported functions
active_user_ids, inactive_user_ids = get_member_ids()
group_ids = get_ids('groups', 'base.json')
group_ids_filtered = get_ids('groups', 'groups_info.json')
event_ids = get_ids('events', 'base.json')
survey_ids = get_ids('surveys', 'base.json')
app = Flask(__name__)


# Function to load configuration from a YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load your configuration
config = load_config('config.yaml')

#you can do multiple at once, as long as their prerequisite data is downloaded first
#And as long as they are on the same level.

pause_base_data = config['levels']['level_1']['pause_base_data']
pause_member_data = config['levels']['level_2']['pause_member_data']
pause_group_data = config['levels']['level_2']['pause_group_data']
pause_event_data = config['levels']['level_2']['pause_event_data']
pause_survey_data = config['levels']['level_2']['pause_survey_data']
pause_edges_data = config['levels']['level_3']['pause_edges_data']
pause_group_edges_data = config['levels']['level_3']['pause_group_edges_data']
pause_event_edges_data = config['levels']['level_3']['pause_event_edges_data']
pause_member_convos_data = config['levels']['level_3']['pause_member_convos_data']
pause_member_posts_data = config['levels']['level_4']['pause_member_posts_data']
pause_group_posts_data = config['levels']['level_4']['pause_group_posts_data']
pause_profile_pic = config['levels']['media']['pause_profile_pic']
pause_group_covers = config['levels']['media']['pause_group_covers']
pause_event_covers = config['levels']['media']['pause_event_covers']
pause_media_members = config['levels']['media']['pause_media_members']
pause_media_groups = config['levels']['media']['pause_media_groups']
pause_convo_media = config['levels']['media']['pause_convo_media']


DATA_FILE = './data/base.json'
DATA_FILE_MEMBERS_INFO = "./data/members_info.json" 
DATA_FILE_GROUPS_INFO = "./data/groups_info.json"
DATA_FILE_EVENTS_INFO = "./data/events_info.json"
DATA_FILE_MEMBER_EDGES = "./data/member_edges.json"
DATA_FILE_GROUP_EDGES = "./data/group_edges.json"
DATA_FILE_EVENT_EDGES = "./data/event_edges.json"
DATA_FILE_SURVEY_INFO = "./data/survey_info.json"
DATA_FILE_MEMBER_POSTS = "./data/member_posts.json"
DATA_FILE_GROUP_POSTS = "./data/group_posts.json"
DATA_FILE_MEMBER_CONVOS = "./data/member_convos.json"


def fetch_base_data(pause_base_data):
	def fetch_and_save_data():
		data = {
			"active_users": fetch_data_base('active_users'),
			"inactive_users": fetch_data_base('inactive_users'),
			"groups": fetch_data_base('groups'),
			"events": fetch_data_base('events'),
			"surveys": fetch_data_base('surveys'),
			"badges": fetch_data_base('badges'),
			"skills": fetch_data_base('skills'),
			"knowledge_cats" : fetch_data_base('knowledge_cats'),
			"knowledge_links" : fetch_data_base('knowledge_links')
		}
		# Save fetched data to file
		with open(DATA_FILE, 'w') as f:
			json.dump(data, f)
		return data

	if pause_base_data == 0:  # Fetch new data
		return fetch_and_save_data()

	if os.path.exists(DATA_FILE):  # Load existing data
		with open(DATA_FILE, 'r') as f:
			return json.load(f)

	# If file doesn't exist, fetch new data
	return None

#Fetch Base Data
def fetch_member_data(pause_member_data):
	def fetch_and_save_data():
		members, dead_members = get_members_info(active_user_ids, inactive_user_ids)		
		data = {
			"members": members,
			"dead_members": dead_members
		}
		with open(DATA_FILE_MEMBERS_INFO, 'w') as f:
			json.dump(data, f)
		return data		   
		
	if pause_member_data == 0:
		return fetch_and_save_data()   
		
	if os.path.exists(DATA_FILE_MEMBERS_INFO):
		with open(DATA_FILE_MEMBERS_INFO, 'r') as f:
			data = json.load(f)
		return data
		
	return None

#Fetch Light Data
def fetch_group_data(pause_group_data):
    return fetch_data(pause_group_data, lambda: get_groups_info(group_ids), 'groups', DATA_FILE_GROUPS_INFO)
	
def fetch_event_data(pause_event_data):
	return fetch_data(pause_event_data, lambda: get_events_info(event_ids), 'events', DATA_FILE_EVENTS_INFO)

def fetch_survey_data(pause_survey_data):
	return fetch_data(pause_survey_data, lambda: get_survey_info(survey_ids), 'surveys', DATA_FILE_SURVEY_INFO)

#Fetch Intermediate Data	
def fetch_member_edges_data(pause_edges_data):
    return fetch_data(pause_edges_data, lambda: get_member_edges(active_user_ids, inactive_user_ids), 'member_edges', DATA_FILE_MEMBER_EDGES)

def fetch_group_edges_data(pause_group_edges_data):
    return fetch_data(pause_group_edges_data, lambda: get_group_edges(group_ids_filtered), 'group_edges', DATA_FILE_GROUP_EDGES)       

def fetch_event_edges_data(pause_event_edges_data):
    return fetch_data(pause_event_edges_data, lambda: get_event_edges(event_ids), 'event_edges', DATA_FILE_EVENT_EDGES)		

#Fetch Heavy Beefy data here
def fetch_member_posts(pause_member_posts_data):
    return fetch_data(pause_member_posts_data, lambda: extract_member_posts(), 'member_posts', DATA_FILE_MEMBER_POSTS)    

def fetch_group_posts(pause_group_posts_data):
    return fetch_data(pause_group_posts_data, lambda: extract_group_posts(), 'group_posts', DATA_FILE_GROUP_POSTS)
	
def fetch_member_convos(pause_member_convos_data):
    return fetch_data(pause_member_convos_data, lambda: extract_member_conversations(), 'member_convos', DATA_FILE_MEMBER_CONVOS)
	


def fetch_all_data():
	results = {}

	# Define the functions you want to call with corresponding keys
	fetch_functions = {
		'base_data': lambda: fetch_base_data(pause_base_data),
		'members_data': lambda: fetch_member_data(pause_member_data),
		'groups_data': lambda: fetch_group_data(pause_group_data),
		'events_data': lambda: fetch_event_data(pause_event_data),
		'survey_data': lambda: fetch_survey_data(pause_survey_data),
		'member_edges_data': lambda: fetch_member_edges_data(pause_edges_data),
		'event_edges_data': lambda: fetch_event_edges_data(pause_event_edges_data),
		'group_edges_data': lambda: fetch_group_edges_data(pause_group_edges_data),
		'member_posts': lambda: fetch_member_posts(pause_member_posts_data),
		'member_convos': lambda: fetch_member_convos(pause_member_convos_data),	  
		'group_posts': lambda: fetch_group_posts(pause_group_posts_data)
	}

	# Use threading to fetch data concurrently
	threads = []
	for key, func in fetch_functions.items():
		thread = threading.Thread(target=lambda k=key, f=func: results.update({k: f()}))
		threads.append(thread)
		thread.start()

	# Wait for all threads to finish
	for thread in threads:
		thread.join()

	return results	# Return all results as a dictionary


all_data = fetch_all_data()
# Fetch data once when the app starts
base_data = all_data.get('base_data')
members_data = all_data.get('members_data')
groups_data = all_data.get('groups_data')
events_data = all_data.get('events_data')
survey_data = all_data.get('survey_data')
member_edges_data = all_data.get('member_edges_data')
event_edges_data = all_data.get('event_edges_data')
group_edges_data = all_data.get('group_edges_data')
member_posts = all_data.get('member_posts')
group_posts = all_data.get('group_posts')
member_convos = all_data.get('member_convos')

#for media
if pause_convo_media == 0:
	save_media_from_conversations(json_data_convos)
if pause_media_members == 0:
	download_media(json_data, folder_path_m_posts, 'member_posts')
if pause_media_groups == 0:
	download_media(json_data_groups, folder_path_g_posts, 'group_posts')	
if pause_profile_pic == 0:	  
	download_member_pictures_from_file(json_file_path, save_directory)
if pause_group_covers == 0:
	download_group_images(json_file, download_directory)
if pause_event_covers == 0:
		download_event_images(event_json_file, event_dl_directory)

@app.route('/base')
def all_data():
	return jsonify(base_data)

@app.route('/members')
def members_data_route():
	return jsonify(members_data)

@app.route('/groups')
def groups_data_route():
	return jsonify(groups_data)

@app.route('/events')
def events_data_route():
	return jsonify(events_data)
	
@app.route('/surveys')
def surveys_data_route():
	return jsonify(survey_data)

@app.route('/edges')
def edges_data_route():
	return jsonify(member_edges_data)

@app.route('/group_edges')
def group_edges_data_route():
	return jsonify(group_edges_data)
	
@app.route('/event_edges')
def event_edges_data_route():
	return jsonify(event_edges_data)	

@app.route('/member_posts')
def member_posts_data_route():
	return jsonify(member_posts)

@app.route('/group_posts')
def group_posts_data_route():
	return jsonify(group_posts)
    
@app.route('/convos')
def convos_data_route():
    return jsonify(member_convos)

if __name__ == "__main__":
	try:
		app.run(ssl_context=('./certs/cert.pem', './certs/key.pem'), host='0.0.0.0', port=9443)
	except KeyboardInterrupt:
		print("Shutting down...")