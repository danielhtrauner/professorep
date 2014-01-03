"""
professorep.py

Runs the Twitter account @ProfessoRep, replying to any
@ProfessoRep tweets containing the hashtag "#middprof"
with the result of running professor_sentiment.py with 
the last name directly following #middprof.

*** Note: This is a modified version of the yhobos_script.py
script located at http://bit.ly/H36W5s.  Original credit goes 
to Al Sweigart -- his tutorial on Python Twitter bots was
incredibly helpful!

Modified by Daniel Trauner on 2013-08-18.
"""

# had to do this to fix a few errors related to Dreamhost...
import sys
import os
sys.path.append('/home/<USERNAME>/<PATH>')
sys.path.append('/home/<USERNAME>/.pythonbrew/pythons/Python-2.7.3/lib/python2.7/site-packages/*')
os.chdir('/home/<USERNAME>/<PATH>')

LATESTFILE = 'last.txt'
LOGFILE = 'log.txt'

from professor_sentiment import reply_tweet
import twitter
import time
import re

api = twitter.Api(consumer_key='XXXXX',
                  consumer_secret='XXXXX',
                  access_token_key='XXXXX',
                  access_token_secret='XXXXX')

# grab the last ID that the bot replied to, so it doesn't reply to earlier posts. (spam prevention measure)
if os.path.exists(LATESTFILE):
    fp = open(LATESTFILE)
    lastid = fp.read().strip()
    fp.close()

    if lastid == '':
        lastid = 0
else:
    lastid = 0

# perform the search
results = api.GetSearch('@ProfessoRep #middprof', since_id=lastid)
if len(results) == 0:
    sys.exit()
repliedTo = []

for statusObj in results:
    postTime = time.mktime(time.strptime(str(statusObj.created_at.encode('utf-8')[:-10]) + str(statusObj.created_at.encode('utf-8')[-4:]), '%a %b %d %H:%M:%S %Y'))

    if (time.time() - (24*60*60) < postTime):
        try:
            # get professor name as first word after "#middprof"
            professor_name = ''
            for i, word in enumerate(statusObj.text.split(' ')):
                if word == '#middprof':
                    professor_name = statusObj.text.split(' ')[i+1]
                    break

            # sanitize professor name
            if not re.match("^[a-zA-Z]+$", professor_name):
                re.split("[^a-zA-Z]*", professor_name)
                professor_name = ''.join(re.split("[^a-zA-Z]*", professor_name))

            reply_tweet = reply_tweet(professor_name)
            api.PostUpdate((str('@%s ' % (statusObj.user.screen_name)) + reply_tweet), in_reply_to_status_id=statusObj.id)
            repliedTo.append( (statusObj.id, statusObj.user.screen_name, statusObj.text.encode('ascii', 'replace')) )
            time.sleep(1)

        except Exception:
            print "Unexpected error:", sys.exc_info()[0:2]


fp = open(LATESTFILE, 'w')
fp.write(str(max([x.id for x in results])))
fp.close()

fp = open(LOGFILE, 'a')
fp.write('\n'.join(['%s|%s|%s' % (x[0], x[1], x[2]) for x in repliedTo]) + '\n')
fp.write('\n')
fp.close()