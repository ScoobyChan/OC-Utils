import plistlib
import json
import base64
import os
import time

class Plistread:
	def __init__(self, Loc, sample, patch):
		self.dp = []
		self.kexts = []
		self.Loc = Loc
		self.patchConf = patch
		self.sampleConf = sample

	def text(self):
		print('Hello')

	def kextToPlist(self,BundlePath,Comment,Enabled=True,ExecutablePath='',MaxKernel='',MinKernel='',PlistPath='Contents/Info.plist'):
		if 'AppleMCEReporter' in BundlePath:
			MinKernel = '19.0.0'
		k = {'BundlePath':BundlePath,'Comment':Comment,'Enabled':Enabled,'ExecutablePath':ExecutablePath,'MaxKernel':MaxKernel,'MinKernel':MinKernel,'PlistPath':PlistPath}
		return k

	def mergeKexts(self):
		lsK = os.listdir(self.Loc+'/Kexts')
		if os.path.exists(self.Loc+'/Kexts/Lilu.kext'):
			try:
				t = os.listdir(self.Loc+"/Kexts/Lilu.kext/Contents/MacOS")[0]
				kext = self.kextToPlist(BundlePath="Lilu.kext",Comment="Lilu",ExecutablePath=f'Contents/MacOS/Lilu')
				self.kexts.append(kext)
			except Exception as e:
				kext = self.kextToPlist(self.Loc+"Lilu.kext","Lilu.kext")
				self.kexts.append(kext)

		if os.path.exists(self.Loc+'/Kexts/VirtualSMC.kext'):
			try:
				t = os.listdir(self.Loc+"/Kexts/VirtualSMC.kext/Contents/MacOS")[0]
				kext = self.kextToPlist(BundlePath="VirtualSMC.kext",Comment="VirtualSMC",ExecutablePath=f'Contents/MacOS/VirtualSMC')
				self.kexts.append(kext)
			except Exception as e:
				kext = self.kextToPlist("VirtualSMC.kext","VirtualSMC.kext")
				self.kexts.append(kext)

		for ls in lsK:
			if not 'Lilu' in ls and not 'VirtualSMC' in ls:
				try:

					t = os.listdir(self.Loc+"/Kexts/"+ls+"/Contents/MacOS")[0]
					kext = self.kextToPlist(BundlePath=ls,Comment=t,ExecutablePath=f'Contents/MacOS/{t}')
					self.kexts.append(kext)
				except Exception as e:
					kext = self.kextToPlist(ls,ls)
					self.kexts.append(kext)
		return self.kexts

	def patch(self):
		try:
			for c in self.patchConf:
				# print(c)
				try:    
					for d in self.patchConf[c]:
						# print(f'{c} -> {d}')
						if d == 'Patch' and c == 'Kernel':
							try:
								for e in self.patchConf[c][d]:
									# print(f'{c} -> {d} -> {e}\n\n')
									
									# e['Find'] = base64.b64encode(e['Find'])
									# e['Mask'] = base64.b64encode(e['Mask'])
									# e['Replace'] = base64.b64encode(e['Replace'])
									# e['ReplaceMask'] = base64.b64encode(e['ReplaceMask'])

									# e['Find'] = e['Find'].hex()#base64.b64encode(e['Find'])
									# e['Mask'] = e['Mask'].hex()#base64.b64encode(e['Mask'])
									# e['Replace'] = e['Replace'].hex()#base64.b64encode(e['Replace'])
									# e['ReplaceMask'] = e['ReplaceMask'].hex() #base64.b64encode(e['ReplaceMask'])
									
									self.dp.append(e)
							except Exception as e:
								# print(e)
								pass
				except Exception as e:
					pass
		except Exception as e:
			pass

		return self.dp

	def driversToPlist(self):
		d = os.listdir(self.Loc+'Drivers')
		return d

	def patchToConf(self, pLoc, dummyPM=False, smb=None):
		self.Model = smb[0]
		self.SN = smb[1]
		self.MLB = smb[2]
		self.UUID = smb[3]	

		self.pLoc = pLoc
		print('Removing Warnings')
		del self.sampleConf['#WARNING - 1']
		del self.sampleConf['#WARNING - 2']
		del self.sampleConf['#WARNING - 3']
		del self.sampleConf['#WARNING - 4']
		del self.sampleConf['#WARNING - 5']

		for c in self.sampleConf:
			for d in self.sampleConf[c]:
				###########################
				# Kernel Section
				###########################
				if c == 'Kernel':
					print('Fixing Kernel')
					if d == 'Patch':
						# print(d)
						try:
							p = self.patch()
							self.sampleConf[c][d] = p 
						except Exception as e:
							print(e)
							pass

					if d == 'Add':
						try:
							p = self.mergeKexts()
							self.sampleConf[c][d] = p 
						except Exception as e:
							print(e)
							pass

					if d == 'Quirks':
						for e in self.sampleConf[c][d]:
							if e == 'ExternalDiskIcons' or e == 'PanicNoKextDump' or e == 'PowerTimeoutKernelPanic' or e == 'XhciPortLimit' or (dummyPM == True and e == 'DummyPowerManagement'):
								self.sampleConf[c][d][e] = True

				###########################
				# ACPI Section
				###########################
				if c == 'ACPI':
					print('Fixing ACPI')
					if d == 'Add' or d == 'Block' or d == 'Patch':
						try:
							self.sampleConf[c][d] = [] 
						except Exception as e:
							pass

				###########################
				# Device Properties Section
				###########################
				if c == 'DeviceProperties' and d == 'Add':
					print('Fixing DeviceProperties')
					try:
						self.sampleConf[c][d] = {}
					except Exception as e:
						pass

				###########################
				# Misc Section
				###########################
				if c == 'Misc':
					print('Fixing Misc')
					if d == 'Debug':
						for e in self.sampleConf[c][d]:
							if e == 'DisableWatchDog':
								self.sampleConf[c][d][e] = True

					if d == 'Security':
						for e in self.sampleConf[c][d]:
							if e == 'AllowNvramReset' or e == 'AllowSetDefault':
								self.sampleConf[c][d][e] = True

							if e == 'AuthRestart' or e == 'RequireSignature' or e == 'RequireVault':
								self.sampleConf[c][d][e] = False

							if e == 'ScanPolicy':
								self.sampleConf[c][d][e] = 0

				###########################
				# NVRAM Section
				###########################
				if c == 'NVRAM':
					print('Fixing NVRAM')
					if d == 'Add':
						for e in self.sampleConf[c][d]:
							if e == '7C436110-AB2A-4BBB-A880-FE41995C9F82':
								try:	
									for f in self.sampleConf[c][d][e]:	
										if f == 'boot-args':
											self.sampleConf[c][d][e][f] = '-v keepsyms=1 debug=0x100 alcid=1 agdpmod=pikera'
										
										# if f == 'csr-active-config':								
										# 	self.sampleConf[c][d][e][f] = b'\xe7\x03\x00\x00'

										if f == 'prev-lang:kbd':
											del self.sampleConf[c][d][e][f]
								except RuntimeError as e:
									print(e)

					if d == 'WriteFlash':
						self.sampleConf[c][d] = True


				###########################
				# PlatformInfo Section
				###########################
				if c == 'PlatformInfo':
					print('Fixing PlatformInfo')
					if d == 'Automatic':
						self.sampleConf[c][d] = True

					if d == 'DataHub' or d == 'SMBIOS':
						del self.sampleConf[c][d]

					# TO QUESTION
					# if d == 'AdviseWindows':
					# 	self.sampleConf[c][d] = True

					if d == 'Generic':
						print(d)
						for e in self.sampleConf[c][d]:
							print(e)
							if e == 'MLB':
								self.sampleConf[c][d][e] = self.MLB
							if e == 'SystemProductName':
								self.sampleConf[c][d][e] = self.Model
							if e == 'SystemSerialNumber':
								self.sampleConf[c][d][e] = self.SN
							if e == 'SystemUUID':
								self.sampleConf[c][d][e] = self.UUID


				###########################
				# UEFI Section
				###########################
				if c == 'UEFI':
					print('Fixing UEFI')
					if d == 'Drivers':
						# p = self.driversToPlist()
						# self.sampleConf[c][d] = p
						pass

					if d == 'Protocols':
						for e in self.sampleConf[c][d]:
							if e == 'ConsoleControl':
								self.sampleConf[c][d][e] = True

					if d == 'Quirks':
						for e in self.sampleConf[c][d]:
							if e == 'ProvideConsoleGop' or e == 'RequestBootVarFallback' or e == 'SanitiseClearScreen':
								self.sampleConf[c][d][e] = True

					if d == 'Input':
						for e in self.sampleConf[c][d]:
							if e == 'PointerSupportMode':
								self.sampleConf[c][d][e] = ''



	def patchMerge(self):
		for c in self.sampleConf:
			for d in self.sampleConf[c]:
				if c == 'Kernel':
					print('Merging Patches')
					if d == 'Patch':
						# print(d)
						try:
							p = self.patch()
							self.sampleConf[c][d] = p 
						except Exception as e:
							print(e)
							pass

	def savePlist(self, conf='config'):
		print('Saving Config')
		time.sleep(0.05)
		try:	
			fileName = f'{self.pLoc}/{conf}.plist'
		except:
			fileName = f'{conf}.plist'
		with open(fileName, 'wb') as fp:
			plistlib.dump(self.sampleConf, fp)
		time.sleep(0.05)
		print('Config Saved')