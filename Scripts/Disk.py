import sys, os
import time
from subprocess import Popen, PIPE

class Disk:
	def __init__(self):
		pass

	def windowsDiskFormat(self):
		p = Popen(["diskpart"], stdin=PIPE)
		print("sending data to STDIN")
		res1 = p.stdin.write(bytes("select disk 2\n", 'utf-8'))
		time.sleep(.5)
		res2 = p.stdin.write(bytes("ATTRIBUTES DISK CLEAR READONLY\n", 'utf-8'))
		time.sleep(.5)
		res3 = p.stdin.write(bytes("online disk noerr\n", 'utf-8'))
		time.sleep(.5)
		res4 = p.stdin.write(bytes("clean\n", 'utf-8'))
		time.sleep(.5)
		res5 = p.stdin.write(bytes("create part pri\n", 'utf-8'))
		time.sleep(.5)
		res6 = p.stdin.write(bytes("select part 1\n", 'utf-8'))
		time.sleep(.5)
		res7 = p.stdin.write(bytes("assign\n", 'utf-8'))
		time.sleep(.5)
		res8 = p.stdin.write(bytes("FORMAT FS=NTFS QUICK \n", 'utf-8'))
		time.sleep(.5)

	def linuxNmacOsDiskFormat(self):
		pass

	def listDisk(self):
		if sys.platform == 'linux':
			os.system('lsblk | grep disk')
		# elif sys.platform == 'windows':
		# 	pass
		# else:
		# 	pass

Disk().listDisk()