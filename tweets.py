"""Assignment 3: Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4

# Helper functions.

def alnum_prefix(text: str) -> str:
    """Return the alphanumeric prefix of text, converted to
    lowercase. That is, return all characters in text from the
    beginning until the first non-alphanumeric character or until the
    end of text, if text does not contain any non-alphanumeric
    characters.

    >>> alnum_prefix('')
    ''
    >>> alnum_prefix('IamIamIam')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!')
    'iamiamiam'
    >>> alnum_prefix('IamIamIam!!andMore')
    'iamiamiam'
    >>> alnum_prefix('$$$money')
    ''

    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.

    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'

    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


# Required functions

def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text, converted to lowercase, with
    duplicates included.

    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []
    """

    result = []
    tweet = text.split()
    for word in tweet:
        if word.startswith(MENTION_SYMBOL):
            mentioned_username = alnum_prefix(word[1:])
            if len(mentioned_username) > 0:
                result.append(mentioned_username)
    
    return result

def extract_hashtags(text: str) -> List[str]:
    """Return a list of all hashtags in text, converted to lowercase, 
    without duplicates.
    """

    result = []
    tweet = text.split()
    for word in tweet:
        if word.startswith(HASH_SYMBOL):
            hashtagged_word = alnum_prefix(word[1:])
            if len(hashtagged_word) > 0 and hashtagged_word not in result:
                result.append(hashtagged_word)
    
    return result

def count_words(text: str, words_to_count: Dict[str, int]) -> None:
    """ Updates the count of words in words_to_count by the number of 
    occurrences in text. If a word is not in words_to_count, create a new
    entry and start counting
    
    >>> message = "#UofT Nick Frosst: Google Brain re-searcher by day,\
    singer @goodkidband by night!"
    >>> d = {}
    >>> count_words(message, d)
    >>> d == {'nick': 1, 'frosst': 1, 'google': 1, 'brain': 1,
    'researcher': 1, 'by': 2, 'day': 1, 'singer': 1, 'night': 1}
    True
    """
    
    tweet = text.split()
    for word in tweet:
        if is_a_word(word):
            cleaned_word = clean_word(word)
            current_count = 0
            if cleaned_word in words_to_count:
                current_count = words_to_count[cleaned_word]
            current_count = current_count + 1
            words_to_count[cleaned_word] = current_count
                
def is_a_word(word: str) -> bool:
    is_word = False
    if not word.startswith(MENTION_SYMBOL) and not \
    word.startswith(HASH_SYMBOL) and not word.startswith(URL_START):
        is_word = True
    return is_word
    
def common_words(words_to_count: Dict[str, int], threshold: int) -> None:
    """ Modifies words_to_count by only including the most common words, 
    and the number of words less than threshold
    """
    num_occurrences = get_num_of_occurrences(words_to_count)
    for num in num_occurrences:
        if len(words_to_count) > threshold:
            remove_items_with_value(words_to_count, num)

def remove_items_with_value(words_to_count: Dict[str, int], 
                            value: int) -> None:
    """ Removes all keys in words_to_count that have a value of value
    """
    keys_to_remove = []
    for word in words_to_count:
        if words_to_count[word] == value:
            keys_to_remove.append(word)
    
    for key in keys_to_remove:
        words_to_count.pop(key)
    
  
def get_num_of_occurrences(words_to_count: Dict[str, int]) -> List[int]:
    """ Returns a list of all possible number of occurrences in 
    words_to_count
    """
    result = []
    for word in words_to_count:
        if words_to_count[word] not in result:
            result.append(words_to_count[word])
    result.sort()        
    return result

def read_tweets(tweets_file) -> Dict[str, List[tuple]]:
    user_tweets = {}
    username = ''
    tweet_details = []
    text = ''
    for line in tweets_file:
        if is_user_line(line):
            username = get_username(line)
            user_tweets[username] = []
        elif is_tweet_history_line(line):
            # parse line to get information
            # split lines at commas
            # get information, sort and store in tweet_details
            if len(tweet_details) == 0:
                tweet_details.extend(get_tweet_info(line))
        elif is_EOT_line(line):
            # put all tweet information in a typle
            # append to list for username
            # reset tweet_details and text
            if len(tweet_details) > 0:
                tweet_tup = (text, tweet_details[0], tweet_details[1], 
                            tweet_details[2], tweet_details[3])
                user_tweets[username].append(tweet_tup)
            tweet_details = []
            text = ''
        else:
            #tweet text line
            # concatenate everything in line in text
            text = text + line
    return user_tweets

    
def get_username(line: str) -> str:
    """ Returns the username converted to lowercase in line
    
    Precondition: The username is of format <username:>
    
    >>> tweet = 'UofTCompSci:'
    >>> get_username(tweet)
    uoftcompsci
    """
    end_index = line.find(':')
    return line[:end_index].lower()


def get_tweet_info(line: str) -> tuple:
    """ Returns the information from tweet in a tuple
    """
    info = line.split(',')
    result = []
    
    if len(info) > 0:
        date = int(info[0])
        result.append(date)
        source = info[2]
        result.append(source)
        fav_count = int(info[3])
        result.append(fav_count)
        rt_count = int(info[4].rstrip('\n'))
        result.append(rt_count)
    return result

def is_user_line(line: str) -> bool:
    """ Returns True if line is a username line, otherwise return False
    """
    
    return line.rstrip('\n').endswith(':')


def is_tweet_history_line(line: str) -> bool:
    """ Returns true if line is a tweet history line, i.e. contains 
    information about the tweet such as text, date, favourite count, etc.
    """
    
    if len(line) <= 1 or MENTION_SYMBOL in line or \
       HASH_SYMBOL in line or URL_START in line or '<<<EOT' in line:
        return False
    return line.rstrip('\n')[-1].isalnum()

def is_EOT_line(line: str) -> bool:
    """ Returns true if line is an end of tweet line, denoted by 
    '<<<EOT\n'
    """
    
    return '<<<EOT' in line

def most_popular(tweets_read: Dict[str, List[tuple]], start_date: int,
                end_date: int) -> str:
    """ Returns the most popular user based on most favourites and 
    retweets between start_date and end_date
    """
    highest_rating = 0
    author = 'tie'
    tweets_in_range = find_tweets_in_range(tweets_read, start_date, end_date)
    for user in tweets_in_range:
        popularity = tweets_in_range[user][TWEET_FAVOURITE_INDEX] + \
            tweets_in_range[user][TWEET_RETWEET_INDEX]
        if popularity > highest_rating:
            highest_rating = popularity
            author = user
        elif popularity == highest:
            author = 'tie'
    return author

def find_tweets_in_range(tweets_read: Dict[str, List[tuple]], 
                        start_date: int, 
                        end_date: int) -> Dict[str, List[tuple]]:
    """ Returns a dictionary mapping users from tweets_read, to tweets between 
    start and end
    """
    result = {}
    for username in tweets_read:
        for tweet in tweets_read[username]:
            if start_date <= tweet[TWEET_DATE_INDEX] <= end_date:
                if username not in result:
                    result[username] = []
                result[username].append(tweet)
    return result



def detect_author(tweets_read: Dict[str, List[tuple]], tweet: str) -> str:
    """ Returns the username of the most likely author given the use of 
    hashtags in tweet. If unknown, return 'unknown'
    """
    hashtags = extract_hashtags(tweet)
    hashtag_to_users = hashtag_count(tweets_read, tweet, hashtags)
    for hashtag in hashtag_to_user:
        possible_authors = hashtag_to_user[hashtag]
        author = possible_authors[0]
        if len(possible_authors) > 1:
            return 'Unknown'
    return author
    
def hashtag_count(tweets_read: Dict[str, List[tuple]], 
                tweet: str, hashtags: List[str]) -> Dict[str, List[str]]:
    """ Returns a dictionary mapping hashtags from tweets to a 
    list of users in tweets_read who used hashtags
    """
    result = {}
    for hashtag in hashtags:
        result[hashtag] = []
        for user in tweets_read:
            if hashtag in tweets_read[user]:
                result[hashtag].append(user)
    return result
    

# TODO: Add the remaining Assignment 3 functions below.


if __name__ == '__main__':
    pass

    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    # import doctest
    # doctest.testmod()
