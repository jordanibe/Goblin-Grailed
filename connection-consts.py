import mysql.connector

MY_DB = mysql.connector.connect(
host='',            # input desired hostname
user='',            # input current/desired user (or root)
passwd='',          # input password corresponding to user
database=''         # input desired database to store queries
)

USER = ''  # input current/desired user for cronjob

DIR_PATH = 'cd /'         # input path to directory
PY_PATH = '/'   # input path to python