import tweepy

# All confidential info replaced with ###

CONSUMER_KEY = '###'
CONSUMER_SECRET = '###'
ACCESS_TOKEN = '###'
ACCESS_TOKEN_SECRET = '###'

# OAuth v1.0a, using tweepy
client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

user_id = 1664869203852288001
target_user_id = 1053194859102769153

# getting the list of accounts that I am following
client.get_users_following(id=user_id, user_auth=True)

# unfollowing : using my account, unfollow target account
client.unfollow_user(target_user_id=target_user_id, user_auth=True)

# following : using my account, follow target account
client.follow_user(target_user_id=target_user_id)

# sending DMs : using my account, send DMs to target account
client.create_direct_message(participant_id=target_user_id, text="testtest")

# OAuth 2.0
# build handler
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id='###',
    redirect_uri="https://example.org",
    scope=["follows.read", "follows.write",
           "users.read", "tweet.read",
           "offline.access",
           "dm.write", "dm.read"],
    client_secret='###'
)
print(oauth2_user_handler.get_authorization_url())
access_token = oauth2_user_handler.fetch_token(
    "###")

client = tweepy.Client("###")
client.get_users_following(id=1664869203852288001, user_auth=False)

client.unfollow_user(target_user_id=1664869203852288001, user_auth=False)

client.follow_user(target_user_id=target_user_id, user_auth=False)

client.create_direct_message(participant_id=target_user_id, text="testing with OAuth 2.0", user_auth=False)


##########################
# testing 3-legged oauth #
##########################

oauth1_user_handler = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET,
    callback="https://example.org"
)

print(oauth1_user_handler.get_authorization_url())


# oauth_token=###
# oauth_verifier=###

access_token, access_token_secret = oauth1_user_handler.get_access_token(
    "###"
)

client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# test_user_id=1053194859102769153
# getting the list of accounts that I am following
client.get_users_following(id=1053194859102769153, user_auth=True)
# not working

# unfollowing : using my account, unfollow target account
# target_user_id: 1664869203852288001
client.unfollow_user(target_user_id=1664869203852288001, user_auth=True)

# following : using my account, follow target account
client.follow_user(target_user_id=1664869203852288001)

# sending DMs : using my account, send DMs to target account
client.create_direct_message(participant_id=1664869203852288001, text="yayaya")


# OAuth2
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id='###',
    redirect_uri="https://example.org",
    scope=["follows.read", "follows.write",
           "users.read", "tweet.read",
           "offline.access"],
    client_secret='###'
)

print(oauth2_user_handler.get_authorization_url())

access_token = oauth2_user_handler.fetch_token(
  "###"
)

client = tweepy.Client("###")

user_id=1053194859102769153 # DoWonKim13
target_user_id=1552978311550500865 # eclair7b
client.get_users_following(id=user_id)
## does not work => to figure out !

client.unfollow_user(target_user_id=target_user_id, user_auth=False)

client.follow_user(target_user_id=target_user_id, user_auth=False)

client.create_direct_message(participant_id=target_user_id, text="Hi my friend", user_auth=False)
# forbidden
# if scope list includes "dm.write" - it works
