def install(package, e):
	print(f"Error: {e}")
	print(f"{package} dependency not found")
	answer = input(f"Would you like to install {package}? y/n: ")
	if answer.lower() == "y":
		print("Beginning installation...")
		
		import platform
		OS = platform.system()
		print(OS)
		
		import os
		if "Windows".lower() in OS.lower():
			os.system(f"pip install {package} && echo. && echo Restart program after package installation. && pause") # for Windows
		else:
			os.system(f"pip3 install {package}") #for Linux and MacOS
		
		print("Restart program after package installation.")
	else:
		print("f{package} is required to run this program.")

try:
    package = "google-api-python-client"
    from googleapiclient.discovery import build
except ModuleNotFoundError as e:
    install(package, e)
else:
    # print(f"{package} already installed")
    pass

# https://console.cloud.google.com/apis/credentials?project=youtube-api-350700
  
# with open("api_key.txt", "r") as token:
# https://www.w3schools.com/python/python_file_open.asp
f = open("api_key.txt", "r")
api_key = f.read()
  
def get_subs_info(response):
  subs = [subs for subs in response["items"]]
  # for sub in response
  # print(f"Subs: {subs[0]}")
  # for i in subs:
    # print(i["snippet"]["resourceId"]["channelId"])
  subs_ids = [subsubs["snippet"]["resourceId"]["channelId"] for subsubs in subs]
  # print(subs_ids)
  subs_titles = [subsubs["snippet"]["title"] for subsubs in subs]
  # print(subs_titles)
  return subs_ids, subs_titles

def get_username(user_id):
  request = youtube.channels().list(part="snippet", id=user_id)
  response = request.execute()
  username = response['items'][0]['snippet']['title']
  return username
  
from shutil import ExecError
from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)
  
