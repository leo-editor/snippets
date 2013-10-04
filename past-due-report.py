@language python

'''
prints a report to the log pane about tasks that are past due and not marked as 'done'
'''

import datetime

today = datetime.date.today()
n = []
for p in c.all_positions():
  duedate = c.cleo.getat(p.v, 'duedate')
  priority = c.cleo.getat(p.v, 'priority')
  if priority: priority = int(priority)
  if (duedate and duedate < today 
      and priority != 100 and p.v not in n):
    n.append(p.v)

if len(n) == 0:
  g.es('No tasks past due.',color='blue')
else:
  g.es('The following tasks are past due:',color='red')
  for v in n:
    g.es(c.vnode2position(v).get_UNL(with_file=False, with_proto=False),color='red')
