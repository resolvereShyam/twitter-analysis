import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def usage():
    print "USAGE"
    print "python tweet_sentiment.py <sentiment scores file> <twitter output json file>"

def getScores(fileName):
    afinnfile = open(fileName)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    
    return scores
    print scores.items() # Print every (term, score) pair in the dictionary

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

def calcSent(scores,tweetsText):
    sents = 0.0*len(tweetsText)
    for item in tweetsText:
        scoreSum = 0
        for word in item.split():
            wordScore = scores.get( word.encode('utf-8').lower(), 0)
            scoreSum = scoreSum+wordScore
        print scoreSum

def main():
    if len(sys.argv)<3:
        usage()
        sys.exit()
    
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    
    scores = getScores(sent_file)
    tweets,tweetsText = readTweets(tweet_file)
    calcSent(scores,tweetsText)
    # tweetsText = tweets[:]['text']
    # print tweetsText[0]
if __name__ == '__main__':
    main()