def get_subscription_data(user, youtube=youtube):
  print("Getting subscription data...")
  request = youtube.subscriptions().list(part="snippet", channelId=user, maxResults=50, pageToken=None, forChannelId=None, order="alphabetical")
  # pageToken examples: CAEQAA, CAIQAA
  try:
    response = request.execute()
  # except googleapiclient.discovery.HttpError as e: 
  except Exception as e:
    if "The requester is not allowed to access the requested subscriptions." in str(e):
    #   raise Exception("HttpError: Subscriptions for one of the accounts are not public.")
        print("Subscriptions for one of the accounts are not public. Requesting login for data.")

        # Let's get private data by logging in then!
        # https://www.thepythoncode.com/article/using-youtube-api-in-python
        # pip install google-api-python-client
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request

        import urllib.parse as p
        import re
        import os
        import pickle

        SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        def youtube_authenticate():
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            api_service_name = "youtube"
            api_version = "v3"
            client_secrets_file = "client_secret_326762071450-c1n449dkr7ugcjgfea261dk4lma3idg2.apps.googleusercontent.com desktop.json"
            creds = None
            # the file token.pickle stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first time
            global token_filename
            token_filename = "token.pickle" 
            if os.path.exists(token_filename):
                with open(token_filename, "rb") as token:
                    creds = pickle.load(token)
            # if there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                # save the credentials for the next run
                with open(token_filename, "wb") as token:
                    pickle.dump(creds, token)

            return build(api_service_name, api_version, credentials=creds)

        # authenticate to YouTube API
        youtube = youtube_authenticate()

        # Now that we have private data access, let's try again.
        request = youtube.subscriptions().list(part="snippet", channelId=user, maxResults=50, pageToken=None, forChannelId=None, order="alphabetical")
        from googleapiclient import errors
        try:
            response = request.execute()
        except errors.HttpError as e:
            # print(e)
            print()
            if "The requester is not allowed to access the requested subscriptions." in str(e):
              username = get_username(user_id=user)
              print(f"Don't have permission to access {username}'s account. This is probably because you're logged into the wrong account.")
              user_input = input(f"Is youtube.com/channel/{user} your account? y/n: ")
              if user_input.lower() == "y":
                user_input = input("Would you like to log out? You'll lose your access tokens to this account. Backup your token.pickle file if you'd like to keep it. y/n: ")
                if user_input.lower() == "y":
                    import os
                    print()
                    print(f"Deleting {token_filename} file")
                    print()
                    os.remove(token_filename)

                    raise Exception("Please restart the current script.")
                else:
                    raise Exception("Need to be logged in since the account doesn't have subscription data public. Go to https://www.youtube.com/account_privacy to make it public. Then go to https://www.youtube.com/account_advanced and copy your Channel ID.")
              else:
                users_ids.remove(user)
                return
            

  # request.execute()

  subscriptions = []
  subscriptions_ids = []
  users_subscriptions_ids = []
  users_subscriptions_titles = []
  try:
    nextpagetoken = response["nextPageToken"]
  except KeyError:
    # only one page
    subs_ids, subs_titles = get_subs_info(response)
    username = get_username(user_id=user)
    subscriptions.append(subs_titles)
    pass
  # print(nextpagetoken)
  # pages = response["pageInfo"]["totalResults"] / response["pageInfo"]["resultsPerPage"]

  # response
  # print(response)
  final_page = False

  # If nextpagetoken is not defined because there is only one page, set to None
  try:
    nextpagetoken
  except: nextpagetoken = None

  while not final_page:
    request = youtube.subscriptions().list(part="snippet", channelId=user, maxResults=50, pageToken=nextpagetoken, forChannelId=None, order="alphabetical")
    from googleapiclient import errors
    try:
        response = request.execute()
    except errors.HttpError as e:
        print(e)
        print()
        if "Internal error encountered." in str(e):
          raise Exception("Internal error: one of the user's channel ID's are probably invalid.")
    
    subs_ids, subs_titles = get_subs_info(response)
    username = get_username(user_id=user)
    subscriptions_ids.append(subs_ids)
    subscriptions.append(subs_titles)
    # print(subscriptions)
  
    # for user_num in range(len(users_ids)):
    #   user_data["user_id"] = Lines[0].strip()
    #   users_data.append(user_data)

    """
    users_data
    [{'user_id': 'UCf7...', 
    'users_subscriptions_titles': '[GreatScott!...,]', 
    'users_subscriptions_ids': [UC6mIx...,]},
    {'user_id': 'UCf7...', 
    'users_subscriptions_titles': '[GreatScott!...,]', 
    'users_subscriptions_ids': [UC6mIx...,]}]
    """
  
    try: 
      nextpagetoken = response["nextPageToken"]
    except:
      final_page = True

  # print(subscriptions)

  # Flatten list, there might be multiple pages and each page is a new list
  import itertools
  merged = list(itertools.chain.from_iterable(subscriptions))
  # print(merged)
  # print(len(merged))
  # Delete duplicates
  mylist = list(dict.fromkeys(merged))
  # print(mylist)
  # print(len(mylist))
  # """this should be a dictionary"""
  users_subscriptions_titles.append(mylist)

  # Now do the same for the IDs
  # Flatten list, there might be multiple pages and each page is a new list
  merged = list(itertools.chain.from_iterable(subscriptions_ids))
  # Delete duplicates
  mylist = list(dict.fromkeys(merged))
  users_subscriptions_ids.append(mylist)
  
  return users_subscriptions_titles, users_subscriptions_ids, username
  
  
# https://www.geeksforgeeks.org/read-a-file-line-by-line-in-python/
# Using readlines()
file1 = open('youtube_channel_ids.txt', 'r')
Lines = file1.readlines()
  
count = 0
users_ids = []
# Strips the newline character
for line in Lines:
    count += 1
    # print("Line{}: {}".format(count, line.strip()))
    users_ids.append(line.strip())

