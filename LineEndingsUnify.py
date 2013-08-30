import sublime, sublime_plugin
import os, glob

handleExtensions = []

def walkdirs(path,callback):
	for currentFile in glob.glob( os.path.join(path, '*') ):
		if os.path.isdir(currentFile):
			walkdirs(currentFile,callback)
		else:
			callback(currentFile)
def unifyLineEnding(file):
	ext = os.path.splitext(file)[1]
	if not (ext in handleExtensions):
		return
	fd = open(file,'rU+')
	lines = fd.readlines()
	fd.seek(0)
	fd.truncate()
	fd.writelines(lines)
	fd.flush()
	fd.close()

def onInputExtensions(text):
	global handleExtensions
	handleExtensions = text.split(',')
	handleExtensions = ['.' + x for x in handleExtensions]
	folders = sublime.active_window().folders()
	for folder in folders:
		walkdirs(folder,unifyLineEnding)
class LineEndingsUnifyCommand(sublime_plugin.WindowCommand):
	def run(self):
		folders = sublime.active_window().folders()
		if(len(folders) > 0):
			sublime.active_window().show_input_panel('handle File Extensions','txt,c,cpp,js,css,html,php,java,rb,lua',onInputExtensions,None,None)
		else:
			sublime.error_message('LineEndingsUnify: drag you folder to sublime\nrun the command again')
		
		

