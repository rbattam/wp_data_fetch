import requests
import json
import os
from vars import *



#Generic Functions to save space:
# Function to make API requests
def get_data(endpoint):
	if endpoint.startswith("http"):
		url = endpoint
	else:
		url = f"{BASE_URL}{endpoint}"
		print(url)
	headers = {
		'Authorization': f'Bearer {ACCESS_TOKEN}',
	}
	response = requests.get(url, headers=headers)
	
	if response.status_code == 200:
		data = response.json()
		# Ensure the returned data has 'data' and 'paging' keys
		if 'data' in data:
			return data
		elif data not in data:
			{'data': data}
			print(f'{data}')
		else:
			print("Data format unexpected, probably is no data key in what was returned:", data)
			return None
	else:
		print(f"Error {response.status_code}: {response.text}")
		return None

def get_user_ids_from_json(json_file_path):
	user_ids = []

	# Load the JSON data from the specified file
	with open(json_file_path, 'r') as file:
		data = json.load(file)

	# Check for 'members' and 'dead_members' keys
	for key in ['active_users', 'inactive_users']:
		if key in data:
			# Loop through each user in the list and extract their "id"
			for user in data[key]:
				if 'id' in user:
					user_ids.append(user['id'])

	return user_ids


def get_ids(key_name, file):
	# Initialize lists to hold the IDs
	ids = []
	# Load the JSON data from the file
	if os.path.exists(f'./data/{file}'):
		with open(f'./data/{file}', 'r') as f:
			data = json.load(f)
			# Get key value ids
			items = data.get(key_name, [])
			# Extract IDs from items
			for item in items:
				if "id" in item:
					ids.append(item["id"])
			return ids
	return ids

def get_nested_ids(parent_key, child_key, file):
	# Initialize lists to hold the IDs
	ids = []
	# Load the JSON data from the file
	with open(f'./data/{file}', 'r') as f:
		data = json.load(f)
		# Get the parent item
		parent = data.get(parent_key, {})
		
		# Check if parent is a dictionary
		if isinstance(parent, dict):
			# Get the child items from the parent
			children = parent.get(child_key, [])
			# Extract IDs from the child items
			for item in children:
				if "id" in item:
					ids.append(item["id"])
					
	return ids
	

def extract_edge_ids(json_file_path, new_main_key_index, edge, edge_key_name, edge_keys):
	if os.path.exists(json_file_path):	  
		with open(json_file_path, 'r') as file:
			data = json.load(file)
			
		# Get the list name based on the provided index
		new_list_name = edge_id_names[new_main_key_index]
		
		# Use a set to collect unique IDs
		unique_edge_ids = set()

		# Access the specified edge key
		edges = data.get(edge_key_name, {})
		edge_key = edges.get(edge_keys[edge], [])
		print(f"Found {len(edge_key)} edges for {edge_key_name}.")

		# Loop through the entries and collect unique IDs
		for entry in edge_key:
			if 'id' in entry:
				unique_edge_ids.add(entry['id'])  # Use set to ensure uniqueness

		# Convert the set back to a list for returning
		return list(unique_edge_ids)



#uses get_data()
def fetch_data_base(resource_name):
	data_list = []
	endpoint = BASE_ENDPOINTS[resource_name]  # Use the resource_name to get the endpoint

	while endpoint:
		try:
			data = get_data(endpoint)  # Reusing get_data function
			if data:
				items = data.get('data', [])  # Get the list of items
				data_list.extend(items)
				print(f"Fetched {len(items)} {resource_name}, total so far: {len(data_list)}")
				endpoint = data.get('paging', {}).get('next', None)
			else:
				break
		except Exception as e:
			print(f"ERROR: {e}")
			break

	return data_list
#individual functions


import requests