users_data = []
user_data = {}
line_num = 0
for user_num in range(len(users_ids)):
  # Add user id to user data dictionary
  # print(f"user num + line num: {user_num + line_num}")
  
  # Gotta put the user ID in the dictionary first and then we can iterate through the items in the dictionary
  user_data["user_id"] = Lines[user_num].strip()
  # print(user_data["user_id"])
  # print(Lines)
  line_num += 1
  # # Add user data dictionary to users data list
  # users_data.append(user_data)
  
  # print(f"user num: {user_num}")
  # print(f"users ids: {users_ids[user_num]}")
  
  # print(user_num)
  # print(len(users_ids))
  try:
    users_subscriptions_titles, users_subscriptions_ids,username = get_subscription_data(user=users_ids[user_num])
  except TypeError: print("Skipping user")
  except IndexError: pass
  
  # Add username to user data dictionary
  user_data["username"] = username
  
  # Add user subscription titles to user data dictionary
  user_data["user_subscriptions_titles"] = users_subscriptions_titles
  # print(f"Userdata['user_id']: {user_data['user_id']}")
  
  
  # Add user data dictionary to users data list
  users_data.append(user_data.copy())
  #                           .copy() or else it will act as if user_data never changed
  #                           this is because it's referencing the same user data dictionary
  #                           I think it has something to do with mutability/immutability
  # print(len(users_data))

# https://www.geeksforgeeks.org/clear-screen-python/
# define our clear function
def clear():
  # import only system from os
  from os import system, name
  # for windows
  if name == 'nt':
      _ = system('cls')
  # for mac and linux(here, os.name is 'posix')
  else:
      _ = system('clear')

clear()
# print(users_data[1]['user_subscriptions_titles'])

# finds common items in 2 lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
  
# set.intersection(*map(set,d))

 
# Driver Code
lst1 = users_data[0]['user_subscriptions_titles'][0] # for some reason it's a list of a list so we have to take the 0th one, even though it has a len() of 1
lst2 = users_data[1]['user_subscriptions_titles'][0] # for some reason it's a list of a list so we have to take the 0th one, even though it has a len() of 1
# lst4 = ['Trader University', 'NileRed', 'Hamilton Morris', 'Myers Mushrooms Farms', 'Greengenes Garden', 'Charls Carroll', 'Mike Boyd', 'TheraminTrees', 'I did a thing', 'Self Sufficient Me', 'Digital Asset News', 'ARK Invest', 'MillionDollarExtreme2', 'Terra Mater', 'yukikawae', 'BuildASoil', 'Nathaniel Whittemore', 'Prof. Edward Dutton: The Jolly Heretic', 'Michigan organic Budz', 'homesteadonomics', 'Robert Sepehr', 'Oxen Project', 'dnsl', 'Langfocus', 'Approtechie', 'DavvyOnYT', "The Investor's Podcast Network", 'Mycology corner', 'Monsieur Z', 'Paul Stamets', 'History Debunked', 'The Spiffing Brit', 'The Market Sniper', 'Benjamin Cowen', 'NakeyJakey', 'Steve Wallis', 'FirstBuild', 'Southwest Mushrooms', 'S2 Underground', 'Best of Perfect Guy Life-MDE', 'DIY Perks', 'Learn Organic Gardening at GrowingYourGreens', 'PilotRedSun', 'Joel Haver', 'Tech Ingredients', 'Home Mycology', 'DistroTube', 'Warlockracy', 'GeoWizard', 'Fresh from the Farm Fungi', "Tod's Workshop", 'Linus Tech Tips', 'Dapp University', 'WHAT THE FUNGUS', 'Crowbcat', 'Jack Sather', 'From Seed to Stoned', 'Sheldon Evans', 'Limmy', 'Mossy Creek Mushrooms', 'Advoko MAKES', 'I Allegedly', 'Earth Angel Mushrooms', 'Anton Petrov', 'Kamikaze Cash', 'JonTronShow', 'WhistlinDiesel', 'Mike Rosehart', 'InRangeTV', 'General Sam', 'HAINBACH', 'Anthony Pompliano', 'DeBacco University', 'Guga Foods', 'HydeWars', 'Vagrant Holiday', 'lil incognito', 'Gamers Nexus', 'Simon Roper', 'Bybit', "Rob Bob's Aquaponics & Backyar's Lemonade - Crime Documentary", 'anton newcombe', 'JayzTwoCents', 'Brandon Buckingham', '2DNSL', 'Louis Rossmann', 'FunGuyFruits', 'InvestAnswers', 'YouTube Movies', 'Fully Silent PCs', 'Kitboga', 'Carefree Wandering', 'Crypto Face', 'Aamon Animations', 'Gregory Mannarino', 'subcool420', 'Sous Vide Everything', 'Coin Bureau', 'J. Kenji López-Alt', 'Engineer Man', 'Forgotten Weapons', 'Techlore', 'Kurzgesagt – In a Nutshell']

