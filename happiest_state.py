''' Problem 3 of week 1 assignment
    Derive the sentiment of new terms
    The approach that I am using is to first estimate whether each tweet is overall positive/negative
    Then, for every tweet, whenever a term is not in the AFINN-111 list, the tweest sentiment score  
    is checked. The number of positive and negative tweets that a non-AFINN-111 term appears in is
    counted, and the ratio of positive to negative is used to calculate the term score.
    
    USAGE
    python term_sentiment.py <sentiment scores file> <twitter output json file>
'''
import sys
import json
import operator
# from geopy.geocoders import Nominatim

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

stateScores = {
        'AK': 0,
        'AL': 0,
        'AR': 0,
        'AS': 0,
        'AZ': 0,
        'CA': 0,
        'CO': 0,
        'CT': 0,
        'DC': 0,
        'DE': 0,
        'FL': 0,
        'GA': 0,
        'GU': 0,
        'HI': 0,
        'IA': 0,
        'ID': 0,
        'IL': 0,
        'IN': 0,
        'KS': 0,
        'KY': 0,
        'LA': 0,
        'MA': 0,
        'MD': 0,
        'ME': 0,
        'MI': 0,
        'MN': 0,
        'MO': 0,
        'MP': 0,
        'MS': 0,
        'MT': 0,
        'NA': 0,
        'NC': 0,
        'ND': 0,
        'NE': 0,
        'NH': 0,
        'NJ': 0,
        'NM': 0,
        'NV': 0,
        'NY': 0,
        'OH': 0,
        'OK': 0,
        'OR': 0,
        'PA': 0,
        'PR': 0,
        'RI': 0,
        'SC': 0,
        'SD': 0,
        'TN': 0,
        'TX': 0,
        'UT': 0,
        'VA': 0,
        'VI': 0,
        'VT': 0,
        'WA': 0,
        'WI': 0,
        'WV': 0,
        'WY': 0
}

def lines(fp):
    print str(len(fp.readlines()))

def usage():
    print "USAGE"
    print "python term_frequency.py <twitter output json file>"

def readTweets(fileName):
    tweets = []
    tweetsText = []
    tweetsFile = open(fileName, "r")
    for line in tweetsFile:
        try:
            tweet = json.loads(line)
            tweets.append(tweet)
            tweetsText.append(tweet['text'])
        except:
            continue
    
    return tweets, tweetsText

def getScores(fileName):
    afinnfile = open(fileName)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    
    return scores
    print scores.items() # Print every (term, score) pair in the dictionary

def calcSent(scores,tweets,tweetsText):
    tweetsSent = [0]*len(tweets)
    for index,item in enumerate(tweetsText):
        scoreSum = 0
        for word in item.split():
            wordScore = scores.get( word.encode('utf-8').lower(), 0)
            scoreSum = scoreSum+wordScore
        tweetsSent[index] = scoreSum
    return tweetsSent

def checkUS(tweets,tweetsSent):
    tweetInUS = [False]*len(tweets)
    for index,tweet in enumerate(tweets):
            # Not using coordinate data since including polygons for boundaries in code
            # here would take up too much space
            # if 'coordinates' in tweet.keys():
                # if tweet['coordinates'] != None:
                    # print tweet['coordinates']['coordinates']
                    # # Disable below code to use geopy to resolve state from coordinates
                    # # coords = tweet['coordinates']['coordinates']
                    # # geolocator = Nominatim()
                    # # address = geolocator.reverse("{0:}, {1:}".format(coords[0],coords[1])).address
                    # # if address != None:
                        # # address = address.encode('utf-8')
                        # # for word in address.split():
                            # # if word in states.keys() or word in states.items():
                                # # print address
            if 'user' in tweet.keys():
                if tweet['user']['location'] != None:
                    unicLoc = tweet['user']['location'].encode('utf-8')
                    for word in unicLoc.split():
                        if word in states.keys():
                            tweetInUS[index] = True
                            stateScores[word] = stateScores[word] + tweetsSent[index]
                            continue
            if 'place' in tweet.keys():
                if tweet['place'] != None:
                    name = tweet['place']['full_name'].encode('utf-8')
                    for word in name.split():
                        if word in states.keys():
                            tweetInUS[index] = True
                            stateScores[word] = stateScores[word] + tweetsSent[index]
    return tweetInUS

def main():
    if len(sys.argv)<3:
        usage()
        sys.exit()
    
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    
    scores = getScores(sent_file)
    tweets,tweetsText = readTweets(tweet_file)
    tweetsSent = calcSent(scores,tweets,tweetsText)
    tweetInUS = checkUS(tweets,tweetsSent)
    
    # for key in stateScores.keys():
       # print states[key], stateScores[key]
    
    #   Get key of state with maximum positive score
    print max(stateScores.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
    main()
