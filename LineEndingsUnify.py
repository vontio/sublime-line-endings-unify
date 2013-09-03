import sublime, sublime_plugin
import os

handleExtensions = []

def scanExtensions(folders):
	global handleExtensions
	for folder in folders:
		for root,dirs,files in os.walk(folder):
			for f in files:
				ext = os.path.splitext(f)[1]
				if ext and ext not in handleExtensions:
					handleExtensions.append(ext)
	handleExtensions = [x[1:] for x in handleExtensions]

def unifyLineEnding(file):
	global handleExtensions
	ext = os.path.splitext(file)[1]
	if ext not in handleExtensions:
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
		for root,dirs,files in os.walk(folder):
			for f in files:
				unifyLineEnding(os.path.join(root,f))
class LineEndingsUnifyCommand(sublime_plugin.WindowCommand):
	def run(self):
		folders = sublime.active_window().folders()
		if(len(folders) > 0):
			scanExtensions(folders)
			extensions = ','.join(handleExtensions)
			sublime.active_window().show_input_panel('Check File Extensions to process',extensions,onInputExtensions,None,None)
		else:
			sublime.error_message('LineEndingsUnify: drag you folder to sublime\nrun the command again')
		
		