# print("Sleeping")
# import time
# time.sleep(2)
# print(len(users_data))
for user_num in range(len(users_data)-1): # -1 because we skip the first user later in the loop, so the length is shorter
  # request = youtube.subscriptions().list(part="snippet", channelId=users_data[user_num]['user_id'], maxResults=1, pageToken=None, forChannelId=None, order="alphabetical")
  # request = youtube.channel_search()
  # https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.channels.html
  # id, forUsername, mine, managedByMe, categoryId, mySubscribers
  # request = youtube.channels().list(part="snippet", id=users_data[user_num]['user_id'])
  # response = request.execute()
  # print(f"Response: {response}")
  # dictionary of a dictionary of a list of a dictionary of a dictionary
  # print(response['items'][0]['snippet']['title'])
  
  # Add username to user data dictionary
  # user_data["username"] = username
  
  # Add user data dictionary to users data list
  # I need to replace the first dictionary
  # users_data.append(user_data.copy())
  # subs_ids, subs_titles = get_subs_info(response)
  
  # print(users_data[0])
  # raise Exception()
  
  # print(users_data[user_num]['user_id'])
  
  
  # print(f"Subscriptions in common with {users_ids[user_num]}")
  # print(users_data[0])
  # raise Exception

  # print(f"Subscriptions in common with {users_data[user_num+1]['username']}")
  # print(f"Comparing user_id1 subscriptions with {users_data[user_num+1]['username']}")
  # try:
  #                                                                                       skip comparing user to themself by adding 1
  common_subs_num = len(intersection(users_data[0]['user_subscriptions_titles'][0], users_data[user_num+1]['user_subscriptions_titles'][0]))
  print(f"{users_data[0]['username']} and {users_data[user_num+1]['username']} have {common_subs_num} subscriptions in common.")

  # Add number of common subscriptions to user_data dictionary
  users_data[user_num+1]['common_subs_num'] = common_subs_num
  
  print(intersection(users_data[0]['user_subscriptions_titles'][0], users_data[user_num+1]['user_subscriptions_titles'][0]))
  print()
  # except IndexError as e: 
  #   print(e)
    # pass
  
# print(users_data[-2])
exit()
"""
for user_num in range(len(users_ids)):
  # Add user id to user data dictionary
  # print(f"user num + line num: {user_num + line_num}")
  
  # Gotta put the user ID in the dictionary first and then we can iterate through the items in the dictionary
  user_data["user_id"] = Lines[user_num].strip()
  # print(user_data["user_id"])
  # print(Lines)
  line_num += 1
  # # Add user data dictionary to users data list
  # users_data.append(user_data)
  
  # print(f"user num: {user_num}")
  # print(f"users ids: {users_ids[user_num]}")
  
  print(user_num)
  print(len(users_ids))
  try:
    users_subscriptions_titles, users_subscriptions_ids = get_subscription_data(user=users_ids[user_num])
  except TypeError: print("Skipping user")
  except IndexError: pass
  # Add user subscription titles to user data dictionary
  user_data["user_subscriptions_titles"] = users_subscriptions_titles
  # print(f"Userdata['user_id']: {user_data['user_id']}")
  
  # Add user data dictionary to users data list
  users_data.append(user_data.copy())
  #                           .copy() or else it will act as if user_data never changed
  #                           this is because it's referencing the same user data dictionary
  #                           I think it has something to do with mutability/immutability
  # print(len(users_data))
"""
  
  
  
  
# print(set.intersection(*map(set,users_data)))
# output: {'user_subscriptions_titles', 'user_id'}
# print(set.intersection( *[ set(tuple(x) for x in users_data[key]) for key in users_data ] ))

