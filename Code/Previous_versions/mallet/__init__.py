#coding: latin1
import io
import os
import random
import itertools

from thtpaths import internal_path


def is_retweet(word_list):
    """
    Usees the text in the tweet to check if its a retweet or not
    
    Empty tweets are retweets:
    >>> is_retweet([])
    True
    """
    if len(word_list) > 0:
        if word_list[0] == 'RT' and word_list[0] == '@':
            return True
        else:
            return False
    else:
        return True

def generate_save_path(internal_path, dirname, filename):
  """
  example:
  >>> generate_save_path("/home/user/data_dir/", "files", "file")
  '/home/user/data_dir/files/file.txt'
  """
  return os.path.join(internal_path, dirname, filename + ".txt")

def write_words(file_object, words):
  """
  writes words to a file

  A wordlist file consists of space seperated words:
  >>> from StringIO import * ;f=StringIO();write_words(f, [
  ... "one", "two" , "three"
  ... ]);f.getvalue()
  'one two three '

  Words that are None are not writen:

  >>> from StringIO import * ;f=StringIO();write_words(f, [
  ... "one", None, "two" , "three"
  ... ]);f.getvalue()
  'one two three '

  Words with utf-8 are encoded:

  >>> from StringIO import * ;f=StringIO();write_words(f, [
  ... u"ö"
  ... ]);f.getvalue()
  '\\xc3\\x83\\xc2\\xb6 '

  The wierd result for this example are because of the way StringIO always
  escape its content by it self.

  """
  file_object.write(" ".join(w.encode('utf8') for w in words if w != None)  + " ")

def save_words_to_path(internal_path, dirname, filename, words):
    """
    convinience wraper for the write_words and generate_save_path function 
    """
    save_path = generate_save_path(internal_path, dirname, filename) 
    with io.open(save_path, 'wb') as f:
        write_words(f, words)

def append_words_to_path(internal_path, dirname, filename, words):
    """
    open file on path in append mode and writes file list to the end of the file.
    """
    save_path = generate_save_path(internal_path, dirname, filename) 
    with io.open(save_path, 'ab') as f:
        write_words(f, words)
  

def saveToFile(word_list, filename, dirname):
        file_path = internal_path + dirname + '/'
        ofile = io.open(file_path + filename + '.txt', 'wb')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8') + ' ')
        ofile.close()


def updateFile(word_list, filename, dirname):
        file_path = internal_path + dirname + '/'
        word_list.insert(0, '\n')
        ofile = io.open(file_path + filename + '.txt', 'ab')
        for word in word_list:
            if word is not None:
                ofile.write(word.encode('utf8') + ' ')
        ofile.close()


def wordForTopics(word_dict, stemming):
    if stemming == u'lemma':
        if word_dict[u'lemma'] != '|':
            return (word_dict[u'lemma'].split('|'))[1]
        else:
            return word_dict[u'val']
    elif stemming == u'val':
        return word_dict[u'val']


def mergeFiles(filename_list, new_filename, dirname):
    file_path = internal_path + dirname + '/'
    newfile = io.open(file_path + new_filename + '.txt', 'wb')
    for filename in filename_list:
        ifile = io.open(file_path + filename + '.txt', 'rb')
        file_content = ifile.read()
        ifile.close()
        os.remove(file_path + filename + '.txt')
        newfile.wrte(file_content)
    newfile.close()


def overlaps(list1, list2):
    sb = set(list2)
    overlap = any(itertools.imap(sb.__contains__, list1))
    return overlap


def findCluster(cluster_dict, hashtags):
    new_cluster_dict = dict()
    anyOverlaps = False
    for key, value in cluster_dict.iteritems():
        if overlaps(value, hashtags):
            new_cluster_dict[key] = value
            anyOverlaps = True
    new_cluster_key = str(int(max(cluster_dict.keys(), key=int)) + 1)
    if anyOverlaps:
        return new_cluster_dict, new_cluster_key
    else:
        return dict(), new_cluster_key


def collapseSubCluster(cluster_dict, current_hashtags):
    hashtag_set = set(current_hashtags)
    for key, value in cluster_dict.iteritems():
        hashtag_set.update(value)
    return list(hashtag_set)


def collapsedKeys(cluster_dict):
    key_list = []
    for key in cluster_dict.iterkeys():
        key_list.append(key)
    return key_list