def get_data_dict(endpoint):
	all_data = []  # Initialize a list to hold all fetched data

	# Construct the URL based on whether it's a full URL or a path
	url = endpoint if endpoint.startswith("http") else f"{BASE_URL}{endpoint}"
	print(f"Fetching from URL: {url}")

	headers = {
		'Authorization': f'Bearer {ACCESS_TOKEN}',
		# Add other headers if needed
	}

	while url:	# Continue fetching as long as there is a valid URL
		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			data = response.json()
			print(f"Received data: {data}")	 # Log received data for debugging

			# If the 'data' key exists, extend all_data with its value
			if 'data' in data:
				if isinstance(data['data'], list):
					all_data.extend(data['data'])
				else:
					all_data.append(data['data'])  # Wrap single item in a list
			else:
				# If 'data' key is missing, append the entire response
				all_data.append(data)  # Append the entire response

			# Check for pagination and continue if 'paging' exists
			if 'paging' in data:
				if 'next' in data['paging']:
					url = data['paging']['next']  # Update URL for the next request
					print(f"Fetching next page: {url}")	 # Log the next page URL
				else:
					print(f"No more pages to fetch. Total items fetched: {len(all_data)}")
					url = None	# Stop the loop if no next page is found
			else:
				print(f"No 'paging' key found in response. Stopping after fetching {len(all_data)} items.")
				url = None	# Stop the loop if no paging info is found

		else:
			print(f"Error {response.status_code}: {response.text}")
			break  # Exit the loop if there's an error

	return all_data	 # Return all fetched data


'''	
def get_data_dict(endpoint):
	all_data = []  # Initialize a list to hold all fetched data

	if endpoint.startswith("http"):
		url = endpoint
	else:
		url = f"{BASE_URL}{endpoint}"
		print(url)

	headers = {
		'Authorization': f'Bearer {ACCESS_TOKEN}',
	}

	while url:	# Continue fetching as long as there is a valid URL
		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			data = response.json()

			# If the 'data' key exists, extend all_data with its value
			if 'data' in data:
				if isinstance(data['data'], list):
					all_data.extend(data['data'])
				else:
					all_data.append(data['data'])  # Wrap single item in a list
			else:
				# If 'data' key is missing, handle according to your needs
				all_data.append(data)  # Append the entire response
			
			# Check for pagination and update the URL for the next page
			url = data.get('paging', {}).get('next')
		else:
			print(f"Error {response.status_code}: {response.text}")
			break  # Exit the loop if there's an error

	return all_data	 # Return all fetched data
'''
 
#resuable for  edges loops			 
def fetch_and_extend_data(user_id, endpoint, target_list, include_subject_id=True):
	try:
		while endpoint:
			data = get_data_dict(endpoint)
			print(f"Data for user {user_id}: {data} (type: {type(data)})")
			
			if data:  # Check if data is not None or empty
				if isinstance(data, list):
					for item in data:
						if include_subject_id:
							item['subject_id'] = user_id	 # Add subject_id if required
					target_list.extend(data)  # Extend for lists
				elif isinstance(data, dict):
					if include_subject_id:
						data['subject_id'] = user_id	 # Add subject_id if required
					target_list.extend(data.get('items', []))  # Extend for dicts

				print(f"Fetched {len(data)} items, total so far: {len(target_list)}")

				# Safely handle pagination
				endpoint = data.get('paging', {}).get('next') if isinstance(data, dict) and 'paging' in data else None
			else:
				print(f"No data found for member with ID: {user_id} at {endpoint}")
				break
	except Exception as e:
		print(f"ERROR fetching data for member: {user_id} at {endpoint}: {e}")


def fetch_and_extend_data_group(group_id, endpoint, target_list, include_subject_id=True):
	try:
		while endpoint:
			data = get_data_dict(endpoint)
			print(f"Data for group {group_id}: {data} (type: {type(data)})")
			
			if data:  # Check if data is not None or empty
				if isinstance(data, list):
					for item in data:
						if include_subject_id:
							item['subject_id'] = group_id	 # Add subject_id if required
					target_list.extend(data)  # Extend for lists
				elif isinstance(data, dict):
					if include_subject_id:
						data['subject_id'] = group_id	 # Add subject_id if required
					target_list.extend(data.get('items', []))  # Extend for dicts

				print(f"Fetched {len(data)} items, total so far: {len(target_list)}")

				# Safely handle pagination
				endpoint = data.get('paging', {}).get('next') if isinstance(data, dict) and 'paging' in data else None
			else:
				print(f"No data found for Group with ID: {group_id} at {endpoint}")
				break
	except Exception as e:
		print(f"ERROR fetching data for Group: {group_id} at {endpoint}: {e}")

