professorep
===========

A Twitter bot that performs sentiment analysis of the given Middlebury professor's course evaluation comments on middkid.com.  Currently a proof-of-concept/alpha (see @ProfessoRep on Twitter).  In order to operate at any real scale, however, you'd need to add basic database support so queries don't constantly hammer middkid.com.

Usage
-----

professor_sentiment.py scrapes middkid.com's course evaluations given a professor name every time it's called, and professorep.py searches for and replies to any tweets with #middprof and a professor name (calling professor_sentiment.py).  

So to use, fill out the Twitter API information in professorep.py, modify references to @ProfessoRep to point to your own bot's account (and optionally change all references to #middprof to your own hashtag), and have a webserver cron run professorep.py every few minutes to search for new tweets with #middprof (or whatever you changed it to).  For help setting up the bot on Dreamhost (what I did), refer to the guide by Al Sweigart that I used at http://bit.ly/H36W5s.

Depends on the following Python libraries: mechanize, BeautifulSoup, HTMLParser, sys, urllib, json, os, twitter, time, and re.