#!/usr/bin/python3

from os import system

import sys
from PySide6 import QtWidgets, QtCore, QtGui

from PySide6.QtCore    import Slot, Qt
from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton
from PySide6.QtGui     import QFont, QKeyEvent





# functions
def open_url(url):
	system('firefox \'' + url + '\' &>/dev/null &')
	return

def open_nemo(url):
	system('nemo \'' + url + '\' &>/dev/null &')





# objects
commands = {
	'21'       : lambda args='': open_url('https://profile.intra.42.fr/'),
	'ifconfig' : lambda args='': open_url('https://ifconfig.me/'),

	'слово'   : lambda args='': open_url(
		'https://ru.wiktionary.org/wiki/%s' % args
		if len(args) != 0 else
		'https://ru.wiktionary.org'
	),
	'word'    : None,

	'вк'      : lambda args='': open_url(
		'https://vk.com/%s' % args
		if len(args) != 0 else
		'https://vk.com/im'
	),
	'vk'      : None,

	'киви'    : lambda args='': open_url('https://qiwi.com/main'),
	'qiwi'    : None,

	'ютуб'    : lambda args='': open_url(
		'https://www.youtube.com/results?search_query=%s' % args
		if len(args) != 0 else
		'https://www.youtube.com'
	),
	'см'      : None,
	'you'     : None,
	'youtube' : None,


	'яндекс'  : lambda args='': open_url(
		'https://yandex.ru/search/?text=%s&lr=10731' % args
		if len(args) != 0 else
		'https://yandex.ru'
	),
	'я'       : None,
	'ya'      : None,
	'yandex'  : None,

	'гугл'    : lambda args='': open_url(
		'https://www.google.com/search?q=%s' % args
		if len(args) != 0 else
		'https://www.google.com/'
	),
	'г'       : None,
	'google'  : None,
	'g'       : None,


	'перевод' : lambda args='': open_url(
		'https://translate.yandex.ru/?lang=ru-en&text=%s' % args
		if len(args) != 0 else
		'https://translate.yandex.ru/?lang=ru-en'
	),
	'tr'      : lambda args='': open_url(
		'https://translate.yandex.ru/?lang=en-ru&text=%s' % args
		if len(args) != 0 else
		'https://translate.yandex.ru/?lang=en-ru'
	),


	'аниме'   : lambda args='': open_url(
		'https://smotret-anime.online/catalog/search?q=%s' % args
		if len(args) != 0 else
		'https://smotret-anime.online'
	),
	'anime'   : None,


	'варт'    : lambda args='': open_url(
		'http://www.world-art.ru/search.php?public_search=%s&global_sector=all' % args
		if len(args) != 0 else
		'http://www.world-art.ru'
	),
	'wart'    : None,


	'озон'    : lambda args='': open_url(
		'https://www.ozon.ru/search/?from_global=true&text=%s' % args
		if len(args) != 0 else
		'https://www.ozon.ru'
	),
	'ozon'    : None,


	'плюсы'   : lambda args='': open_url(
		'http://www.cplusplus.com/search.do?q=%s' % args
		if len(args) != 0 else
		'http://www.cplusplus.com'
	),
	'++'      : None,
	'c++'     : None,
	'с++'     : None,


	'кт'      : lambda args='': open_url(
		'https://doc.qt.io/qt-5.15/search-results.html?q=%s' % args
		if len(args) != 0 else
		'https://doc.qt.io/qt-5.15'
	),
	'qt'      : None,



	'почта'   : lambda args='': open_url('https://mail.yandex.ru/lite/'),
	'post'    : None,

	'диск'    : lambda args='': open_url('https://disk.yandex.ru/client/disk?source=domik-main'),
	'disk'    : None,
	'гдиск'   : lambda args='': open_url('https://drive.google.com/drive/my-drive'),
	'gdisk'   : None,

	'трел'    : lambda args='': open_url('https://trello.com/b/0JUDvgmK/учеба'),
	'трело'   : None,
	'трелло'  : None,
	'trel'    : None,
	'trello'  : None,

	'дис'     : lambda args='': open_url('https://discord.com/channels/748577967449309236/748577967449309239'),
	'dis'     : None,

	'автор'   : lambda args='': open_url('https://author.today/'),
	'author'  : None,

	'гитхаб'  : lambda args='': open_url(
		'https://github.com/nvxden?tab=repositories'
		if len(args) == 0 else
		'https://github.com/nvxden/%s' % args
	),
	'гит'     : None,
	'github'  : None,
	'git'     : None,

	'хабр'    : lambda args='': open_url('https://habr.com/ru/top/'),
	'habr'    : None,

	'степик'  : lambda args='': open_url(
		'https://stepik.org/users/18395707/courses'
		if len(args) == 0 else
		{
			'тв'      : 'https://stepik.org/course/3089/syllabus',
			'теорвер' : 'https://stepik.org/course/3089/syllabus',
			'dl'      : 'https://stepik.org/course/91157/syllabus',
			'го'      : 'https://stepik.org/course/91157/syllabus',
		}[args]
	),
	'stepik'  : None,

	'мега'    : lambda args='': open_url('https://mega.nz/fm/account'),

	'кдбэк'   : lambda args='': open_url('https://backoffice.kodland.org/ru/courses/'),
	'кдпитон' : lambda args='': open_url('https://backoffice.kodland.org/ru/courses_67/'),
	'кдгр'    : lambda args='': open_url('https://backoffice.kodland.org/ru/groups/'),
	'кдчек'   : lambda args='': open_url('https://docs.google.com/forms/d/e/1FAIpQLSfuAE8lQ0qo_yNNN7Y4JpnuBNjvyJAMhi1L8zDAGMngnRVPdg/viewform'),
	'кдплат'  : lambda args='': open_url('https://platform.kodland.org/ru/courses/'),
	'кдотчёт' : lambda args='': open_url('https://forms.gle/4Hhe1FRYiVBVjYoz8'),
	'кдбаза'  : lambda args='': open_url('https://www.notion.so/b5adc3748449494784b5999f7815864b'),
	'вебка'   : lambda args='': open_url('https://ru.webcamtests.com/'),

	'мосру'   : lambda args='': open_url('https://my.mos.ru/my'),
	'mosru'   : None,

	'расп'    : lambda args='': open_url('https://e.mospolytech.ru/?p=rasp'),
	'сдо'     : lambda args='': open_url(
		'https://online.mospolytech.ru/'
		if len(args) == 0 else
		{
			'англ'    : 'https://online.mospolytech.ru/course/view.php?id=7964',
			'матан'   : 'https://online.mospolytech.ru/course/view.php?id=313',
			'диффуры' : 'https://online.mospolytech.ru/course/view.php?id=3362',
			'диф'     : 'https://online.mospolytech.ru/course/view.php?id=3362',
			'матстат' : 'https://online.mospolytech.ru/course/view.php?id=720',
			'мс'      : 'https://online.mospolytech.ru/course/view.php?id=720',
			'теорвер' : 'https://online.mospolytech.ru/course/view.php?id=573',
			'тв'      : 'https://online.mospolytech.ru/course/view.php?id=573',
			'физра'   : 'https://online.mospolytech.ru/course/view.php?id=4436',
			'бд'      : 'https://online.mospolytech.ru/course/view.php?id=1563',
		}
		[args]
	),
	'сессия'  : lambda args='': open_url('https://rasp.dmami.ru/session'),

	'тимс'    : lambda args='': open_url(
		'https://teams.microsoft.com/_#/school//?ctx=teamsGrid'
		if len(args) == 0 else
		{
			'гр'  : 'https://teams.microsoft.com/_#/school/conversations/%D0%9E%D0%B1%D1%89%D0%B8%D0%B9?threadId=19:73a13a965d894b48b227faef1cb113b1@thread.tacv2&ctx=channel',
			'рвп' : 'https://teams.microsoft.com/_#/school/conversations/%D0%9E%D0%B1%D1%89%D0%B8%D0%B9?threadId=19:01ba1f56023e43ea91b28c79cbf23ae7@thread.tacv2&ctx=channel',
			'вт'  : 'https://teams.microsoft.com/_#/school/conversations/%D0%9E%D0%B1%D1%89%D0%B8%D0%B9?threadId=19:3c2a8a5cc8344214ba01564ce23dbf4d@thread.tacv2&ctx=channel'
		}[args]
	),
	'teams'   : None,

	'немо'    : lambda args='': open_nemo( {
		''         : '',
		'заг'      : '/home/lis/dow',
		'dow'      : '/home/lis/dow',
		'док'      : '/home/lis/doc',
		'doc'      : '/home/lis/doc',
		'из'       : '/home/lis/pictures',
		'pic'      : '/home/lis/pictures',
		'pictures' : '/home/lis/pictures',
		'муз'      : '/home/lis/music',
		'музыка'   : '/home/lis/music',
		'mus'      : '/home/lis/music',
		'music'    : '/home/lis/music',
		'вид'      : '/home/lis/movies',
		'видео'    : '/home/lis/movies',
		'mov'      : '/home/lis/movies',
		'movie'    : '/home/lis/movies',

		'раб'      : '/home/lis/work',
		'рабочая'  : '/home/lis/work',
		'work'     : '/home/lis/work',
		'уч'       : '/home/lis/doc/Книги/Учебники',
		'учебники' : '/home/lis/doc/Книги/Учебники',
		'bk'       : '/home/lis/doc/Книги/Учебники',
		'универ'   : '/home/lis/doc/Университет',
		'uni'      : '/home/lis/doc/Университет',
		'univer'   : '/home/lis/doc/Университет',
		'кодленд'  : '/home/lis/doc/Kodland',
		'кд'       : '/home/lis/doc/Kodland',
		'kd'       : '/home/lis/doc/Kodland',
		'kodland'  : '/home/lis/doc/Kodland',
		'рассказ'  : '/home/lis/doc/Записи/Художественное/Рассказы/03. Юные Авантюристы',
		'story'    : '/home/lis/doc/Записи/Художественное/Рассказы/03. Юные Авантюристы',

		'англ'     : '/home/lis/doc/Университет/Английский',
		'дискра'   : '/home/lis/doc/Университет/Дискра',
		'матан'    : '/home/lis/doc/Университет/Матан',
		'инфа'     : '/home/lis/doc/Университет/Информатика',
		'уп'       : '/home/lis/doc/Университет/Управление персоналом',
		'книги'    : '/home/lis/doc/Книги'
	}[args] ),

	'англ' : lambda args='': open_url(
		'https://myefe.ru/pd'
		if len(args) == 0 else
		{
			'словари' : 'https://myefe.ru/pd',
			'dict'    : 'https://myefe.ru/pd',
			'тр'      : 'https://myefe.ru/anglijskaya-transkriptsiya.html',
			'tr'      : 'https://myefe.ru/anglijskaya-transkriptsiya.html',
		}
		[args]
	),

	'туду'    : lambda args='': open_url('https://todoist.com/app/today#'),
	'todo'    : None,
	'todoist' : None,
}