def updateFilesReturnNewDictElem(cluster_dict, hashtags, word_list, dirname):
    isNotEmpty = (cluster_dict and True) or False
    if not isNotEmpty:
        saveToFile(word_list, '1', dirname)
        return cluster_dict, ['1', hashtags]
    else:
        sub_cluster_dict, new_key = findCluster(cluster_dict, hashtags)
        isNotEmpty = (sub_cluster_dict and True) or False
        if not isNotEmpty:
            saveToFile(word_list, new_key, dirname)
            return sub_cluster_dict, [new_key, hashtags]
        else:
            sub_cluster_files = collapsedKeys(sub_cluster_dict)
            new_hashtags = collapseSubCluster(sub_cluster_dict, hashtags)
            updateClusterFiles(sub_cluster_files, word_list, new_key, dirname)
            return sub_cluster_dict, [new_key, new_hashtags]


def updateClusterFiles(sub_cluster_files, word_list, new_key, dirname):
    file_path = internal_path + dirname + '/'
    tempfile = io.open(file_path + 'temp' + '.txt', 'wb')
    for word in word_list:
        if word is not None:
            tempfile.write(word.encode('utf8') + ' ')
    tempfile.close()
    sub_cluster_files.append('temp')
    mergeFiles(sub_cluster_files, new_key, dirname)


def file_to_list(filename):
    word_list = []
    ifile = io.open(internal_path + filename + '.txt', 'r')
    for word in ifile:
        word_list.append(word.replace('\n', ''))
    ifile.close()
    return word_list


# The following function gathers non-pldebatt and
# non-username words from tweets,
# groups them by TWEETS and saves them to a file.
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerTweet(users, dirname):
    no_go_list = (
        file_to_list('english_stoplist') +
        file_to_list('swedish_stoplist') +
        file_to_list('domain_word_list')
    )
    for user in users:
        if u'text' in user:
            for text in user[u'text']:
                if u'mentions' in text:
                    mentions_list = text[u'mentions'].split('|')
                else:
                    mentions_list = []
                if u'hashtags' in text:
                    if "pldebatt" in text[u'hashtags']:
                        tweet_words = []
                        tweet_id = text[u'id']
                        if u'sentence' in text:
                            for sentence in text[u'sentence']:
                                if u'w' in sentence:
                                    for word in sentence[u'w']:
                                        if u'val' in word:
                                            word_cond = word[u'val'] != 'pldebatt' and \
                                                        word[u'val'] not in mentions_list and \
                                                        word[u'val'] not in no_go_list
                                            if word_cond:
                                                tweet_words.append(wordForTopics(word, u'lemma'))
                        if tweet_words:
                            saveToFile(tweet_words, tweet_id, dirname)


# The following function gathers non-pldebatt and
# non-username words from tweets,
# groups them by USER and saves them to a file.
# No metadata is saved. Filtering on tweets based on #pldebatt
def save_words_per_user(users, dirname):
    no_users = 0
    for user in users:
        user_words = []
        if u'username' in user:
            texts = user.get(u'text', [])
            for text in texts:
                if "pldebatt" in text.get(u'hashtags', []):
                    for sentence in text.get(u'sentence', []):
                        for word in sentence.get(u'w', []):
                            if u'val' in word:
                                user_word = wordForTopics(word, u'lemma')
                                user_words.append(user_word)
            if len(user_words) > 0:
              username = user[u'username']
              saveToFile(user_words, username, dirname)
              no_users += 1
    print "number of LDA documents: ", no_users


# The following function gathers non-pldebatt and
# non-username words from tweets,
# groups them by USER and saves them to a file.
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerHashtag(users, dirname):
    no_go_list = (
        file_to_list('english_stoplist') +
        file_to_list('swedish_stoplist') +
        file_to_list('domain_word_list')
    )
    retweets = 0
    tweets = 0
    for user in users:
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
                    hashtags = []
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []
                    if u'hashtags' in text:
                        if text[u'hashtags'] != '|#pldebatt|':
                            hashtags_temp = text[u'hashtags'].split('|')
                            hashtags = hashtags_temp[1:len(hashtags_temp) - 1]
                        else:
                            hashtags = [u'noHashtag']
                        if "pldebatt" in text[u'hashtags']:
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                word_cond = word[u'val'] != 'pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list

                                                if word_cond:
                                                    if word[u'val'] == u'RE':
                                                        print 'retweet'
                                                    tweet_words.append(wordForTopics(word, u'lemma'))
                    if len(tweet_words) > 0:
                        tweets += 1
                        if not is_retweet(tweet_words):
                            for hashtag in hashtags:
                                if hashtag != u'#pldebatt':
                                    updateFile(tweet_words, hashtag, dirname)
                        else:
                            retweets += 1
    print "Number of retweets: ", retweets
    print "Number of tweets: ", tweets


