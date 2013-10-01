'''
Prints a report to the log pane about tasks that are past due and not marked as 'done'

Useful as an @button node

Jake Peck 20131001
'''

import datetime

today = datetime.date.today()
n = []
for p in c.all_positions():
  duedate = c.cleo.getat(p.v, 'duedate')
  priority = c.cleo.getat(p.v, 'priority')
  if priority: priority = int(priority) # 100 = 'done', per todo.py
  if (duedate and duedate < today 
      and priority != 100 and p.v not in n):
    n.append(p.v)

if len(n) == 0:
  g.es('No tasks past due.',color='blue')
else:
  g.es('The following tasks are past due:',color='red')
  for v in n:
    g.es(v.h,color='red')
