from search import Query
from scraper import *
from connection-consts import MY_DB
import mysql.connector
import os
import sys

def notify(title, subtitle, text):
    """
    Creates a system notification with a title, subtitle, and body.

    Parameter title: the title of the notification
    Precondition: title is a string

    Parameter subtitle: the subtitle of the notification
    Precondition: subtitle is a string

    Parameter text: the body of the notification
    Precondition: body is a string
    """
    os.system("""osascript -e 'display notification "{}" with title "{}" subtitle "{}"'""".format(text,title,subtitle))


query = Query(sys.argv[1])
t = int(sys.argv[2])

for x in getRecents(query,MY_DB,t):
    notify('Goblin','New item!', x[0] + ', ' + x[4] + ' - $' + str(x[1]))