def saveWordsPerReply(users, dirname):
    no_go_list = (
        file_to_list('english_stoplist') +
        file_to_list('swedish_stoplist') +
        file_to_list('domain_word_list')
    )
    no_of_replies = 0
    for user in users:
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []
                    if u'hashtags' in text:
                        if "pldebatt" in text[u'hashtags']:
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                word_cond = word[u'val'] != 'pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list
                                                if word_cond:
                                                    tweet_words.append(wordForTopics(word, u'lemma'))

                    if len(tweet_words) > 0:
                        if u'id' in text:
                            tweet_id = text[u'id']
                        else:
                            tweet_id = 'noid'
                        if u'replytostatus' not in text:
                            if os.path.exists(internal_path + dirname + '/' + tweet_id + '.txt'):
                                updateFile(tweet_words, tweet_id, dirname)
                            else:
                                saveToFile(tweet_words, tweet_id, dirname)
                        else:
                            no_of_replies += 1
                            reply_status_id = text[u'replytostatus']
                            print reply_status_id, tweet_id
                            if os.path.exists(internal_path + dirname + '/' + reply_status_id + '.txt'):
                                updateFile(tweet_words, reply_status_id, dirname)
                            else:
                                saveToFile(tweet_words, reply_status_id, dirname)
    print 'no of replies: ', no_of_replies


# The following function gathers non-pldebatt
# and non-username words from tweets,
# groups them by USER and saves them to a file.
# No metadata is saved. Filtering on tweets based on #pldebatt
def saveWordsPerHashtagCluster(users, dirname):
    no_go_list = (
        file_to_list('english_stoplist') +
        file_to_list('swedish_stoplist') +
        file_to_list('domain_word_list')
    )
    cluster_dict = dict()
    for user in users:
        if u'username' in user:
            if u'text' in user:
                for text in user[u'text']:
                    tweet_words = []
                    hashtags = []
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []
                    if u'hashtags' in text:
                        if u'#pldebatt' in text[u'hashtags']:
                            if text[u'hashtags'] != '|#pldebatt|':
                                hashtags_temp = text[u'hashtags'].split('|')
                                hashtags = hashtags_temp[1:len(hashtags_temp) - 1]
                                if u'#pldebatt' in hashtags:
                                    hashtags.remove(u'#pldebatt')
                            else:
                                hashtags = [u'noHashtag']
                            if u'sentence' in text:
                                for sentence in text[u'sentence']:
                                    if u'w' in sentence:
                                        for word in sentence[u'w']:
                                            if u'val' in word:
                                                word_cond = word[u'val'] != 'pldebatt' and \
                                                            word[u'val'] not in mentions_list and \
                                                            word[u'val'] not in no_go_list
                                                if word_cond:
                                                    tweet_words.append(wordForTopics(word, u'lemma'))
                    if len(tweet_words) > 0 and hashtags != [u'noHashtag']:
                        toDelete, keyValPair = updateFilesReturnNewDictElem(cluster_dict, hashtags, tweet_words, dirname)
                        isNotEmpty = (toDelete and True) or False
                        if isNotEmpty:
                            for key in toDelete.iterkeys():
                                del cluster_dict[key]
                        cluster_dict[keyValPair[0]] = keyValPair[1]
    print 'dict: ', cluster_dict


# The following function gathers non-username words from ALL tweets, groups them by user and saves them to a file.
# No metadata is saved. No filtering on the tweets is made.
def saveWordsPerUserAll(users, dirname):
    no_go_list = file_to_list('english_stoplist') + file_to_list('swedish_stoplist')
    no_users = 0
    for user in users:
        user_words = []
        if u'username' in user:
            username = user[u'username']
            if u'text' in user:
                for text in user[u'text']:
                    if u'mentions' in text:
                        mentions_list = text[u'mentions'].split('|')
                    else:
                        mentions_list = []
                    if u'sentence' in text:
                        for sentence in text[u'sentence']:
                            if u'w' in sentence:
                                for word in sentence[u'w']:
                                    if u'val' in word:
                                        if word[u'val'] not in mentions_list and word[u'val'] not in no_go_list:
                                            user_words.append(wordForTopics(word, u'lemma'))
        if u'username' in user:
            username = user[u'username']
        else:
            username = str(random.randint(1, 10000))
        if user_words:
            saveToFile(user_words, username, dirname)
        user_words = []
        no_users += 1
    print "number of LDA documents: ", no_users


if __name__ == "__main__":
    import thtdb
    db = thtdb.ThtConnection(host='squib.de', dbName='karinas_twitter_db', collectionName='twitter-pldebatt-131006-new')
    save_words_per_user(db.collection.find(), 'testaggreply')
