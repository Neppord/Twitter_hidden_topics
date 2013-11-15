#from bson.son import SON
import thtdb
import io
from thtpaths import internal_data_path
#from bson.code import Code
import random


def saveToFile(word_list, filename, dirname):
        file_path = internal_data_path+dirname+'/'
        #user_words_filename = internal_path+'/malletTwitterOctober/'+username
        ofile = io.open(file_path+filename+'.txt', 'wb')
        for word in word_list:
            ofile.write(word.encode('utf8')+' ')
        ofile.close()


def saveWordsPerUserPldebatt():
    count = 0
    user_stat = dict()
    hash_stat = dict()
    word_stat = dict()
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            count += 1
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                hash_list = user[u'text'][u'hashtags'].split('|')
                                if hash_list:
                                    for hashtag in hash_list:
                                        if hashtag != '#pldebatt' and hashtag!='':
                                            if hashtag in hash_stat:
                                                hash_stat[hashtag] += 1
                                            else:
                                                hash_stat[hashtag] = 1
                                if username in user_stat:
                                    user_stat[username] += 1
                                else:
                                    user_stat[username] = 1
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    if user[u'text'][u'sentence'][u'w'][u'val'] in word_stat:
                                                        word_stat[user[u'text'][u'sentence'][u'w'][u'val']] += 1
                                                    else:
                                                        word_stat[user[u'text'][u'sentence'][u'w'][u'val']] = 1
                                                    if user[u'text'][u'sentence'][u'w'][u'val']!='pldebatt':
                                                        user_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val'] in word_stat:
                                                            word_stat[word[u'val']] += 1
                                                        else:
                                                            word_stat[word[u'val']] = 1
                                                        if word[u'val']!='pldebatt':
                                                            user_words.append(word[u'val'])

                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val'] in word_stat:
                                                            word_stat[sentence[u'w'][u'val']] += 1
                                                        else:
                                                            word_stat[sentence[u'w'][u'val']] = 1
                                                        if sentence[u'w'][u'val']!='pldebatt':
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']:
                                                        if u'val' in word:
                                                            if word[u'val'] in word_stat:
                                                                word_stat[word[u'val']] += 1
                                                            else:
                                                                word_stat[word[u'val']] = 1
                                                            if word[u'val']!='pldebatt':
                                                                user_words.append(word[u'val'])
                    else:
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if "pldebatt" in text[u'hashtags']:
                                    hash_list = text[u'hashtags'].split('|')
                                    if hash_list:
                                        for hashtag in hash_list:
                                            if hashtag != '#pldebatt' and hashtag!='':
                                                if hashtag in hash_stat:
                                                    hash_stat[hashtag] += 1
                                                else:
                                                    hash_stat[hashtag] = 1
                                    if username in user_stat:
                                        user_stat[username] += 1
                                    else:
                                        user_stat[username] = 1
                                    if u'sentence' in text:
                                        if isinstance(text[u'sentence'], dict):
                                            if u'w' in text[u'sentence']:
                                                if isinstance(text[u'sentence'][u'w'], dict):
                                                    if u'val' in text[u'sentence'][u'w']:
                                                        if text[u'sentence'][u'w'][u'val'] in word_stat:
                                                            word_stat[text[u'sentence'][u'w'][u'val']] += 1
                                                        else:
                                                            word_stat[text[u'sentence'][u'w'][u'val']] = 1
                                                        if text[u'sentence'][u'w'][u'val']!='pldebatt':
                                                            user_words.append(text[u'sentence'][u'w'][u'val'])
                                                else:
                                                    for word in text[u'sentence'][u'w']:
                                                        if u'val' in word:
                                                            if word[u'val'] in word_stat:
                                                                word_stat[word[u'val']] += 1
                                                            else:
                                                                word_stat[word[u'val']] = 1
                                                            if word[u'val']!='pldebatt':
                                                                user_words.append(word[u'val'])
                                        else:
                                            for sentence in text[u'sentence']:
                                                if u'w' in sentence:
                                                    if isinstance(sentence[u'w'], dict):
                                                        if u'val' in sentence[u'w']:
                                                            if sentence[u'w'][u'val'] in word_stat:
                                                                word_stat[sentence[u'w'][u'val']] += 1
                                                            else:
                                                                word_stat[sentence[u'w'][u'val']] = 1
                                                            if sentence[u'w'][u'val']!='pldebatt':
                                                                user_words.append(sentence[u'w'][u'val'])
                                                    else:
                                                        for word in sentence[u'w']:
                                                            if u'val' in word:
                                                                if word[u'val'] in word_stat:
                                                                    word_stat[word[u'val']] += 1
                                                                else:
                                                                    word_stat[word[u'val']] = 1
                                                                if word[u'val']!='pldebatt':
                                                                    user_words.append(word[u'val'])
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, 'malletTwitterOctober')
        user_words = []