# Python code to demonstrate
# intersection of two dictionaries 
# using dict comprehension
  
# inititialising dictionary
# ini_dict1 = {'nikhil': 1, 'vashu' : 5,
            #  'manjeet' : 10, 'akshat' : 15}
# ini_dict2 = {'akshat' :15, 'nikhil' : 1, 'me' : 56}
  
# printing initial json
# print ("initial 1st dictionary", ini_dict1)
# print ("initial 2nd dictionary", ini_dict2)
  
# It's a list of dictionaries with lists as the values
  
# intersecting two dictionaries
# final_dict = dict(users_data[0].items() & users_data[1].items())
# print ("final dictionary", str(final_dict))
# print(users_data[0].items())

# from functools import reduce
# reduce(set.intersection, map(set, users_data[0].values()))
# {23}


print()
print(f"Users have {len(intersection_as_list)} subscriptions in common:")
print(intersection_as_list)
print()
raise Exception("")

"""
users_data
[{'user_id': 'UCf7...', 
'users_subscriptions_titles': '[GreatScott!...,]', 
'users_subscriptions_ids': [UC6mIx...,]},
 {'user_id': 'UCf7...', 
'users_subscriptions_titles': '[GreatScott!...,]', 
'users_subscriptions_ids': [UC6mIx...,]}]
"""








users_subscriptions_titles = []
users_subscriptions_ids = []
users_data = []
# for user in users_ids:

  

  # response

for user_num in range(len(users_ids)):
  users_data[user_num] = user
  
print(users_data)
input()



# using zip()
# to convert lists to dictionary
# https://www.geeksforgeeks.org/python-convert-two-lists-into-a-dictionary/
user1_subscriptions = dict(zip(users_subscriptions_titles[0], users_subscriptions_ids[0]))
user2_subscriptions = dict(zip(users_subscriptions_titles[1], users_subscriptions_ids[1]))
# print(user1_subscriptions)
# print(user2_subscriptions)

# print(f"User subs: {user_subscriptions}")

# print(f"User 1: {user_subscriptions[0]}")
print()
# https://www.w3schools.com/python/python_dictionaries_access.asp
# print(f"User 2: {user2_subscriptions.keys()}")


list1_as_set = set(user1_subscriptions)
intersection = list1_as_set.intersection(user2_subscriptions)
#Find common elements of set and list

intersection_as_list = sorted(list(intersection))

print()
print(f"Users have {len(intersection_as_list)} subscriptions in common:")
print(intersection_as_list)
print()

try:
  print(f"User 1 has {round((len(intersection_as_list) / len(user1_subscriptions))*100)}% of subscriptions in common")
except ZeroDivisionError: pass
try:
  print(f"User 2 has {round((len(intersection_as_list) / len(user2_subscriptions))*100)}% of subscriptions in common")
except ZeroDivisionError: pass

print()
print("Channels you may be interested in that they are subscribed to:")
print(sorted(set(user2_subscriptions) - set(user1_subscriptions)))

print()

# So, we need to first search the user input string in the user_subscriptions
# Does the youtube api have some sort of function that can help with this? Can we use the title to find the id?


# import sleep to show output for some time period
from time import sleep


# f = open("api_key.txt", "r")
# api_key = f.read()
clear()