commands['word']    = commands['слово']
commands['vk']      = commands['вк']
commands['qiwi']    = commands['киви']
commands['см']      = commands['ютуб']
commands['you']     = commands['ютуб']
commands['youtube'] = commands['ютуб']
commands['я']       = commands['яндекс']
commands['ya']      = commands['яндекс']
commands['yandex']  = commands['яндекс']
commands['г']       = commands['гугл']
commands['google']  = commands['гугл']
commands['g']       = commands['гугл']
commands['пер']     = commands['перевод']
commands['anime']   = commands['аниме']
commands['wart']    = commands['варт']
commands['ozon']    = commands['озон']
commands['++']      = commands['плюсы']
commands['c++']     = commands['плюсы']
commands['с++']     = commands['плюсы']
commands['qt']      = commands['кт']

commands['post']    = commands['почта']
commands['disk']    = commands['диск']
commands['gdisk']   = commands['гдиск']
commands['трело']   = commands['трел']
commands['трелло']  = commands['трел']
commands['trel']    = commands['трел']
commands['trello']  = commands['трел']
commands['dis']     = commands['дис']
commands['author']  = commands['автор']
commands['гит']     = commands['гитхаб']
commands['github']  = commands['гитхаб']
commands['git']     = commands['гитхаб']
commands['habr']    = commands['хабр']
commands['stepik']  = commands['степик']
commands['mega']    = commands['мега']
commands['teams']   = commands['тимс']
commands['nemo']    = commands['немо']
commands['myefe']   = commands['англ']
commands['mosru']   = commands['мосру']

commands['todo'] = commands['туду']
commands['todoist'] = commands['туду']





# main
app = QApplication(sys.argv)

class Line(QLineEdit):
	def __init__(self, parent=None):
		super(Line, self).__init__(parent)
		self.setWindowFlags( Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
		self.resize(200, 60)
		self.setStyleSheet(
			'background: #2E2E2E;\n' +
			'color: #EDEDED;\n' +
			'border: 15px solid #404040;\n' +
			'padding: 5px;'
		)


	def keyPressEvent(self, event):
		super(Line, self).keyPressEvent(event)
		if event.key() == Qt.Key_Enter:
			text = self.text().strip().split(' ')
			if len(text) == 0:
				return
			try:
				com = commands[text[0]];
				com(' '.join(text[1:]))
				exit(0)

				if len(text) == 1:
					value = references[text[0]]
					system('firefox ' + value + ' &')
				else:
					value = references_with_search[text[0]]
					system( 'firefox ' + (value % '+'.join(text[1:])) )
					print( 'firefox ' + (value % '+'.join(text[1:])) )
			except Exception:
				self.setText('')
				return

		elif event.key() == Qt.Key_Escape:
			exit(0)



w = Line()
w.show()

sys.exit(app.exec_())





# END
