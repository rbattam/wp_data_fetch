import os
import yaml

def load_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load your configuration
config = load_config('config.yaml')
# Your API credentials
ACCESS_TOKEN = config['token']['value']

#Blank variables to be populated later
json_data = ''
json_data_groups = ''
json_data_convos = ''
active_user_ids = ''
inactive_user_ids = ''


# Base URL for the Workplace API
BASE_URL = 'https://graph.facebook.com/'

BASE_ENDPOINTS = {
    "community_id" : "community",
    "all_users" : "community/organization_members",
    "active_users" : "community/members",
    "inactive_users" : "community/former_members",
    "groups" : "community/groups",
    "events" : "community/events",
    "surveys" : "community/surveys",
    "skills" : "community/skills",
    "badges" : "community/badges",
    "knowledge_cats" : "community/knowledge_library_categories",
    "knowledge_links" : "community/knowledge_quick_links"
}

ENDPOINTS_FIELDS = {
"member_fields" : "?fields=id, first_name, last_name, email, title, about, active, frontline, organization, division, department, primary_phone, primary_address, picture, link, locale, name, name_format,updated_time, account_invite_time, account_claim_time, account_deactivate_time, external_id, start_date, work_locale, access_code, claim_link, cost_center",
"group_fields" : "?fields=id,cover,description, icon, is_workplace_default, is_community, name, owner, privacy, updated_time, archived, post_requires_admin_approval, purpose, post_permissions, join_setting, is_official_group",
"event_fields" : "?fields=id, attending_count, cover, declined_count, description, end_time, event_times, guest_list_enabled, interested_count, is_canceled, maybe_count, name, owner, parent_group, place, start_time, timezone, type, updated_time",
"skills_fields" : "",
"survey_fields" : "?fields=id, title, is_test, invite_message, questions, scheduling_config",
"post_fields" : "?fields=id, created_time, formatting, from, icon, link, message, name, object_id, permalink_url, picture, place, poll, properties, status_type, story, to, type, updated_time",
"convo_fields" : "?fields=id, email, name, participants, username, updated_time, messages{message, attachments, from}"
}





# Each endpoint formed
all_users = BASE_ENDPOINTS["all_users"]
active_users = BASE_ENDPOINTS["active_users"]
inactive_users = BASE_ENDPOINTS["inactive_users"]
groups = BASE_ENDPOINTS["groups"]
events = BASE_ENDPOINTS["events"]
surveys = BASE_ENDPOINTS["surveys"]
skills = BASE_ENDPOINTS["skills"]
badges = BASE_ENDPOINTS["badges"]
knowledge_cats = BASE_ENDPOINTS["knowledge_cats"]
knowledge_links = BASE_ENDPOINTS["knowledge_links"]


JSON_KEY_DATA = 'data'
JSON_KEY_PAGING = 'paging'
JSON_KEY_NEXT = 'next'


edge_id_names = [
    'member_post_ids', 'group_post_ids',
    'conversation_ids', 'manager_ids', 'report_ids',
    'photo_ids', 'phone_ids', 'skill_ids', 'badge_ids'
]

edge_keys = [
    'feed', 'conversations', 'groups', 'events', 'phones', 'skills',
    'badges', 'reports', 'managers', 'photos'
]

group_edge_keys = [
    'admins', 'albums', 'docs', 'events', 'feed', 'files', 'groups', 'memeber_requests',
    'members', 'moderators'
]