#!/env python
# -*- coding: utf-8 -*-

import os, stat, datetime, time, shutil
from dateutil import relativedelta as rd

archive_path = 'd:\\tmp\\backup\\dayly'

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