#relying on get_data_dict for pagination trial it...
def fetch_deep_data(entity_id, endpoint, target_list, include_subject_id=True):
	accessed_endpoints = set()	# Initialize a set to track accessed endpoints
	try:
		if endpoint not in accessed_endpoints:
			accessed_endpoints.add(endpoint)  # Add endpoint to the set
		else:
			print(f"Duplicate endpoint detected: {endpoint}")
			return	# Exit the function if endpoint has already been processed

		# Fetch the data, which handles pagination internally
		data = get_data_dict(endpoint)

		print(f"Data for entity {entity_id}: {data} (type: {type(data)})")

		if data:  # Check if data is not None or empty
			if isinstance(data, list):
				for item in data:
					if include_subject_id:
						item['subject_id'] = entity_id	# Add subject_id if required
				target_list.extend(data)  # Extend for lists
			elif isinstance(data, dict):
				if include_subject_id:
					data['subject_id'] = entity_id	# Add subject_id if required
				target_list.extend(data.get('items', []))  # Extend for dicts

			print(f"Fetched {len(data)} items, total so far: {len(target_list)}")
		else:
			print(f"No data found for Entity with ID: {entity_id} at {endpoint}")

	except Exception as e:
		print(f"ERROR fetching data for Entity: {entity_id} at {endpoint}: {e}")


'''
def fetch_deep_data(entity_id, endpoint, target_list, include_subject_id=True):
	accessed_endpoints = set()	# Initialize a set to track accessed endpoints
	try:
		while endpoint:
			if endpoint not in accessed_endpoints:
				accessed_endpoints.add(endpoint)  # Add endpoint to the set
			else:
				print(f"Duplicate endpoint detected: {endpoint}")

			data = get_data_dict(endpoint)
			print(f"Data for entity {entity_id}: {data} (type: {type(data)})")

			if data:  # Check if data is not None or empty
				if isinstance(data, list):
					for item in data:
						if include_subject_id:
							item['subject_id'] = entity_id	# Add subject_id if required
					target_list.extend(data)  # Extend for lists
				elif isinstance(data, dict):
					if include_subject_id:
						data['subject_id'] = entity_id	# Add subject_id if required
					target_list.extend(data.get('items', []))  # Extend for dicts

				print(f"Fetched {len(data)} items, total so far: {len(target_list)}")

				# Safely handle pagination
				endpoint = data.get('paging', {}).get('next') if isinstance(data, dict) and 'paging' in data else None
			else:
				print(f"No data found for Entity with ID: {entity_id} at {endpoint}")
				break
	except Exception as e:
		print(f"ERROR fetching data for Entity: {entity_id} at {endpoint}: {e}")
'''


	
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Next level Functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
	
def get_member_ids():
	# Initialize lists to hold the member IDs
	inactive_user_ids = []
	active_user_ids = []

	# Load the JSON data from the file
	if os.path.exists('./data/base.json'):
		with open('./data/base.json', 'r') as f:
			data = json.load(f)
			# Get inactive and active users
			inactive_users = data.get("inactive_users", [])
			active_users = data.get("active_users", [])

			# Extract IDs from active users
			for user in active_users:
				if "id" in user:
					active_user_ids.append(user["id"])

			# Extract IDs from inactive users
			for user in inactive_users:
				if "id" in user:
					inactive_user_ids.append(user["id"])

	# Backup return in case the file doesn't exist or contains no data
	return active_user_ids, inactive_user_ids


	
	
#use the group IDS in the function above to retrieve detailed info about each user and their profile.
def get_members_info(active_user_ids, inactive_user_ids):
	members = []
	dead_members = []

	for user_id in active_user_ids:	 # Loop through all active user IDs
		endpoint_active = f'{user_id}{ENDPOINTS_FIELDS["member_fields"]}'
		try:
			data = get_data_dict(endpoint_active)
			print(f"Data for active user {user_id}: {data} (type: {type(data)})")
			if data:  # Check if data is not None or empty
				members.extend(data)  
				print(f"Fetched {len(data)} active members, total so far: {len(members)}")
			else:
				print(f"No data found for active member ID: {user_id}")
		except Exception as e:
			print(f"ERROR fetching active member {user_id}: {e}")

	for user_id in inactive_user_ids:  # Iterate through inactive user IDs
		endpoint_inactive = f'{user_id}{ENDPOINTS_FIELDS["member_fields"]}'
		try:
			data = get_data_dict(endpoint_inactive)
			print(f"Data for inactive user {user_id}: {data} (type: {type(data)})")
			if data:  # Check if data is not None or empty
				dead_members.extend(data)  
				print(f"Fetched {len(data)} inactive members, total so far: {len(dead_members)}")
			else:
				print(f"No data found for inactive member ID: {user_id}")
		except Exception as e:
			print(f"ERROR fetching inactive member {user_id}: {e}")

	print(f"Total active members fetched: {len(members)}")
	print(f"Total inactive members fetched: {len(dead_members)}")
	
	return members, dead_members

	

		
