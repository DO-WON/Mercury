import os
import gzip
import shutil
import pandas as pd
import numpy as np
import json

# directory set
dir_name = '/Users/dowonkim/PycharmProjects/pythonProject2/hometimelines/'

def gz_extract(directory):
    extension = ".gz"
    os.chdir(directory)
    for item in os.listdir(directory): # loop through items in dir
      if item.endswith(extension): # check for ".gz" extension
          gz_name = os.path.abspath(item) # get full path of files
          file_name = (os.path.basename(gz_name)).rsplit('.',1)[0] #get file name for file within
          with gzip.open(gz_name,"rb") as f_in, open(file_name,"wb") as f_out:
              shutil.copyfileobj(f_in, f_out)
          os.remove(gz_name) # delete zipped file
## gz_extract(dir_name) # decompressed data replaced gzip files in directory


# json file
file_list = os.listdir(dir_name)
json_file = []
for file in file_list:
    json_file.append(dir_name + file)
    json_file.sort()

def df_for_R(file):
    with open(file, 'r', encoding='utf-8') as f:
        try:
            data_dict = json.load(f)
            # which user? :
            user_id = data_dict["userObject"]["id_str"]
            # number of friends that user has:
            user_friends_count = data_dict["userObject"]["friends_count"]

            # extract account id from the lists of home timeline tweets
            lists = data_dict["homeTweets"]
            # len(lists) # 781

            # tweet_id
            tweet_id = []
            for list in lists:
                tweet_id_str = list["id_str"]
                tweet_id.append(tweet_id_str)

            # len(pd.Series(tweet_id).drop_duplicates().tolist()) # 781 check

            # account_id
            account_id = []
            for list in lists:
                account_id_str = list["user"]["id_str"]
                account_id.append(account_id_str)

            tweet = pd.Series(tweet_id, name='tweet_id')
            account = pd.Series(account_id, name='account_id')

            user = pd.DataFrame({"user_id": pd.Series(np.tile(user_id, len(tweet_id))),
                                 "user_friends_count": pd.Series(np.tile(user_friends_count, len(tweet_id)))}
                                )
            df = pd.concat([user, tweet, account], axis=1)
            return df

        except BaseException as e:
            print('The file contains invalid JSON')


df = df_for_R(json_file[0]) # initial setting
for i in range(len(json_file)):
        df = pd.concat([df, df_for_R(json_file[i])], ignore_index=True)


print(df)

# df (data frame): user_id - each tweet from homeTweets (user-tweet) dyad
# user-level: user_id, friends_count
# tweet-level: tweet_id, account_id

len(df.user_id.unique())  # 60
len(df.account_id.unique())  # 15774

# export to csv files for R (visualization)
df.to_csv('/Users/dowonkim/Desktop/Mercury/Pilot/pilot_test/df.csv', index=False)

