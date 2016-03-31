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
    print "python term_sentiment.py <sentiment scores file> <twitter output json file>"

def getScores(fileName):
    afinnfile = open(fileName)
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.
    
    return scores

def readTweets(fileName):
    tweets = []
    tweetsText = []
    tweetsFile = open(fileName, "r")
    for line in tweetsFile:
        tweet = json.loads(line)
        tweets.append(tweet)
        if 'text' in tweet.keys():
            tweetsText.append(tweet['text'])
        else:
            tweetsText.append('')
    
    return tweets, tweetsText

def checkPosNeg(tweetsText, scores):
    tweetsPos = [False]*len(tweetsText)
    tweetsNeg = [False]*len(tweetsText)
    for index,tweetText in enumerate(tweetsText):
        for word in tweetText.split():
            word = word.encode('utf-8').lower()
            if word in scores:
                wordScore = scores.get( word, 0)
                if wordScore > 0:
                    tweetsPos[index] = True
                elif wordScore < 0:
                    tweetsNeg[index] = True
            if tweetsPos[index] and tweetsNeg[index]:
                continue
    return tweetsPos, tweetsNeg

def getNonDefTerms(tweetsText,scores,tweetsPos,tweetsNeg):
    nonDefTerms = {}
    termPos = {}
    termNeg = {}
    for index,tweetText in enumerate(tweetsText):
        for word in tweetText.split():
            word = word.encode('utf-8').lower()
            if word not in scores:
                if word not in nonDefTerms.keys():  #   Create item for term if not stored in dictionary
                    nonDefTerms[word] = 1
                    if tweetsPos[index]:
                        termPos[word] = 1
                    else:                           #   If the first tweet that the term comes from is not positive, the positive score is 0
                        termPos[word] = 0
                    if tweetsNeg[index]:
                        termNeg[word] = 1
                    else:                           #   If the first tweet that the term comes from is not negative, the negative score is 0
                        termNeg[word] = 0
                else:
                    nonDefTerms[word] = nonDefTerms[word] + 1
                    if tweetsPos[index]:
                        termPos[word] = termPos[word]+1
                    if tweetsNeg[index]:
                        termNeg[word] = termNeg[word]+1
    return nonDefTerms,termPos,termNeg

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
    # Establish whether tweets are positive, negative, both or neutral
    tweetsPos,tweetsNeg = checkPosNeg(tweetsText,scores)

    nonDefTerms,termPos,termNeg = getNonDefTerms(tweetsText,scores,tweetsPos,tweetsNeg)
    for key in nonDefTerms.keys():
        if termPos[key]==0:
            termPos[key] = 1
        if termNeg[key]==0:
            termNeg[key] = 1
        print key, float(termPos[key])/termNeg[key]

if __name__ == '__main__':
    main()