def get_member_edges(active_user_ids, inactive_user_ids):
	events = []
	feed = []
	conversations = []
	managers = []
	reports = []
	picture = []
	groups = []
	phones = []
	skills = []
	badges = []
	
	for user_id in active_user_ids:
		endpoints = {
			"events": f'{user_id}/events',
			"feed": f'{user_id}/feed',
			"conversations": f'{user_id}/conversations',
			"managers": f'{user_id}/managers',
			"reports": f'{user_id}/reports',
			"picture": f'{user_id}/picture?redirect=0&type=large',
			"groups": f'{user_id}/groups',
			"phones": f'{user_id}/phones',
			"skills": f'{user_id}/skills',
			"badges": f'{user_id}/badges'
		}

		for key, endpoint in endpoints.items():
			fetch_and_extend_data(user_id, endpoint, locals()[key])
			
	for user_id in inactive_user_ids:
		inactive_endpoints = {
			"events": f'{user_id}/events',
			"feed": f'{user_id}/feed',
			"conversations": f'{user_id}/conversations',
			"managers": f'{user_id}/managers',
			"reports": f'{user_id}/reports',
			"picture": f'{user_id}/picture?redirect=0&type=large',
			"groups": f'{user_id}/groups',
			"phones": f'{user_id}/phones',
			"skills": f'{user_id}/skills',
			"badges": f'{user_id}/badges'
		}		

		for key, endpoint in inactive_endpoints.items():
			fetch_and_extend_data(user_id, endpoint, locals()[key])

	return {
		"events": events,
		"feed": feed,
		"conversations": conversations,
		"managers": managers,
		"reports": reports,
		"picture": picture,
		"groups": groups,
		"phones": phones,
		"skills": skills,
		"badges": badges
	}  

	
#group ids runs generic function and is launched on app.py

#Use group IDS to fetch each groups full detailed information
def get_groups_info(group_ids):
	groups = []

	for group_id in group_ids:	# Loop through all group IDs
		endpoint_active = f'{group_id}{ENDPOINTS_FIELDS["group_fields"]}'  # Correct endpoint format
		try:
			data = get_data_dict(endpoint_active)
			print(f"Data for active group {group_id}: {data} (type: {type(data)})")

			if data:  # Check if data is not None or empty
				# Handle list responses
				if isinstance(data, list) and len(data) > 0:
					group_data = data[0]  # Get the first item (assuming it's the relevant one)
					
					# Check if group_data is a dictionary and has the "purpose" key
					if isinstance(group_data, dict):
						purpose = group_data.get("purpose", "Unknown")	# Default to "Unknown"
						if purpose != "WORK_MULTI_COMPANY":	 # Adjust this line based on your filtering criteria
							groups.append(group_data)  # Append the valid group data
							print(f"Fetched group: {group_data.get('name')}, total so far: {len(groups)}")
						else:
							print(f"Skipping group {group_id} due to purpose: {purpose}")
					else:
						print(f"Unexpected data format for group {group_id}: {group_data}")
				else:
					print(f"Unexpected data format for group {group_id}: {data}")
			else:
				print(f"No data found for group ID: {group_id}")
		except Exception as e:
			print(f"ERROR fetching group {group_id}: {e}")

	return groups



'''
def get_groups_info(group_ids):
	
	groups = []

	for group_id in group_ids:	# Loop through all active user IDs
		endpoint_active = f'{group_id}{ENDPOINTS_FIELDS["group_fields"]}'
 # Correct endpoint format
		try:
			data = get_data_dict(endpoint_active)
			print(f"Data for active group {group_id}: {data} (type: {type(data)})")
			if data:  # Check if data is not None or empty
				# Since data is a list now, you can directly extend members
				groups.extend(data)	 
				print(f"Fetched {len(data)} groups, total so far: {len(groups)}")
			else:
				print(f"No data found for group ID: {group_id}")
		except Exception as e:
			print(f"ERROR fetching group {group_id}: {e}")

	return groups
'''	
def get_group_edges(group_ids):
	admins = []
	albums = []
	auto_membership_rules = []
	docs = []
	events = []
	feed = []
	files = []
	member_requests = []
	members = []
	moderators = []
	pinned_posts = []
	groups = [] 
	
	for group_id in group_ids:
		endpoints = {
			"admins": f'{group_id}/admins',
			"albums": f'{group_id}/albums',
			"auto_membership_rules": f'{group_id}/auto_membership_rules',
			"docs": f'{group_id}/docs',
			"events": f'{group_id}/events',
			"feed": f'{group_id}/feed',
			"files": f'{group_id}/files',
			"member_requests": f'{group_id}/member_requests',
			"members": f'{group_id}/members',
			"moderators": f'{group_id}/moderators',
			"pinned_posts": f'{group_id}/pinned_posts',
			"groups": f'{group_id}/groups'			  
		}

		for key, endpoint in endpoints.items():
			fetch_and_extend_data_group(group_id, endpoint, locals()[key])
	  

	return {
		"admins": admins,
		"albums": albums,
		"auto_membership_rules": auto_membership_rules,
		"docs": docs,
		"events": events,
		"feed": feed,
		"files": files,
		"member_requests": member_requests,
		"members": members,
		"moderators": moderators,
		"pinned_posts": pinned_posts,
		"groups": groups
	}  
	

	
