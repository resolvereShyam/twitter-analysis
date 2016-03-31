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

def countHashOcc(tweets):
    hashOcc = {}
    for tweet in tweets:
        if 'entities' in tweet.keys():
            if 'hashtags' in tweet['entities'].keys():
                tags = tweet['entities']['hashtags']
                for tag in tags:
                    uniTag = tag['text'].encode('utf-8')
                    if uniTag not in hashOcc.keys():
                        hashOcc[uniTag] = 1
                    else:
                        hashOcc[uniTag] = hashOcc[uniTag] + 1
    return hashOcc

def main():
    if len(sys.argv)<2:
        usage()
        sys.exit()
    
    tweet_file = sys.argv[1]
    
    tweets,tweetsText = readTweets(tweet_file)
    
    # Get frequency of hashtags, sort by descending order and print out
    hashOcc = countHashOcc(tweets)
    sortdHashOcc = sorted(hashOcc.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(0,10):
        print sortdHashOcc[i][0],sortdHashOcc[i][1]

if __name__ == '__main__':
    main()
