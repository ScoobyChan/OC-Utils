import plistlib
import os
import sys
import time

class PLIST:
	def __init__(self):
		pass

	def clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')

	def openFile(self, FILE=None):
		if not FILE:
			return print('No File Given')
		file, ext = os.path.splitext(FILE)
		if ext == '.plist' or ext == '.xml':
			try:	
				c = open(file+ext, 'rb')
				self.config = plistlib.load(c)
				return self.config
			except FileNotFoundError:
				return print('File Can not be found')
		else:
			return print('Invalid Extension')

	def listContents(self):
		try:
			for c in self.config:
				print(c)
				try:	
					for d in self.config[c]:
						print(f'{c} -> {d}')
						try:
							for e in self.config[c][d]:
								print(f'{c} -> {d} -> {e}')
						except Exception as e:
							pass
				except Exception as e:
					pass
		except Exception as e:
			pass

