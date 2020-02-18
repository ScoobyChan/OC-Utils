import subprocess
import shlex
class Run:
	def __init__(self):
		pass

	def run(self, file=None, args=None):
		if args:
			args = shlex.split(args)
			args.insert(0, file)
			process = subprocess.Popen(args, stdout=subprocess.PIPE, universal_newlines=True)
		else:
			process = subprocess.Popen([file], stdout=subprocess.PIPE, universal_newlines=True)
					
		return process