def get_events_info(event_ids):
	
	events = []

	for event_id in event_ids:	# Loop through all active user IDs
		endpoint_active = f'{event_id}{ENDPOINTS_FIELDS["event_fields"]}'
 # Correct endpoint format
		try:
			data = get_data_dict(endpoint_active)
			print(f"Data for active event {event_id}: {data} (type: {type(data)})")
			if data:  # Check if data is not None or empty
				# Since data is a list now, you can directly extend members
				events.extend(data)	 
				print(f"Fetched {len(data)} events, total so far: {len(events)}")
			else:
				print(f"No data found for event ID: {event_id}")
		except Exception as e:
			print(f"ERROR fetching event {event_id}: {e}")

	return events
	
def get_event_edges(event_ids):
	admins = []

	
	for event_id in event_ids:
		endpoints = {
			"admins": f'{event_id}/admins'
		}

		for key, endpoint in endpoints.items():
			fetch_deep_data(event_id, endpoint, locals()[key])
	  

	return {
		"admins": admins
	}		  

#ids runs on app.py using new generic function
def get_survey_info(survey_ids):
	
	surveys = []
	
	for survey_id in survey_ids:  # Loop through all active user IDs
		endpoint_active = f'{survey_id}{ENDPOINTS_FIELDS["survey_fields"]}'
 # Correct endpoint format
		try:
			data = get_data_dict(endpoint_active)
			print(f"Data for active survey {survey_id}: {data} (type: {type(data)})")
			if data:  # Check if data is not None or empty
				# Since data is a list now, you can directly extend members
				surveys.extend(data)  
				print(f"Fetched {len(data)} surveys, total so far: {len(surveys)}")
			else:
				print(f"No data found for survey ID: {survey_id}")
		except Exception as e:
			print(f"ERROR fetching survey {survey_id}: {e}")

	return surveys

	
#PULL of POSTS
#New main JSON key for each ID section



'''
def extract_member_posts():
	# Get the IDs for member posts from the feed
	  # For 'member_post_ids' and 'feed'
	member_post_ids = extract_edge_ids('./data/member_edges.json', 0, 0, 'member_edges', edge_keys)
	# Initialize a list to hold retrieved post data
	list_to_fill = []
	
	# Define the endpoints directly as a list of strings
	endpoints = [
		f'{ENDPOINTS_FIELDS["post_fields"]}',  # For fields, append to post_id later
		'/attachments',
		'/comments',
		'/reactions',
		'/seen'
	]
	
	# Loop through each post ID and fetch the corresponding post data
	for post_id in member_post_ids:
		for endpoint in endpoints:
			# Construct the full endpoint using the post_id
			full_endpoint = f'{post_id}{endpoint}'	# Concatenate post_id with the endpoint
			fetch_deep_data(post_id, full_endpoint, list_to_fill)  # Fetch data for the constructed endpoint

	return list_to_fill	 # Return the collected post data
'''
def extract_member_posts():
	# Get the IDs for member posts from the feed
	member_post_ids = extract_edge_ids('./data/member_edges.json', 0, 0, 'member_edges', edge_keys)
	list_to_fill = []

	# Define the endpoints
	endpoints = [
		f'{ENDPOINTS_FIELDS["post_fields"]}',  # For fields
		'/attachments',
		'/comments',
		'/reactions',
		'/seen'
	]

	# Loop through each post ID and fetch the corresponding post data
	for post_id in member_post_ids:
		for endpoint in endpoints:
			full_endpoint = f'{post_id}{endpoint}'	# Construct full endpoint
			fetch_deep_data(post_id, full_endpoint, list_to_fill)  # Pass the target list

	# After all data is fetched, append post_id to each item in the list
	'''		
	for item in list_to_fill:
		item['post_id'] = item.get('id', post_id)
	'''		   # Add post_id, or use 'id' if available

	return list_to_fill	 # Return the collected post data

	
