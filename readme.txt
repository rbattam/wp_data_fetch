========================================================================================================
Workplace Data Fetch - Python Tool
	By Robbie Battam
========================================================================================================

STEP 1

Free to use and share, and edit.

I assume you extracted this folder and arent reading inside the zip archive, but if not, extract it before you start.

Note, although this app has no real Interface, it works fine and is not techincally difficult to operate. Just follow these steps and you will be fine.


STEP 2

Open the config.yaml file.

Note there is a specific format in here, use spaces only for the config file.


Note that "levels" and "token" are hard against the left-edge of the file, each level is spaced in exactly 4 spaces, and each sub-item is indented exactly 4 more spaces again.

Although typical Python files are happy to use tabs or spaces, YAML files don't like tabs.  A single tab will break the YAML file and the app won't use it.
If you use incorrect spacing / indentation...... well, YAML format is essentially python, and it will not run.

The values, 1 and 0 or the token are to be placed one space after the : for each item.

You can always paste the content from below back into that config.yaml file if you stuff the formatting (it's not rocket surgery, however).


The format is like this:

levels:
    level_1: # Required for level 2
        pause_base_data: 1
    level_2: # Required for level 3
        pause_member_data: 1
        pause_group_data: 1
        pause_event_data: 0
        pause_survey_data: 1
    level_3: # Required for level 4
        pause_edges_data: 1
        pause_group_edges_data: 1
        pause_event_edges_data: 1
        pause_member_convos_data: 1  # <-- Conversations data is Heavier data than all level 4's
    level_4: # Requires Level 3 Data Downloaded First
        pause_member_posts_data: 1
        pause_group_posts_data: 1
    media: #Obviously, do these last, convo media could be savage in size if you have a large organisation, keep that in mind.
        pause_profile_pic: 1
        pause_group_covers: 1
        pause_event_covers: 1
        pause_media_members: 1
        pause_media_groups: 1
        pause_convo_media: 1
token:
    value: TOKEN_NUMBER_GOES_HERE

========================================================================================================

STEP 4

To get your token:
On workplace app, in admin, go to Custom Integrations  and then set up a new Custom Integration, set everything to ON. And copy the token secret.

Go back to the config.yaml file.
Shove your token in after the "value:" option, make exactly 1 space after value: and paste your WORKPLACE API TOKEN in there (custom integration, whatever rubbish they call it).
========================================================================================================

STEP 5

Open config.yaml

Start with pause_base_data and set it to 0 and leave the rest of the options on 1.  Remember to save every time you change config.yaml, before running the app.

Next ->  Run the "Run as admin" file  (as an admin ....),  Once the Base Data finishes, close the window and open config.yaml again, set pause_base_data back to 1 again.

Set all level 2 items to 0, save yaml, run the file again.
Set all level 2 items back to one again
Set all level 3  items to 0 and save the file and run the app again.

You get the idea? keep doing that pattern.  Media goes last.

Good luck!
========================================================================================================

Info about what the App gets:

This tool will not get videos.  There's no way I've been able to find to actually retrieve the videos as the API doesn't provide the actual storage location of the files, only the POST URL.

Even the default example app someone made for META to use, the guy says "this does not support videos as of this time" in his application notes. So you can see that it's not just me who has this issue.

Work-around for videos:

I'd reccomend getting users of the Workplace groups to download the videos in their groups and saving it all to one central folder.  At least then you have them.

===================================================================================================================================

As for the rest of the media, this tool will get:

Cover photos for groups

Cover photos for events

All photos from member posts

All photos from group posts

All member main profile pics

All files sent in conversations between workplace members (except videos)

All post data for members and groups including extra data, like likes, reactions, seen, comments, etc.

All info about groups and members and events and surveys, and all the weird stuff like badges and skills, categories etc. (the stuff nobody cares about).

All conversations with their messages.  Be careful how you store messages data!, as you can imagine, if someone reads someone elses messages and they are trash talking people, it might open up a can of worms.

====================================================================================================================================

I've also made the app inject Relevant ids into deeper layers of data that is fetched for child items of other data.  As workplace data doesn't seem to do this by default for many important things.
This way you can relate it back to it's parent data later.

I've prevented global shared workplace groups for all worldwide companies using workplace, from being downloaded.  Such as "Workplace Admins". Trust me, you do not want these.

Only your company's own Workplace Groups will be downloaded. Not other organisation's data, or globally shared data that is irrelevant to your business.  If these are allowed to download your download will NEVER finish, itll run for years.  Imagine the Billions of posts in those groups, and your server will crash due to 0 memory and disk space.


I've threaded the app so you can do multiple endpoints at once, well, at least each level's options at once in the yaml file.  (not including media downloads, media will run one after the other).

I will be building a viewer at some point, to look at this historical data.  But for now, its just data saved so you can file it away in your archives, or use it later for something else you may want to build.

The app generates its own SSL certs, they arent gong to be trusted, but the app will run.  Feel free to replace them at any time with a trusted company cert / key pair of PEM format files, with no password on the key.

NOTE:  There are endpoints you can visit to view your data locally, (if you have downloaded it already) as they loaded by the app, threfore, the app serves as a local API server, so you can re-serve the downloaded data to another custom app if you want to make one to use it from this app.

OK good luck!
