from flask import Flask, request, render_template, redirect, abort, jsonify
import json
from feedgen.feed import FeedGenerator

from channels import *

app = Flask(__name__)

@app.route('/')
def index() -> str:
    return 'Hi!'

@app.route('/channels/', methods=['POST', 'GET'], defaults={'post_format': 'html', 'channel_id':None}, strict_slashes=False)
@app.route('/channels/<channel_id>/', methods=['PUT'], defaults={'data_format': 'html'}, strict_slashes=False)
def channels(post_format, channel_id) -> str:
    if request.method == 'POST':
        if post_format == 'html':
            data = request.form
        else:
            abort(500)
        
        validate_channel(data)

        insert_channel(data['title'], data['link'], data['description'], channel_id=channel_id, logger=app.logger.info)
        
        return redirect(request.url)
    else:
        return render_template('channels.html', channels=get_channels())

@app.route('/channels/<channel_id>/', methods=['POST', 'GET'], defaults={'data_format': 'html'}, strict_slashes=False)
@app.route('/channels/<channel_id>/<data_format>', methods=['POST', 'GET'])
def channel(channel_id, data_format) -> str:
    if request.method == 'POST':
        data = request.form
        
        validate_entry(data)

        insert_channel_entry(int(channel_id), data['title'], data['link'], data['description'], None, logger=app.logger.info)

        return redirect(request.url)
    else:
        channel_info = get_channel(channel_id)
        channel_entries = get_channel_entries(channel_id)

        if data_format == 'html':
            return render_template('channel_entries.html', title='', desciption='', entries=channel_entries)
        elif data_format =='json':
            return json.dumps(list(channel_entries))
        elif data_format in ['rss', 'atom']:
            return get_feed(channel_info, channel_entries, feed_fromat=data_format)
        else:
            abort(404)

def validate_channel(channel):
    valid = False
    for k in ['title', 'link', 'description']:
        if k not in channel or not channel[k]:
            raise Exception('Missing required channel elemeent %s' % k)

def validate_entry(entry, feed_format='rss'):
    valid = False
    entry_requirenments = {
        'rss': ['title', 'description'],
        'atom': ['id', 'title']
    }
    for k in entry_requirenments[feed_format]:
        if k in entry and entry[k]:
            valid = True
    if not valid:
        raise Exception('At least one of title or description must be present')

def make_error(status_code, sub_code, message, action):
    response = jsonify({
        'status': status_code,
        'sub_code': sub_code,
        'message': message,
        'action': action
    })
    response.status_code = status_code
    return response

def get_feed(channel_info, entries, feed_fromat='rss'):
    fg = FeedGenerator()
    fg.id(channel_info['channel_id'])
    fg.title(channel_info['title'])
    fg.link(href=channel_info['link'])
    fg.description(channel_info['description'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
