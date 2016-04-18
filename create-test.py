#!/env python
# -*- coding: utf-8 -*-

import os, stat, datetime, time, shutil, sys
from dateutil import relativedelta as rd

if len(sys.argv) > 1:
	archive_path = sys.argv[1];

if not os.path.exists(archive_path):
	exit(1)

file_date = datetime.datetime(2010, 1, 1)

for i in range(1,1200):
    file_name = 'backup-' + file_date.strftime('%Y%m%d') + '.bak'
    file = open(os.path.join(archive_path, file_name), 'w')
    file.write(file_name)
    file.close()
    #
    os.utime(os.path.join(archive_path, file_name), (time.mktime(file_date.timetuple()), time.mktime(file_date.timetuple())))
    #
    file_date = file_date + datetime.timedelta(days=1)
