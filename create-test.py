#!/env python3

import os
import datetime
import time
import sys


def usage():
    print('''Usage:
    python3 create-test.py </path/to/dir>
    </path/to/dir> must be exists!
''')


archive_path = ''
if len(sys.argv) > 1:
    archive_path = sys.argv[1];
else:
    usage()

if archive_path and not os.path.isdir(archive_path):
    print('Path for test data doesnt exists!')
    usage()
    exit(1)

file_date = datetime.datetime(2010, 1, 1)

for i in range(1, 1200):
    file_name = 'backup-' + file_date.strftime('%Y%m%d') + '.bak'
    file = open(os.path.join(archive_path, file_name), 'w')
    file.write(file_name)
    file.close()
    #
    os.utime(os.path.join(archive_path, file_name),
             (time.mktime(file_date.timetuple()), time.mktime(file_date.timetuple())))
    #
    file_date = file_date + datetime.timedelta(days=1)
