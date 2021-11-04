from operator import itemgetter

from plotly.graph_objs import Bar
from plotly import offline

import requests

# Make an API call and store the response.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f'Status code: {r.status_code}')

# Process information about each submission.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
	# Make a separate API call for each submission.
	url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
	r = requests.get(url)
	print(f'id: {submission_id}\tstatus: {r.status_code}')
	response_dict = r.json()

	# Build a dictionary for each article.
	if 'descendants' in response_dict:
		submission_dict = {
    	'title': response_dict['title'],
    	'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
    	'comments': response_dict['descendants'],
    	}
		submission_dicts.append(submission_dict)

print(f'Submissions extracted: {len(submission_dicts)}')

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
	reverse=True)

# Make a visualization using Plotly lib.

article_links, comments = [], []

for submission_dict in submission_dicts:
	article_title = submission_dict['title']
	article_url = submission_dict['hn_link']
	article_link = f"<a href='{article_url}'>{article_title}</a>"
	article_links.append(article_link)

	comments.append(submission_dict['comments'])

data = [{
	'type': 'bar',
	'x': article_links,
	'y': comments,
	'marker': {
		'color': 'rgb(60, 100, 150)',
		'line':{'width': 1.5, 'color': 'rgb(25, 25, 25)'}
	},
	'opacity': 0.5,
}]

my_layout = {
	'title': 'Hottest Hacker News Articles',
	'xaxis': {
		'title': 'Article', 
		'titlefont': {'size': 24},
		'tickfont': {'size': 14}
	},
	'yaxis': {
		'title': 'Comments',
		'titlefont': {'size': 24},
		'tickfont': {'size': 14}
	}
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_top_articles.html')