def extract_member_conversations():
	if os.path.exists('./data/base.json'):
		all_user_ids = get_user_ids_from_json('./data/base.json')

	list_to_fill = []

	# Define the endpoints directly as a list of strings (modify as needed)
	endpoints = [
		f'{ENDPOINTS_FIELDS["convo_fields"]}'
	]

	# Loop through each user ID and fetch the corresponding conversation data
	for user_id in all_user_ids:
		for endpoint in endpoints:
			# Construct the full endpoint using the user_id
			full_endpoint = f'{user_id}/conversations/{endpoint}'  # Concatenate user_id with the endpoint
			fetch_deep_data(user_id, full_endpoint, list_to_fill)  # Fetch data for the constructed endpoint

	return list_to_fill	 # Return the collected conversation data	 
	
def extract_thread_messages():
	all_user_ids = get_user_ids_from_json('./data/base.json')
	all_thread_ids = get_nested_ids('member_edges', 'conversations', 'member_edges.json')
	print(all_thread_ids)
	list_to_fill = []

	# Loop through each thread ID
	for thread_id in all_thread_ids:
		# Loop through each user ID
		for user_id in all_user_ids:
			# Construct the full endpoint using the thread_id and user_id
			full_endpoint = f'{thread_id}/messages?user={user_id}'	# Adjust based on API requirements
			fetch_deep_data(thread_id, full_endpoint, list_to_fill)	 # Fetch data for the constructed endpoint
			full_endpoint = f'{thread_id}/messages?user={user_id}'
			print(f"Fetching from endpoint: {full_endpoint}")			 

	return list_to_fill	 # Return the collected conversation data
	
def extract_messages_final():
	all_thread_ids = get_nested_ids('member_edges', 'conversations', 'member_edges.json')

	list_to_fill = []

	# Loop through each user ID and fetch the corresponding conversation data
	for thread_id in all_thread_ids:
			# Construct the full endpoint using the user_id
			full_endpoint = f'{thread_id}?fields=id, email, name, participants, username, updated_time, messages{{message, attachments, from}}' 
			fetch_deep_data(thread_id, full_endpoint, list_to_fill)	 # Fetch data for the constructed endpoint	  
 
	
def extract_group_posts():
	# Get the IDs for group posts from the feed
	# index 1 from edge_id_names and index 4 from group_edge_keys 'feed'
	group_post_ids = extract_edge_ids('./data/group_edges.json', 1, 4, 'group_edges', group_edge_keys)
	# Initialize a list to hold retrieved post data
	list_to_fill = []
	
	# Define the endpoints directly as a list of strings
	endpoints = [
		f'{ENDPOINTS_FIELDS["post_fields"]}',  # For fields, append to post_id later
		'/attachments',
		'/comments',
		'/reactions',
		'/seen'
	]
	
	# Loop through each post ID and fetch the corresponding post data
	for post_id in group_post_ids:
		for endpoint in endpoints:
			# Construct the full endpoint using the post_id
			full_endpoint = f'{post_id}{endpoint}'	# Concatenate post_id with the endpoint
			fetch_deep_data(post_id, full_endpoint, list_to_fill)  # Fetch data for the constructed endpoint

	return list_to_fill	 # Return the collected post data
	

#Function Templates	

#fetch function single key
def fetch_and_save(fetch_function, key, filename):
	# Call the fetch function to get the data
	list_to_fill = fetch_function()
	
	# Create the data dictionary with the specified key
	data = {key: list_to_fill}
	
	# Save the data to a JSON file
	with open(filename, 'w') as f:
		json.dump(data, f)
	
	# Returning the structured data (optional)
	return data
	#Fetch data which calls teh above function
def fetch_data(pause_data, fetch_function, key, filename):
	if pause_data == 0:
		return fetch_and_save(fetch_function, key, filename)

	if os.path.exists(filename):
		with open(filename, 'r') as f:
			return json.load(f)
	
	return None #Fetch data which calls teh above function