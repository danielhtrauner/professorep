"""
professor_sentiment.py

Uses middkid.com course evaluation comments
in order to obtain an approximate sentiment
value for any given Middlebury professor,
generating a tweet-length string with the
resulting sentiment information.

Created by Daniel Trauner on 2013-08-18.
Copyright (c) 2013 Daniel Trauner. All rights reserved.
"""

import mechanize
from BeautifulSoup import BeautifulSoup
import HTMLParser
import sys
import urllib
import json

def get_eval_links(professor_name):
	'''
	Given a professor name, returns an array
	containing a link object for the eval page
	for each of the courses he or she teaches.
	'''
	br = mechanize.Browser()
	evals_search = br.open('http://middkid.com/course-evaluations/')

	br.form = list(br.forms())[0]
	br.form.controls[2].value = professor_name
	response = br.submit()

	last_course=0
	for link in list(br.links()):
		if link.text != 'Contact Us':
			last_course+=1
		else:
			break

	return list(br.links())[58:last_course]

def get_comments_string(eval_links):
	'''
	Given a list of eval link objects, returns
	a string containing the concatenation of 
	all course eval comments.
	'''
	all_eval_comments = ''

	br = mechanize.Browser()
	h = HTMLParser.HTMLParser()
	for eval_link in eval_links:
		eval_page = br.open(eval_link.url)
		soup = BeautifulSoup(eval_page)
		for tag in soup.findAll('blockquote'):
			raw_comment = ''.join(tag.findAll(text=True))
			comment = h.unescape(raw_comment).strip()
			if comment != 'No Comment':
				all_eval_comments += comment + ' '

	return all_eval_comments

def get_sentiment(comments):
	'''
	Given a string, returns its sentiment data
	in a Python dictionary using the API at
	text-processing.com.
	'''
	br = mechanize.Browser()
	if comments:
		words = len(comments.split(' '))

		json_response = br.open('http://text-processing.com/api/sentiment/', urllib.urlencode({'text' : comments.encode('utf-8')})).read()

		sentiment_dict = json.loads(json_response)

		if sentiment_dict['label'] == 'pos':
			overall = 'positive'
		elif sentiment_dict['label'] == 'neg':
			overall = 'negative'
		else:
			overall = 'neutral'

		result = {
					'words' : words,
					'overall' : overall,
					'positive' : (sentiment_dict['probability'])['pos'],
					'negative' : (sentiment_dict['probability'])['neg'],
					'neutral' : (sentiment_dict['probability'])['neutral']
				 }

	else:
		sys.exit()

	return result
	
def reply_tweet(professor_name):
	'''
	Returns the string the Twitter bot should
	reply with in response to the given query
	(professor name).
	'''
	eval_links = get_eval_links(professor_name)
	comments_string = get_comments_string(eval_links)
	sentiment = get_sentiment(comments_string)

	return 'Across ' + str(sentiment['words']) + ' words of comments on Prof. ' + professor_name.title() + ', the consensus is ' + sentiment['overall'] + ' (' + str(round(sentiment['positive']*100, 2)) + '% pos | ' + str(round(sentiment['negative']*100, 2)) + '% neg).'

def main(argv):
	print reply_tweet(argv[0])

if  __name__ =='__main__':
	main(sys.argv[1:])