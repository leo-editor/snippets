"""
get_tips.py - download current tips from GitHub

NOTE: if the list of tips gets long enough, GitHub may stop serving them
all in a single request, and serve them page by page - not hard to
handle if it happens.

Terry Brown, terrynbrown@gmail.com, Thu Dec  7 09:10:54 2017
"""

from collections import namedtuple

import requests

Tip = namedtuple('Tip', 'title tip tags')

URL = "https://api.github.com/repos/leo-editor/leo-editor/issues?labels=Tip&state=closed"

# for dev., use open tips
URL = URL.replace('closed', 'open')

def get_tips(data):
    """get_tips - get tips from GitHub issues

    :param dict data: GitHub API issues list
    :return: list of Tips
    """
    tips = []
    for issue in data:
        if '\n' in issue['body']:
            tip, tags = issue['body'].strip().rsplit('\n', 1)
        else:
            tip, tags = issue['body'].strip(), ''
        if tags.lower().startswith('tags:'):
            tags = [i.strip().strip('.') for i in tags[5:].split(',')]
        else:
            tags = []
            tip = "%s\n%s" % (tip, tags)
        tips.append(Tip(issue['title'], tip, tags))
    return tips


def main():
    data = requests.get(URL).json()
    for tip in get_tips(data):
        print('-'*40)
        print("%s\n%s\n%s\n" % (
            tip.title, tip.tags or "**NO TAGS FOR TIP**", tip.tip))

if __name__ == '__main__':
    main()
