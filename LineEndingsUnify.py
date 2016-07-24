import sublime, sublime_plugin
import os
import re

if sublime.version() < '3000':
	from io import open

guessEncodings = ['utf-8','latin1']
handleExtensions = []
lineEndingMode = 0

def convertLineEndings(line, mode):	
	if mode == 0:
		line = line.replace('\r\n', '\n')
		line = line.replace('\r', '\n')
	elif mode == 1:
		line = line.replace('\r\n', '\r')
		line = line.replace('\n', '\r')
	elif mode == 2:
		line = re.sub("\r(?!\n)|(?<!\r)\n", "\r\n", line)
	return line

def scanExtensions(folders):
	global handleExtensions
	for folder in folders:
		for root,dirs,files in os.walk(folder):
			for f in files:
				ext = os.path.splitext(f)[1]
				if ext and ext not in handleExtensions:
					handleExtensions.append(ext)
	handleExtensions = [x[1:] for x in handleExtensions]

def handleFileWithGuessEncoding(file,encodingIndex=0):
	global guessEncodings
	global lineEndingMode
	encoding = guessEncodings[encodingIndex]
	try:
		fd = open(file,'r+',encoding=encoding,newline='')
		lines = fd.readlines()
		lines = [convertLineEndings(line,lineEndingMode) for line in lines]
		fd.seek(0)
		fd.truncate()
		fd.writelines(lines)
		fd.flush()
		fd.close()
	except Exception as e:
		if encodingIndex >= len(guessEncodings) - 1:
			raise
		else:
			return handleFileWithGuessEncoding(file,encodingIndex+1)

def unifyLineEnding(file):
	try:
		global handleExtensions
		ext = os.path.splitext(file)[1]
		if ext not in handleExtensions:
			return
		handleFileWithGuessEncoding(file)
	except Exception as e:
		sublime.error_message('LineEndingsUnify: failed on file ' + file + ' with error: ' + str(e))
		raise

def unifyLineEndingByFolders(folders):
	for folder in folders:
		for root,dirs,files in os.walk(folder):
			for f in files:
				unifyLineEnding(os.path.join(root,f))

def onInputExtensions(text):
	global handleExtensions
	handleExtensions = text.split(',')
	handleExtensions = ['.' + x for x in handleExtensions]
	sublime.active_window().show_input_panel('Input line ending to use',r'\r\n' if os.name == 'nt' else r'\n',onInputLineEnding,None,None)

def onInputLineEnding(text):
	global lineEndingMode
	if text == r'\n':
		lineEndingMode = 0
	elif text == r'\r':
		lineEndingMode = 1
	elif text == r'\r\n':
		lineEndingMode = 2
	else:
		sublime.error_message(r'LineEndingsUnify: please input one of \n,\r,\r\n')
		sublime.active_window().show_input_panel('Input line ending to use',r'\r\n' if os.name == 'nt' else r'\n',onInputLineEnding,None,None)
		return
	unifyLineEndingByFolders(sublime.active_window().folders())
	sublime.message_dialog('LineEndingsUnify Complete')

class LineEndingsUnifyCommand(sublime_plugin.WindowCommand):
	def run(self):
		folders = sublime.active_window().folders()
		if(len(folders) > 0):
			scanExtensions(folders)
			extensions = ','.join(handleExtensions)
			sublime.active_window().show_input_panel('Check File Extensions to process',extensions,onInputExtensions,None,None)
		else:
			sublime.error_message('LineEndingsUnify: drag you folder to sublime\nrun the command again')



