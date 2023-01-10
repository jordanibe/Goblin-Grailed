import crontab
from connection-consts import *

q = input('Search for product: ') ## input to make Query object
t = input('How often (minutes) should Goblin update you?: ') ## input to set Cron interval

cron = crontab.CronTab(user=USER)

job = cron.new(command=DIR_PATH + ' && ' + PY_PATH + ' ' + q + ' ' + t)
job.minute.every(int(t))

cron.write()