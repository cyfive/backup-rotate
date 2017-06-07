# backup-rotate

Скрипт ротации архивов резервных копий. Написан на Python 2.7.

## Использование

Для работы скрипта требуется [Python 2.7](http://python.org), [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

Если вы хотите создать выполняемый файл для Windows вам потребуется установиить python-dateutil командой:

```
easy_install --always-unzip python-dateutil
```

Для создания выполняемого файла вам потребуется установить [py2exe](http://www.py2exe.org/) и выполнить:

```
python setup.py py2exe
```
в папке *dist* будут сгенерированы файлы, которые можно использовать без установки python

## Поддерживаемые платформы
Скрипт протестирован:

Windows 7 sp1

Windows 2008 server

Fedora 23
