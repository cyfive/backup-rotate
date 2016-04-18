#!/env python
# -*- coding: utf-8 -*-

import os, stat, datetime, shutil, getopt, sys
from dateutil import relativedelta as rd

#default configuration
dayly_params = {'type' : 'dayly', 'cnt' : 7, 'arch_dir': 'dayly'}
weekly_params = {'type' : 'weekly', 'cnt' : 4, 'arch_dir': 'weekly'}
monthly_params = {'type' : 'monthly', 'cnt' : 12, 'arch_dir': 'monthly'}
yearly_params = {'type' : 'yearly', 'cnt' : 5, 'arch_dir': 'yearly'}
#
archive_path = os.getcwd()
log_path = os.getcwd()
#
rotate_steps = []
#
def print_help() :
	print ''
	print 'backup-rotate (c) 2015, Stanislav V. Emets'
	print 'Usage:'
	print '	backup-rotate [-a <path>| --archive=<path>]'
	print ''
	print '		-h | --help - print this help'
	print '		-l <path> | --log=<path> - path to log file, default value: current directory'
	print '		-a <path> | --archive=<path> - path to archive directory,  default value: current directory'
	print '		-d <number> | --dayly=<number> - how many keep dayly copies, default value 7'
	print '		-w <number> | --weekly - how many keep weekly copies, default value 4'
	print '		-m <number> | --montly=<number> - how many keep monthly copies, default value 12'
	print '		-y <number> | --yearly=<number> - how many keep yearly copies, default value 5'

def parse_args():
	global dayly_params, weekly_params, monthly_params, yearly_params, archive_path, log_path
	 
	status = True
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hl:a:d:w:m:y:", ["help", "log=", "archive=", "dayly=", "weekly=", "monthly=", "yearly=", ])
	except getopt.GetoptError as err:
		status = False
		
	for opt, arg in opts :
		if opt in ('-h', '--help'):
			print_help()
			status = False
		elif opt in ('-l', '--log'):
			log_path = arg
		elif opt in ('-a', '--archive'):
			archive_path = arg
		elif opt in ('-d', '--dayly'):
			dayly_params['cnt'] = int(arg)
		elif opt in ('-w', '--weekly'):
			weekly_params['cnt'] = int(arg)
		elif opt in ('-m', '--monthly'):
			monthly_params['cnt'] = int(arg)
		elif opt in ('-y', '--yearly'):
			yearly_params['cnt'] = int(arg)
			
	return status
	
def get_file_list(step, dir_path):
	archive_file_list = {}
	cur_dir = os.path.join(dir_path, step['arch_dir'])
	file_list = os.listdir(cur_dir)
	for file_name in file_list:
		cur_file = os.path.join(cur_dir, file_name)
		file_attrib = os.stat(cur_file)
		if stat.S_ISREG(file_attrib.st_mode) :
			archive_file_list[file_attrib.st_mtime] = cur_file
	return archive_file_list

def rotate_dir(step, next_step, dates, files):
	if len(next_step) > 0:
		for file_date in dates:
			#находим самый свежий файл в next_step
			next_step_files = get_file_list(next_step, archive_path)
			if len(next_step_files) > 0 :
				next_step_dates = sorted(next_step_files)
				next_step_last_date = datetime.datetime.fromtimestamp(next_step_dates[len(next_step_dates)-1])
				step_file_date = datetime.datetime.fromtimestamp(file_date)
				
				#к дате добавляем интервал в зависимости от типа следующего шага
				if next_step['type'] == 'weekly':
					next_file_date = next_step_last_date + rd.relativedelta(weeks = +1)
				elif next_step['type'] == 'monthly':
					next_file_date = next_step_last_date + rd.relativedelta(months = +1)
				elif next_step['type'] == 'yearly':
					next_file_date = next_step_last_date + rd.relativedelta(years = +1)
				
				#если дата текущего файла больше или равна получившейся, то файл перемещаем в next_step, иначе удаляем
				if step_file_date >= next_file_date:
					#переносим в следующий шаг
					new_file_name = os.path.split(files[file_date])
					new_file_name = os.path.join(archive_path, next_step['arch_dir'], new_file_name[1])
					shutil.move(files[file_date], new_file_name)
				else:
					#удаляем
					os.remove(os.path.join(archive_path, step['arch_dir'], files[file_date]))
	
			else: #ничего нет пока в следующем шаге, просто перемещаем
				new_file_name = os.path.split(files[file_date])
				new_file_name = os.path.join(archive_path, next_step['arch_dir'], new_file_name[1])
				shutil.move(files[file_date], new_file_name)

	else: #следующего шага нет, просто удаляем лишние файлы
		for file_date in dates:
				new_file_name = os.path.split(files[file_date])
				new_file_name = os.path.join(archive_path, next_step['arch_dir'], new_file_name[1])
				shutil.move(files[file_date], new_file_name)

	
def main():
	global rotate_steps
	
	has_errors = False
	
	if not parse_args():
		print_help()
		sys.exit()

	if dayly_params['cnt'] > 0:
		rotate_steps.append(dayly_params)
		
	if weekly_params['cnt'] > 0:
		rotate_steps.append(weekly_params)
		
	if monthly_params['cnt'] > 0:
		rotate_steps.append(monthly_params)
		
	if yearly_params['cnt'] > 0:
		rotate_steps.append(yearly_params)
	
	#проверим соответствие заданного каталога требуемой структуре
	dir_list = os.listdir(archive_path)
	if len(dir_list) == 0 :
		print_help()
		sys.exit()
	else :
		for cur_step in rotate_steps :
			try :
				dir_list.index(cur_step['arch_dir'])
			except ValueError:
				has_errors = True
					
	if has_errors :
		print_help()
		sys.exit()
		
	#начинаем ротацию архива
	next_step_index = 1
	for cur_step in rotate_steps:
		archive_files = get_file_list(cur_step, archive_path)
		archive_dates = sorted(archive_files)
		
		rotate_dates = []
		if len(archive_dates) > cur_step['cnt']:
			rotate_dates = archive_dates[0:len(archive_dates) - cur_step['cnt']]
			if next_step_index > 0:
				next_step = rotate_steps[next_step_index]
			else:
				next_step = {}
	
			rotate_dir(cur_step, next_step, rotate_dates, archive_files)

		next_step_index += 1
		if next_step_index > (len(rotate_steps) - 1):
			next_step_index = 0

if __name__ == '__main__':
	main()
