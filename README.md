# Kindling
Uses data from social medias to connect and make friends.

![image](https://user-images.githubusercontent.com/36944031/170806373-e4292064-7f43-4c0c-964a-17ef2087aed5.png)


# Instructions
1. Get an API key by following this video: <a href="http://www.youtube.com/watch?feature=player_embedded&v=th5_9woFJmk
" target="_blank"><img src="http://img.youtube.com/vi/th5_9woFJmk/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="240" height="180" border="10" /></a>. Once you have it put it in [`api_key.txt`](/api_key.txt).
2. Go to https://www.youtube.com/account_privacy, uncheck "Keep all my subscriptions private". (Alternatively, the person running the script can authenticate by logging in. Your friends need to give you their Channel IDs though.)
3. Go to https://www.youtube.com/account_advanced to get your Channel ID, and tell your friends to do steps 1 & 2, and have them send you their Channel IDs to add to the [`youtube_channel_ids.txt`](/youtube_channel_ids.txt).
4. The person running the script should have their YouTube Channel ID as the first line in [`youtube_channel_ids.txt`](/youtube_channel_ids.txt). (Even if you choose to authenticate by logging in)
5. Add your friends or potential friends' IDs to the next lines.
6. Run v5.py

# To Do:
* Add Reddit API, TikTok
* Make it a web app
* Store users subscriptions to a database to find new friends that have previously used the website
* Add messaging functionality OR allow people to add their social medias so they can now make friends :)