load = False
if load == True:
  print("Loading user subscriptions database")
  with open('user_subscriptions_database.txt', 'r') as file: 
    user_subscriptions_database = file.read()

  # clear()

  # Separate each newline
  user_subscriptions_database = user_subscriptions_database.split("\n")
  
  line_number = 1
  for user_num in range(len(users_ids)):
    # Split string of subscription titles into list
    users_subscriptions_titles[user_num] = user_subscriptions_database[line_number].split(",")
    # Strip off the extra text on the edges
    users_subscriptions_titles[user_num] = [i.strip("[']\" ") for i in users_subscriptions_titles[user_num]]
    # print(users_subscriptions_titles[0][0])
    line_number += 1

    # Split string of subscription IDs into list
    users_subscriptions_ids[user_num] = user_subscriptions_database[line_number].split(",")
    # Strip off the extra text on the edges
    users_subscriptions_ids[user_num] = [i.strip("[']\" ") for i in users_subscriptions_ids[user_num]]

    # Skip user_subscriptions_database[3] because that is the user id
    line_number += 2


  # print(users_subscriptions_titles[1])

  # Subscription IDS
  # print(user_subscriptions_database[2])
  clear()
  # And finally we have loaded the saved database into dictionaries
  # user1_subscriptions = dict(zip(users_subscriptions_titles[0], users_subscriptions_ids[0]))
  # user2_subscriptions = dict(zip(users_subscriptions_titles[1], users_subscriptions_ids[1]))
  
  # And finally we have loaded the saved database into a list of dictionaries
  user_subscriptions_database_final = []
  for user_num in range(len(users_ids)):
    user_subscriptions_database_final.append(dict(zip(users_subscriptions_titles[user_num], users_subscriptions_ids[user_num])))

  print()
  print(user_subscriptions_database_final[1])
  print()
  print(user_subscriptions_database_final[2])

# https://stackoverflow.com/questions/6612769/is-there-a-more-elegant-way-for-unpacking-keys-and-values-of-a-dictionary-into-t
# Separate dictionary keys and values into two lists
# keys, subscr = zip(*user1_subscriptions.items())
# this is actually redundant because I already have user_subscriptions and user_subscriptions_ids

# https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
users_checked = []
with open('user_subscriptions_database.txt', 'r') as file: 
  readfile = file.read()
  for user in users_ids:
    if user in readfile:
      print("User already in database")   
    else:
      print("Adding user to database")
input()

# https://www.pythonforbeginners.com/files/with-statement-in-python
# Make a database that holds user subscriptions
print("Saving user subscriptions")           #a
with open('user_subscriptions_database.txt', 'w') as file:    
    for user_num in range(len(users_ids)):
      file.write(str(users_ids[user_num]))
      file.write(str("\n"))
      file.write(str(users_subscriptions_titles[user_num]))
      file.write(str("\n"))
      file.write(str(users_subscriptions_ids[user_num]))
      file.write(str("\n"))
      
raise Exception("")

# Ask the user if they want to search new channels from other users
i = 0
channels_searched = []
while True:
  if i >= 20:
    clear()
    print()
    print(f"Users have {len(intersection_as_list)} subscriptions in common:")
    print(intersection_as_list)
    print()

    try:
      print(f"User 1 has {round((len(intersection_as_list) / len(user1_subscriptions))*100)}% of subscriptions in common")
    except ZeroDivisionError: pass
    try:
      print(f"User 2 has {round((len(intersection_as_list) / len(user2_subscriptions))*100)}% of subscriptions in common")
    except ZeroDivisionError: pass

    print()
    print("Channels you may be interested in that they are subscribed to:")
    print(sorted(set(user2_subscriptions) - set(user1_subscriptions) - set(channels_searched)))
    i = 0
  print()
  channel_search = input("Open a channel that you may be interested in (case sensitive): ")
  if channel_search in user2_subscriptions: 
    channels_searched.append(channel_search)
    print("Channel found")
    corresponding_id = user2_subscriptions[channel_search]
    # https://www.geeksforgeeks.org/python-script-to-open-a-web-browser/
    # first import the module
    import webbrowser
    # then call the default open method described above
    print(corresponding_id)
    # Needs the www
    # new=1 opens in new tab
    webbrowser.open(f"www.youtube.com/channel/{corresponding_id}", new=1)
  else: print("Channel not found.")
  i = i + 1



"""
DONE:
input("Open a channel that you may be interested in: ")
user_subscription["id"]
open("youtube.com/c/{id}")

MAKE A DATABASE THAT HOLDS EACH USERS SUBSCRIPTIONS

IMPROVE THE DATABASE TO HOLD MORE USERS

add len(intersection) as another item to add to the database

LOAD IN ALL USERS AND COMPARE ALL USERS AGAINST SINGLE USER

TO DO:

"""


