import uuid
import os
import sys
import shutil
import tempfile
try:
	from Scripts import Downloader, Plist, Utils, Run
except:
	import Downloader, Plist, Utils, Run 
###################
# Generate SMBios #
###################

class MacSerial:
	def __init__(self):
		self.d = Downloader.Downloader()
		self.p = Plist.PLIST()
		self.u = Utils.Utils()
		self.r = Run.Run()
		self.Loc = None
		self.SMB = None
		self.MAC = None

	def GetSMBLoc(self):
		self.u.clear()
		self.u.title('Check If Downloaded')
		print(os.listdir(self.Loc))
		print(self.Loc)
		if os.path.exists(f'{self.Loc}/macserial'):
			self.MAC = 'macserial'
		elif os.path.exists(f'{self.Loc}/macserial32.exe'):
			self.MAC = 'macserial32.exe'
		else:
			print('macserial doesn\'t exist')
			self.MAC = None

		return self.MAC

	def getMacSer(self):
		self.u.clear()
		self.u.title('Downloading latest MacSerial')
		url = 'https://api.github.com/repos/acidanthera/MacInfoPkg/releases'
		print('Get latest')
		MacInfo = self.d.OpenAsJSON(url)[0]['assets']
		for k in MacInfo:
			if k['name'].endswith(f"{sys.platform}.zip"):
				self.d.Download(url=k['browser_download_url'], path=self.Loc)

		self.d.unZipper(self.Loc)
		for o in os.listdir(self.Loc):
			if os.path.isdir(self.Loc+"/"+o):
				for s in os.listdir(self.Loc+"/"+o):
					shutil.move(self.Loc+"/"+o+"/"+s, self.Loc+"/")
				break
				

	def getMacSerVersion(self):
		self.u.clear()
		self.u.title('SMBIOS Model')
		ver = self.r.run(f'{self.Loc}/{self.MAC}', '-v')
		for line in ver.stdout: print(line.strip())

	def getSMBios(self):
		ssh = self.r.run(f'{self.Loc}/{self.MAC}', f'-m {self.SMB}')
		for line in ssh.stdout:
			SNBSN = line.strip()
			break

		self.MLB = SNBSN.split(' | ')[1]
		self.SN = SNBSN.split(' | ')[0]
		self.UUID = str(uuid.uuid4()).upper()

	def SMBSelect(self):
		while True:
			self.u.clear()
			self.u.title('SMBIOS Model')
			print('1 - iMac14,2')
			print('2 - iMacPro1,1')
			print('3 - MacPro7,1')
			i = input('what SMBios do you want? ')
			try:
				i = int(i)
				if i > 3: int('a')
				break
			except ValueError:
				print('Please input an integer and between 1 - 3')

		self.SMB = 'iMac14,2' if 1 == i else 'iMacPro1,1' if 2 == i else 'MacPro7,1'

	def main(self):
		with tempfile.TemporaryDirectory() as tmpdirname:
			self.Loc = tmpdirname
			self.getMacSer()
			s = self.GetSMBLoc()
			if not s: return print(f'I could not Locate macserial{"32.exe" if "window" in sys.platform else ""}')

			self.SMBSelect()
			self.getSMBios()

		self.u.clear()
		self.u.title('Mac SMBIOS')
		# print(f'Model: {self.SMB}\nMLB: {self.MLB}\nSerialNumber: {self.SN}\nUUID: {self.UUID}')
		return (self.SMB, self.MLB, self.SN, self.UUID)

# MacSerial().main()
# class Temp:
# 	def __init__(self):
# 		pass