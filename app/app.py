from flask import Flask, request, render_template
import json
from feedgen.feed import FeedGenerator

from channels import *

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return 'Hi!'

@app.route('/channels', methods=['POST', 'GET'], defaults={'post_format': 'html'}, strict_slashes=False)
def channels(post_format) -> str:
    if request.method == 'POST':
        if post_format == 'html':
            data = request.form
        else:
            raise Exception('Only form data or json POST are alowed.')

        insert_channel(data['title'], data['description'], logger=app.logger.info)
        
    return render_template('channels.html', channels=get_channels())

def get_feed(entries, feed_fromat='rss'):
    fg = FeedGenerator()
    fg.id('id')
    fg.title('title')
    fg.link(href='link')
    fg.description('description')
    for entry in entries:
        fe = fg.add_entry()
        fe.id(str(entry['entry_id']))
        fe.title(entry['title'])
        fe.link(href=entry['link'])
        fe.description(entry['description'])
    if feed_fromat == 'rss':
        return fg.rss_str(pretty=True)
    elif feed_fromat == 'atom':
        return fg.atom_str(pretty=True)
    else:
        raise Exception()

@app.route('/channels/<channel_id>', methods=['POST', 'GET'], defaults={'response_format': 'html'}, strict_slashes=False)
@app.route('/channels/<channel_id>/<response_format>', methods=['POST', 'GET'])
def channel(channel_id, response_format) -> str:
    app.logger.info(channel_id)
    if request.method == 'POST':
        if response_format == 'html':
            data = request.form
        elif response_format =='json':
            data = request.get_json(force=True, silent=True)
        else:
            raise Exception('Only form data or json POST are alowed.')

        insert_channel_entry(int(channel_id), data['title'], data['link'], data['description'], None, logger=app.logger.info)

    channel_entries = get_channel_entries(channel_id)

    if response_format == 'html':
        return render_template('channel_entries.html', title='', desciption='', entries=channel_entries)
    elif response_format =='json':
        return json.dumps(list(channel_entries))
    elif response_format in ['rss', 'atom']:
        return get_feed(channel_entries, feed_fromat=response_format)
    else:
        raise Exception()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
