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

def countTermsOcc(tweetsText):
    termsOcc = {}
    for tweetText in tweetsText:
        for word in tweetText.split():
            unicodeWord = word.encode('utf-8').lower()
            if unicodeWord not in termsOcc.keys():
                if unicodeWord not in termsOcc.keys():
                    termsOcc[unicodeWord] = 1
                else:
                    termsOcc[unicodeWord] = termsOcc[unicodeWord] + 1
    return termsOcc

def main():
    if len(sys.argv)<2:
        usage()
        sys.exit()
    
    tweet_file = sys.argv[1]
    
    tweets,tweetsText = readTweets(tweet_file)

    termsOcc = countTermsOcc(tweetsText)
    totalOcc = 0
    for key in termsOcc.keys():
        totalOcc = totalOcc + termsOcc[key]
    for key in termsOcc.keys():
        print '{0:100} {1:3f}'.format(key, termsOcc[key]/float(totalOcc) )

if __name__ == '__main__':
    main()
