from time import strftime

def DebugLog(message):
	time = str(strftime('%H:%M:%S'))
	print('[' + time + '] ' + message)
	logFile = open('log', 'a')
	logFile.write('[' + time + '] ' + message + '\n')
	logFile.close()