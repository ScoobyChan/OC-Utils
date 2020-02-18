from Scripts import Downloader, Plist, Plistread, CheckerOC, Utils, MC
import os, sys, time, shutil

# Download AppleMCE
# link to SSDTTime for pro models

class EFIMaker:
	def __init__(self):
		self.d = Downloader.Downloader()
		self.p = Plist.PLIST()
		self.CheckerOC = CheckerOC.CheckerOC()
		self.u = Utils.Utils()
		self.macser = MC.MacSerial()
		self.oc_url = "https://api.github.com/repos/Acidanthera/OpenCorePkg/releases"
		self.null = 'https://cdn.discordapp.com/attachments/263757191608139779/643751774666358794/NullCPUPowerManagement.kext.zip'
		self.ALC = 'https://api.github.com/repos/Acidanthera/AppleALC/releases'
		self.Lilu = 'https://api.github.com/repos/Acidanthera/Lilu/releases'
		self.WEG = 'https://api.github.com/repos/Acidanthera/WhateverGreen/releases'
		self.virtual = 'https://api.github.com/repos/Acidanthera/VirtualSMC/releases'
		self.Atheros = 'https://api.github.com/repos/Mieze/AtherosE2200Ethernet/releases'
		self.Intel = 'https://cdn.discordapp.com/attachments/613613525897576487/669425469619437568/SmallTreeIntel82576.zip'
		self.Realtek = 'https://api.github.com/repos/Mieze/RTL8111_driver_for_OS_X/releases'
		self.AppleSupportPkg = 'https://api.github.com/repos/Acidanthera/AppleSupportPkg/releases' # APFS
		self.HFPlus = 'https://cdn.discordapp.com/attachments/606452360495104000/633621011887292416/HFSPlus.efi'
		self.Null = False
		self.EFI = None
		self.status = ''
		self.patConf = ''
		self.defaultLocat = os.path.dirname(os.path.abspath(__file__))
		self.AppleMCEURL = 'https://github.com/AMD-OSX/AMD_Vanilla/raw/master/Extra/AppleMCEReporterDisabler.kext.zip'


	def cleanUp(self, Res=False):
		print("Cleaning up Folders")
		if os.path.exists('Drivers'):
			shutil.rmtree('Drivers/')
		if os.path.exists('Kexts/'):
			shutil.rmtree('Kexts/')
		if os.path.exists('Opencore/'):
			shutil.rmtree('Opencore/')
		if os.path.exists('Patches/'):
			shutil.rmtree('Patches/')
		if os.path.exists('PlistMerge/'):
			shutil.rmtree('PlistMerge/')
		if os.path.exists('AppleMCE/'):
			shutil.rmtree('AppleMCE/')
		if Res == True:
			if os.path.exists('Results/'):
				shutil.rmtree('Results/')

	def main(self):
		while True:
			try:
				self.u.clear()
				self.u.title('OpenCore Utilities')
				print(self.status)
				print("Do you want to:")
				print("1 - Check EFI") # Add
				print("2 - Make EFI") # Done
				print("3 - Make USB")
				print("4 - Update OpenCore AMD Patches")
				print("5 - Update OpenCore Version")
				print("6 - Clean Up Folders")
				print("7 - Check Config")
				print("8 - Generate Recommended SMBios\n")
				print("q - Quit\n")
				i = input("User Choice: ")
				try:
					i = int(i)
					if i == 1:
						print('Checking EFI')
						self.CheckEFI()
					elif i == 2:
						print('Making OC EFI')
						self.buildOC()
					elif i == 3:
						print('Making USB')
						print('== Work in progress')
						time.sleep(2)
						# Download OS Make Partitions...
					elif i == 4:
						print('Updating Patches')
						self.mergePatches()
					elif i == 5:
						print('Updating OpenCore')
						self.UpdateOpenCore()
					elif i == 6:
						self.cleanUp(Res=True)
						time.sleep(1)
					elif i == 7:
						pass
						time.sleep(1)
					elif i == 8:
						self.SMBIOSGen()
						time.sleep(1)
					else:
						print('Invalid Number')
					time.sleep(1)
					self.status = ''
				except ValueError as e:
					break
			except KeyboardInterrupt:
				print('\nQuit Program')
				break

	def CheckEFI(self):
		self.u.clear()
		self.u.title('OpenCore EFI Checker')
		print('\nOpencore EFI Checker')
		while True:
			if not os.path.exists('config.plist'):
				locat = input('Please give location to config.plist or Place me in folder of config.plist: ')
				if not locat: return

			if not os.path.exists(locat+'config.plist'):
				print('Still Cannot find Config please try again')

			break

		stat = self.CheckerOC.main(locat, self.defaultLocat)
		self.status = stat

	def UpdateOpenCore(self):
		self.u.clear()
		self.u.title('OpenCore Updater')
		self.cleanUp()
		print('\nOpencore EFI Checker')
		while True:
			if not os.path.exists('config.plist'):
				locat = input('Please give location to config.plist: ')
				if not locat: return

			if not os.path.exists(locat+'config.plist'):
				print('Still Cannot find Config please try again')

			break

		self.d.unZipper('Opencore/')
		folder = os.listdir('Opencore')[0]
		locEFI = f"Opencore/{folder}/EFI"
		Boot = os.listdir(f'{locEFI}/BOOT')[0]
		for o in os.listdir(f'{locEFI}/OC'):
			if o.endswith('.efi'):
				OCEFI = o

		locOC = f"{locEFI}/OC/{OCEFI}"


		if os.path.exists(f'{locat}/{OCEFI}'): 
			os.remove(f'{locat}/{OCEFI}')

		shutil.move(locOC, locat)
		shutil.move(f'{locEFI}/BOOT/{Boot}', locat)

		os.chdir(locat)
		
		if os.path.exists(f'../BOOT/{Boot}'): os.remove(f'../BOOT/{Boot}')			
		shutil.move(f'{Boot}',f'../BOOT/{Boot}')

		os.chdir(self.defaultLocat)
		time.sleep(0.05)
		self.status = 'OpenCore has been Updated'
		self.OCSelector()

	def buildOC(self):
		self.cleanUp()
		self.Name = input('User Name: ')
		self.CPUSelect()
		self.OCSelector()
		self.NullCPU()
		self.MainKext()
		self.Audiokext() 
		self.AppleSupport()
		self.NetworkKext()
		self.Drivers()
		self.Unzip()
		self.AppleMCED()
		self.createStructure()

	def AppleMCED(self):
		self.u.clear()
		self.u.title('Downloading AppleMCEReporterDisabler')
		self.d.Download(url=self.AppleMCEURL, path='AppleMCE', output='AppleMCE.zip')
		self.d.unZipper(path='AppleMCE')
		if os.path.exists(f'AppleMCE/-AppleMCE.zip/AppleMCEReporterDisabler.kext') and os.path.exists(f'{self.EFI}/EFI/OC/Kexts/'):
			print('Moving AppleMCEReporterDisabler')
			shutil.move(f'AppleMCE/-AppleMCE.zip/AppleMCEReporterDisabler.kext', f'{self.EFI}/EFI/OC/Kexts/')
		

	def NullCPU(self):
		self.u.clear()
		self.u.title('OpenCore NullCPUPowerManagement Kext or Quirk')
		while True:
			i = input('Kext or Quirk? k/q:\n')
			i = i.lower()
			if i == 'k':
				self.Null = False
				break
			elif i == 'q':
				self.Null = True
				break
			else:
				print('Invalid Answer')

	def CPUSelect(self):
		valid = ['17h','16h','15h']
		while True:	
			self.u.clear()
			self.u.title('CPU Selector')
			print('What CPU Type are you using')
			print(' - 17h')
			print(' - 16h')
			print(' - 15h')
			print('')
			self.i = input('CPU Type: ')
			if self.i in valid:
				break

		if self.i == '17h':
			print('Ryzen')
			dLink = 'https://files.amd-osx.com/patches/OC-patches-17h.plist.zip'
		else:
			print('FX/APU')
			dLink = 'https://files.amd-osx.com/patches/OC-patches-15_16h.plist.zip'
		self.u.clear()
		self.u.title('OpenCore Patches')
		print(f"downloading {self.i} Patches")
		self.d.Download(url=dLink, path='Patches', output='patch.zip')
		self.d.unZipper(path='Patches')
		for f in os.listdir('Patches'):
			try:
				for P in os.listdir(f'Patches/{f}'):
					if P.endswith('.plist'):
						shutil.move(f'Patches/{f}/{P}', f'Patches/')
			except NotADirectoryError:
				pass

	def OCSelector(self):
		while True:
			self.u.clear()
			self.u.title('OpenCore Version Selector')
			ocu = self.d.OpenAsJSON(self.oc_url)
			num = 1
			for c in ocu:
				print(f'{num} - Opencore Version:', c['name'])
				num += 1

			i = input("list input: ")
			try:
				i = int(i)
				self.u.clear()
				self.u.title(f'Downloading {ocu[i-1]["name"]}')
				for k in ocu[i-1]['assets']:
					if "RELEASE" in k['browser_download_url']:
						self.d.Download(url=k['browser_download_url'], path='Opencore')
				break
			except ValueError:
				print('Needs to be a number not letter')

	def MainKext(self):
		self.u.clear()
		self.u.title('Downloading main Kexts')
		print(f'Downloading VirtualSMC')
		self.d.GitDL(self.virtual, 'Kexts')
		
		print(f'Downloading Lilu')
		self.d.GitDL(self.Lilu, 'Kexts')
		
		print(f'Downloading WhateverGreen')
		self.d.GitDL(self.WEG, 'Kexts')

		if self.Null == False:
			print(f'Downloading NullCPUPowerManagement')
			self.d.Download(url=self.null, path='Kexts')

	def AppleSupport(self):
		self.u.clear()
		self.u.title('AppleSupportPkg Download')
		print(f'Downloading AppleSupportPkg')
		self.d.GitDL(self.AppleSupportPkg, 'Drivers')

	def Audiokext(self):
		self.u.clear()
		self.u.title('OpenCore Audio kexts')
		if self.i == '17h':
			self.d.GitDL(self.ALC, 'Kexts')
			print(f'Downloading AppleALC')
		else:
			self.d.GitDL(self.VoodooHDA, 'Kexts')
			print(f'Downloading VoodooHDA')
		
	def NetworkKext(self):
		while True:	
			self.u.clear()
			self.u.title('Network Kext Selector')
			print('1 - Intel')
			print('2 - Atheros')
			print('3 - Realtek8111')
			net = input('Choice 1 - 3: ')
			try:
				net = int(net)
				if net == 1:
					print('Downloading Intel Drivers')
					self.d.Download(url=self.Intel, path='Kexts')
		
				elif net == 2:
					print('Downloading Atheros Drivers')
					ocu = self.d.OpenAsJSON(self.Atheros)
					for k in ocu[0]['assets']:
						if ".zip" in k['browser_download_url']:
							self.d.Download(url=k['browser_download_url'], path='Kexts')

				else:
					print('Downloading Realtek Drivers')
					ocu = self.d.OpenAsJSON(self.Realtek)
					for k in ocu[0]['assets']:
						if ".zip" in k['browser_download_url']:
							self.d.Download(url=k['browser_download_url'], path='Kexts')
				
				break
			except Exception as e:
				print(e)

	def Drivers(self):
		self.u.clear()
		self.u.title('Driver Downloader')
		self.d.Download(url=self.HFPlus, path='Drivers')

	def Unzip(self):
		self.u.clear()
		self.u.title("Unzipping Kext Files")
		for k in os.listdir('Kexts/'):
			self.d.unZipper('Kexts/', k)


		time.sleep(2)
		self.u.clear()
		self.u.title("Unzipping OpenCore Files")
		self.d.unZipper('Opencore/')

		time.sleep(2)
		self.u.clear()
		self.u.title('Unzipping Driver Files')
		self.d.unZipper('Drivers/')

	def moveKexts(self):
		print('Moving Kexts')
		if os.path.exists(f'Kexts/-patch.zip/Kexts/VirtualSMC.kext'):
			print('Moving VirtualSMC')
			shutil.move(f'Kexts/-patch.zip/Kexts/VirtualSMC.kext', f'{self.EFI}/EFI/OC/Kexts/')
		
		try:
			# Move Kexts
			k = os.listdir("Kexts")
			for kext in k:
				for K in os.listdir(f'Kexts/{kext}'):
					if K.endswith('.kext'):
						time.sleep(0.05)
						if os.path.exists(f'Kexts/{kext}/{K}'):
							print(f"Moving {K} to EFI")
							shutil.move(f'Kexts/{kext}/{K}', f'{self.EFI}/EFI/OC/Kexts/')
		except Exception as e:
			print(e)
			pass

		print('Completed')

	def moveEFI(self):
		o = os.listdir("Opencore")
		if not os.path.exists(f'{self.EFI}/EFI'):
			time.sleep(0.05)
			print("Moving EFI Folder")
			shutil.move(f'Opencore/{o[0]}/EFI', f'{self.EFI}/')

	def moveDrivers(self):
		print('Moving Drivers')
		# check for actual files
		if os.path.exists('Drivers/-AppleSupport-2.1.5-RELEASE.zip/Drivers/ApfsDriverLoader.efi'):
			print('Moving APFS Driver')
			shutil.move('Drivers/-AppleSupport-2.1.5-RELEASE.zip/Drivers/ApfsDriverLoader.efi', f'{self.EFI}/EFI/OC/Drivers/')

		if os.path.exists('Drivers/HFSPlus.efi'):
			print('Moving HFSPlus')
			shutil.move('Drivers/HFSPlus.efi', f'{self.EFI}/EFI/OC/Drivers/')			

	def getConfig(self):
		if not os.path.exists('PlistMerge'): os.mkdir('PlistMerge')
		o = os.listdir("Opencore")
		print('Moving Sample')
		time.sleep(0.05)
		if os.path.exists(f'Opencore/{o[0]}/Docs/Sample.plist'):
			shutil.move(f'Opencore/{o[0]}/Docs/Sample.plist', 'PlistMerge')
		
		p = os.listdir('Patches')
		for pat in p:
			if pat.endswith('.plist'):
				print('moving patches')
				time.sleep(0.05)
				patConf = pat
				shutil.move(f'Patches/{pat}', 'PlistMerge')
				break

		self.patchConf = self.p.openFile(f'PlistMerge/{patConf}')
		self.sampleConf = self.p.openFile('PlistMerge/Sample.plist')
		p = Plistread.Plistread('PlistMerge', self.sampleConf, self.patchConf)
		smb = self.macser.main()
		if 'Pro' in smb[0]:
			self.AppleMCED()

		p.patchToConf(f"{self.EFI}/EFI/OC", self.Null, smb)
		p.savePlist()

		if os.path.exists('PlistMerge/config.plist'):
			print('Moving Completed Config')
			time.sleep(0.05)
			shutil.move('PlistMerge/config.plist', f'{self.EFI}/EFI/OC')

	def cleanEFI(self):
		print('Clean up')
		time.sleep(2)
		print('Removing')
		drivers = ['ApfsDriverLoader.efi','FwRuntimeServices.efi','HFSPlus.efi']
		for c in os.listdir(f"{self.EFI}/EFI/OC/Drivers/"):
			if not c in drivers:
				print(f' - {c}')
				time.sleep(0.05)
				os.remove(f'{self.EFI}/EFI/OC/Drivers/{c}')
		
	def createStructure(self):
		self.u.clear()
		self.u.title('OpenCore EFI Structure')
		if not os.path.exists('Results'):
			os.mkdir('Results')

		self.EFI = f"Results/EFI-{self.Name}"
		if not os.path.exists(self.EFI):
			os.mkdir(self.EFI)

		self.moveEFI()
		self.moveKexts()
		self.moveDrivers()
		self.getConfig()
		self.cleanEFI()
		self.cleanUp()

		self.status = 'EFI Structure has been created\n\n'
		time.sleep(1)

	def mergePatches(self):
		self.u.title('OpenCore Patch Updater')
		if not os.path.exists('PatchMerge'):
			os.mkdir('PatchMerge')
		
		self.CPUSelect()
		for p in os.listdir('Patches'):
			if p.endswith('.plist'):
				self.patConf = p
				print('moving patches')
				time.sleep(0.05)
				shutil.move(f'Patches/{self.patConf}', f'PatchMerge/{self.patConf}')
				break

		if os.path.exists(f'PatchMerge/{self.patConf}'):
			self.patchConf = self.p.openFile(f'PatchMerge/{self.patConf}')

			print('Please Paste in config.plist to update')
			input('press [enter] or any key when done')

			
			if os.path.exists('PatchMerge/config.plist'):
				self.sampleConf = self.p.openFile('PatchMerge/config.plist')
				p = Plistread.Plistread('PatchMerge', self.sampleConf, self.patchConf)
				p.patchMerge()
				p.savePlist('updated-confing')
			else:
				print('You are missing one or both files or they are not named correct')

	def SMBIOSGen(self):
		self.genSMB()
		self.u.clear()
		self.u.title(f'SMBIOS for {self.Model}')
		print(f'Serial Number - {self.SN}')
		print(f'MLB(BoardSerialNumber) - {self.MLB}')
		print(f'UUID - {self.UUID}')
		input('[enter] to continue')
	
	def genSMB(self):
		ms = self.macser.main()
		self.Model = ms[0]
		self.SN = ms[1]
		self.MLB = ms[2]
		self.UUID = ms[3]	

if __name__ == '__main__':
	EFIMaker().main()