def saveWordsPerTweet(dirname):
    for user in db.collection.find():
        if u'username' in user:
            username = user[u'username']
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                tweet_words = []
                                tweet_id = user[u'text'][u'id']
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    if user[u'text'][u'sentence'][u'w'][u'val']!='pldebatt':
                                                        tweet_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt':
                                                            tweet_words.append(word[u'val'])

                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt':
                                                            tweet_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']: 
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt':
                                                                tweet_words.append(word[u'val'])
                                if tweet_words:
                                    saveToFile(tweet_words, tweet_id, 'malletTwitterLDAOctober')
                                user_words = []
                    else:
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if "pldebatt" in text[u'hashtags']:
                                    tweet_words = []
                                    tweet_id = text[u'id']
                                    if u'sentence' in text:
                                        if isinstance(text[u'sentence'], dict):
                                            if u'w' in text[u'sentence']:
                                                if isinstance(text[u'sentence'][u'w'], dict):
                                                    if u'val' in text[u'sentence'][u'w']:
                                                        if text[u'sentence'][u'w'][u'val']!='pldebatt':
                                                            tweet_words.append(text[u'sentence'][u'w'][u'val'])
                                                else:
                                                    for word in text[u'sentence'][u'w']:
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt':
                                                                tweet_words.append(word[u'val'])
                                        else:
                                            for sentence in text[u'sentence']:
                                                if u'w' in sentence:
                                                    if isinstance(sentence[u'w'], dict):
                                                        if u'val' in sentence[u'w']:
                                                            if sentence[u'w'][u'val']!='pldebatt':
                                                                tweet_words.append(sentence[u'w'][u'val'])
                                                    else:
                                                        for word in sentence[u'w']:
                                                            if u'val' in word:
                                                                if word[u'val']!='pldebatt':
                                                                    tweet_words.append(word[u'val'])
                                    if tweet_words:
                                        saveToFile(tweet_words, tweet_id, dirname)
                                    user_words = []


def saveWordsPerUser(dirname):
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        if u'hashtags' in user[u'text']:
                            if "pldebatt" in user[u'text'][u'hashtags']:
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    if user[u'text'][u'sentence'][u'w'][u'val']!='pldebatt':
                                                        user_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        if word[u'val']!='pldebatt':
                                                            user_words.append(word[u'val'])

                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt':
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']: 
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt':
                                                                user_words.append(word[u'val'])
                    else:
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if "pldebatt" in text[u'hashtags']:
                                    if u'sentence' in text:
                                        if isinstance(text[u'sentence'], dict):
                                            if u'w' in text[u'sentence']:
                                                if isinstance(text[u'sentence'][u'w'], dict):
                                                    if u'val' in text[u'sentence'][u'w']:
                                                        if text[u'sentence'][u'w'][u'val']!='pldebatt':
                                                            user_words.append(text[u'sentence'][u'w'][u'val'])
                                                else:
                                                    for word in text[u'sentence'][u'w']:
                                                        if u'val' in word:
                                                            if word[u'val']!='pldebatt':
                                                                user_words.append(word[u'val'])
                                        else:
                                            for sentence in text[u'sentence']:
                                                if u'w' in sentence:
                                                    if isinstance(sentence[u'w'], dict):
                                                        if u'val' in sentence[u'w']:
                                                            if sentence[u'w'][u'val']!='pldebatt':
                                                                user_words.append(sentence[u'w'][u'val'])
                                                    else:
                                                        for word in sentence[u'w']:
                                                            if u'val' in word:
                                                                if word[u'val']!='pldebatt':
                                                                    user_words.append(word[u'val'])
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []


def saveWordsPerUserAll(dirname):
    for user in db.collection.find():
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if True:
                if u'text' in user:
                    if isinstance(user[u'text'], dict): 
                        if u'hashtags' in user[u'text']:
                            if True:
                                if u'sentence' in user[u'text']:
                                    if isinstance(user[u'text'][u'sentence'], dict):
                                        if u'w' in user[u'text'][u'sentence']:
                                            if isinstance(user[u'text'][u'sentence'][u'w'], dict):
                                                if u'val' in user[u'text'][u'sentence'][u'w']:
                                                    user_words.append(user[u'text'][u'sentence'][u'w'][u'val'])
                                            else:
                                                for word in user[u'text'][u'sentence'][u'w']:
                                                    if u'val' in word:
                                                        user_words.append(word[u'val'])

                                    else:
                                        for sentence in user[u'text'][u'sentence']:
                                            if u'w' in sentence:
                                                if isinstance(sentence[u'w'], dict):
                                                    if u'val' in sentence[u'w']:
                                                        if sentence[u'w'][u'val']!='pldebatt':
                                                            user_words.append(sentence[u'w'][u'val'])
                                                else:
                                                    for word in sentence[u'w']: 
                                                        if u'val' in word:
                                                            user_words.append(word[u'val'])
                    else:
                        for text in user[u'text']:
                            if u'hashtags' in text:
                                if True:
                                    if u'sentence' in text:
                                        if isinstance(text[u'sentence'], dict):
                                            if u'w' in text[u'sentence']:
                                                if isinstance(text[u'sentence'][u'w'], dict):
                                                    if u'val' in text[u'sentence'][u'w']:
                                                        user_words.append(text[u'sentence'][u'w'][u'val'])
                                                else:
                                                    for word in text[u'sentence'][u'w']:
                                                        if u'val' in word:
                                                            user_words.append(word[u'val'])
                                        else:
                                            for sentence in text[u'sentence']:
                                                if u'w' in sentence:
                                                    if isinstance(sentence[u'w'], dict):
                                                        if u'val' in sentence[u'w']:
                                                            user_words.append(sentence[u'w'][u'val'])
                                                    else:
                                                        for word in sentence[u'w']:
                                                            if u'val' in word:
                                                                user_words.append(word[u'val'])
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []


if __name__ == "__main__":
    db = thtdb.ThtConnection(collectionName='test_pldebatt_june')
    #db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='import_steffen')
    #saveWordsPerUser('malletTwitterOctober')
    saveWordsPerUserAll('malletTwitterLDAJuneAll')
