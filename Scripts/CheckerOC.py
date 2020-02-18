import plistlib
import os
import sys
import time

# Check For Clover Structure
# Check OC Structure

class CheckerOC:
	def __init__(self):
		self.ERRORS = ''
		self.drivers = ['FwRuntimeServices.efi','ApfsDriverLoader.efi','HFSPlus.efi']
		self.UEFI = {"Protocols":{"AppleBootPolicy":False,"AppleEvent":False,"AppleImageConversion":False,"AppleKeyMap":False,"AppleUserInterfaceTheme":False,"ConsoleControl":True,"DataHub":False,"DeviceProperties":False,"FirmwareVolume":False,"HashServices":False,"OSInfo":False,"UnicodeCollation":False}, "Quirks":{"AvoidHighAlloc":False,"ExitBootServicesDelay":0,"IgnoreInvalidFlexRatio":False,"IgnoreTextInGraphics":False,"ProvideConsoleGop":True,"ReleaseUsbOwnership":False,"RequestBootVarRouting":True,"ReplaceTabWithSpace":False,"SanitiseClearScreen":True,"ClearScreenOnModeSwitch":False}}
		self.BOOTER = {"Quirks":{"SignalAppleOS":False,"AvoidRuntimeDefrag":True,"DevirtualiseMmio":False,"DisableVariableWrite":False,"DisableSingleUser":False,"DiscardHibernateMap":False,"EnableSafeModeSlide":True,"EnableWriteUnprotector":True,"ForceExitBootServices":False,"ProtectCsmRegion":False,"ProvideCustomSlide":True,"SetupVirtualMap":True,"ShrinkMemoryMap":False,"SignalAppleOs":False}}
		self.KERNEL = {"Quirks":{"IncreasePciBarSize":False,"AppleXcpmForceBoost":False,"DummyPowerManagement":True,"AppleCpuPmCfgLock":False,"AppleXcpmCfgLock":False,"AppleXcpmExtrasMsrs":False,"AppleXcpmForceBoost":False,"CustomSMBIOSGuid":False,"DisableIOMapper":False,"DummyPowerManagement":True,"ExternalDiskIcons":True,"LapicKernelPanic":False,"PanicNoKextDump":True,"PowerTimeoutKernelPanic":True,"ThirdPartyDrives":False,"XhciPortLimit":True}}
		self.MISC = {"Boot":{"TakeoffDelay":0,"BuiltinTextRenderer":False,"HideSelf":True,"PollAppleHotKeys":False,"ShowPicker":True},"Debug":{"DisableWatchDog":False},"Security":{"AuthRestart":False,"AllowSetDefault":True,"AllowNvramReset":True,"AllowSetDefault":True,"AuthRestart":False,"RequireSignature":False,"RequireVault":False,"ScanPolicy":0}}
		self.NVRAM = {"LegacyEnable":False, "WriteFlash":True, "LegacyOverwrite":False}
		self.PLATINFO = {"Automatic":True,"Generic":{"AdviseWindows":False,"MLB":"M000000000001","SpoofVendor":False,"SystemSerialNumber":"W0000000001","SystemUUID":"00000000-0000-0000-0000-000000000000"},"UpdateDataHub":True,"UpdateNVRAM":True,"UpdateSMBIOS":True,"UpdateSMBIOSMode":"Create"}
		self.KEXTS = ['WhateverGreen.kext', 'Lilu.kext', 'VirtualSMC.kext','AppleMCEReporterDisabler.kext']
		# Needed For iMacPro
		self.OCStructure = {"ACPI":{"Add":None,"Block":None,"Patch":None,"Quirks":['FadtEnableReset','NormalizeHeaders','RebaseRegions','ResetHwSig','ResetLogoStatus']},
		"Booter":{"MmioWhitelist":None,"Quirks":["SignalAppleOS","AvoidRuntimeDefrag","DevirtualiseMmio","DisableSingleUser","DisableVariableWrite","DiscardHibernateMap","EnableSafeModeSlide","EnableWriteUnprotector","ForceExitBootServices","ProtectCsmRegion","ProvideCustomSlide","SetupVirtualMap","ShrinkMemoryMap","SignalAppleOs"]},
		"DeviceProperties":{"Add":None,"Block":None},
		"Kernel":{"Add":None,"Block":None,"Emulate":None,"Patch":None,"Quirks":["AppleCpuPmCfgLock","AppleXcpmForceBoost","DummyPowerManagement","IncreasePciBarSize","AppleXcpmCfgLock","AppleXcpmExtraMsrs","CustomSMBIOSGuid","DisableIoMapper","ExternalDiskIcons","LapicKernelPanic","PanicNoKextDump","PowerTimeoutKernelPanic","ThirdPartyDrives","XhciPortLimit"]},
		"Misc":{"BlessOverride":None,"Boot":['TakeoffDelay','BuiltinTextRenderer','ConsoleBehaviourOs','ConsoleBehaviourUi','ConsoleMode','HibernateMode','HideSelf','PollAppleHotKeys','Resolution','ShowPicker','Timeout','UsePicker'],"Debug":['DisableWatchDog','DisplayDelay','DisplayLevel','Target'],"Entries":None,"Security":['AllowSetDefault','AuthRestart','AllowNvramReset','ExposeSensitiveData','HaltLevel','RequireSignature','RequireVault','ScanPolicy'],"Tools":None},
		"NVRAM":{"Add":None,"Block":None,"LegacyEnable":None,"LegacyOverwrite":False,"WriteFlash":True,"LegacySchema":None},
		"PlatformInfo":{"Automatic":None,"DataHub":None,"Generic":["AdviseWindows","MLB","ROM","SpoofVendor","SystemProductName","SystemSerialNumber","SystemUUID"],"PlatformNVRAM":None,"SMBIOS":None,"UpdateDataHub":None,"UpdateNVRAM":None,"UpdateSMBIOS":None,"UpdateSMBIOSMode":None},
		"UEFI":{"ConnectDrivers":None,"Drivers":None,"Input":['KeyForgetThreshold','KeyMergeThreshold','KeySupport','KeySupportMode','KeySwap','PointerSupport','PointerSupportMode','TimerResolution'],"Protocols":['AppleSmcIo','OSInfo','AppleBootPolicy','AppleEvent','AppleImageConversion','AppleKeyMap','AppleUserInterfaceTheme','ConsoleControl','DataHub','DeviceProperties','FirmwareVolume','HashServices','UnicodeCollation'],"Quirks":['AvoidHighAlloc','ClearScreenOnModeSwitch','ExitBootServicesDelay','IgnoreInvalidFlexRatio','IgnoreTextInGraphics','ProvideConsoleGop','ReconnectOnResChange','ReleaseUsbOwnership','ReplaceTabWithSpace','RequestBootVarFallback','RequestBootVarRouting','SanitiseClearScreen','UnblockFsConnect']}
		}

	def clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')
		
	def main(self,  path=None, defPath=None):
		self.path = path
		self.defPath = defPath
		try:
			os.chdir(self.path)
		except:
			pass
		self.clear()
		self.loadConfig()
		if self.loadConfig() == False: return
		time.sleep(0.05)
		self.clear()
		self.Struct()
		self.Folders()
		self.Config()
		return self.DisplayERRORS()

	def loadConfig(self):
		try:
			os.chdir(self.path)
		except:
			pass

		try:	
			c = open('config.plist', 'rb')
			self.config = plistlib.load(c)
			print("Loaded Config")
		except FileNotFoundError:
			print('Invalid Location. Cannot find Config.plist')
			return False


	def Config(self):
		self.clear()
		time.sleep(0.05)
		self.checkACPI()
		self.clear()
		time.sleep(0.05)
		self.checkBooter()
		self.clear()
		time.sleep(0.05)
		self.checkKernel()
		self.clear()
		time.sleep(0.05)
		self.checkMisc()
		self.clear()
		time.sleep(0.05)
		self.checkNVRAM()
		self.clear()
		time.sleep(0.05)
		self.checkPlat()
		self.clear()
		time.sleep(0.05)
		self.checkUEFI()
		self.clear()
		time.sleep(0.05)

	def Folders(self):
		self.checkDriversFolder()
		time.sleep(0.05)
		self.clear()
		self.checkKextsFolder()
		time.sleep(0.05)
		self.clear()
		self.checkACPIFolder()
		time.sleep(0.05)
		self.clear()

	def Struct(self):
		self.checkOCStruct()
		self.clear()
		time.sleep(0.05)
		self.checkOCStructFile()
		self.clear()

	def checkOCStruct(self):
		try:
			os.chdir(self.path)
		except:
			pass

		E = ''
		if os.path.exists('config.plist'):
			print('Right Folder')

		DIR = ['ACPI/','Drivers/','Kexts/','Tools/','OpenCore.efi']

		for i in DIR:
			if os.path.exists(i):
				time.sleep(0.05)
				print(f'{i} Folder Exists')
			else:
				E += f"\n - Missing {i} File/Folder"

		if os.path.exists('../BOOT/'):
			if os.path.exists('../BOOT/BOOTX64.efi') or os.path.exists('../BOOT/BOOTx64.efi'):
				time.sleep(0.05)
				print(f'File BOOTX64.efi Exists')
			else:
				E += f"\n - Missing BOOTx64.efi File"
		else:
			E += f"\n - Missing BOOT Folder"
			E += f"\n - Missing BOOTX64.efi File"

		if not E == '':
			self.ERRORS += 'OC Folder Structure Missing'
			self.ERRORS += E
		time.sleep(2)

	def checkOCStructFile(self):
		print('\nChecking File Structure')
		E = ''
		for c in self.config:
			time.sleep(0.05)
			if not "#WARNING - 1" in c and not "#WARNING - 2" in c and not "#WARNING - 3" in c and not "#WARNING - 4" in c and not "#WARNING - 5" in c:
				print(c)
				try:
					self.OCStructure[c]
					for d in self.config[c]:
						time.sleep(0.05)
						print(f' - {d}')
						try:
							self.OCStructure[c][d]
							try:	
								for g in self.config[c][d]:
									if not g in self.OCStructure[c][d]:
										E += f"\n - {g} Not part of Config Structure. Found: {c} -> {d}"
							except TypeError as e:
								pass
						except KeyError as e:
							print(f'Missing from config {d}')
							E += f"\n - {d} Not part of Config Structure. Found: {c}"
				except KeyError as e:
					print(f'Missing from config {c}')
					E += f"\n - {c} Not part of Config Structure"

		if not E == '':
			self.ERRORS += "File Structure Error"
			self.ERRORS += E
		time.sleep(2)
				
		
	#######  UEFI Drivers  #######
	def checkDriversFolder(self):
		try:
			os.chdir(self.path)
		except:
			pass

		print('Scanning Drivers Folder')
		self.DF = os.listdir('Drivers/')
		if '.DS_Store' in self.DF:
			self.DF.remove('.DS_Store')

		defaults = ['hfsplus.efiorvboxplus.efi', 'apfsdriverloader.efi', 'fwruntimeservices.efi']
		for d in self.DF:
			time.sleep(5)
			print(f' - found {d}')
			if d.lower() == 'hfsplus.efi' or d.lower() == 'vboxplus.efi': defaults.remove('hfsplus.efiorvboxplus.efi')
			if d.lower() == 'fwruntimeservices.efi': defaults.remove(d.lower())
			if d.lower() == 'apfsdriverloader.efi': defaults.remove(d.lower())

		if defaults != []:
			self.ERRORS += '\nMissing Drivers'
			for d in defaults:
				self.ERRORS += f"\n - {d}"

		if self.DF == []:
			print('No Files in Folder')		
		time.sleep(3)
	
	#######  Kext Folder  #######
	def checkKextsFolder(self):
		if not self.path: os.chdir(self.path)
		print('Checking Kext Folder')
		E = ''
		self.Kexts = os.listdir('Kexts')
		if '.DS_Store' in self.Kexts:
			self.Kexts.remove('.DS_Store')

		if self.Kexts == []:
			print('Folder empty')
		for ke in self.Kexts:
			print(f" - Found {ke}")

		for k in self.KEXTS:
			time.sleep(0.05)
			if not k in self.Kexts:
				t = ''
				if 'AppleMCEReporterDisabler' in k:
					t = ' (Only Needed For Catalina For SMBIOS\'s: iMacPro1,1, MacPro7,1 and MacPro6,1)'
				E += f"\n - {k}{t}"

		if not E == '':
			self.ERRORS += "\nMissing Kexts"
			self.ERRORS += E
		time.sleep(2)

	#######  ACPI SSDT #######
	def checkACPIFolder(self):
		print("Scanning ACPI Folder")
		af = os.listdir('ACPI')
		if '.DS_Store' in af:
			af.remove('.DS_Store')
		
		if af != []:
			for a in af:
				time.sleep(0.05)
				print(f' - Found {a}')
		else:
			print('Folder Empty')
		
		self.af = af
		time.sleep(2)

	#######  APCI  #######	
	def checkACPI(self):
		print('Checking ACPI')
		check = 'ACPI'
		A = ""
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f' - Checking {c}')

				for a in self.config[check][c]:
					if 'Add' in c:
						print(f" = Found {a['Path']}")
						try:	
							if not a['Path'] in self.af:
								A += f"\n - Add {a['Path']} to Folder or Remove From Config"
						except AttributeError:
							pass

					if 'Quirks' in c:
						q = self.config[check][c][a]
						if q != False:
							A += f"\n - {a} set to False"
		if not A == '':
			self.ERRORS += "\nACPI Errors"
			self.ERRORS += A

		time.sleep(2)

	#######  Booter  #######
	def checkBooter(self):
		print('Checking Booter')
		check = 'Booter'
		B = ''
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f' - Checking {c}')
				if 'Quirks' == c:
					for q in self.config[check][c]:
						time.sleep(0.05)
						print(f' = {q}')
						try:
							if self.config[check][c][q] != self.UEFI[c][q]:
								B += f"\n - {q} needs to be set to {self.UEFI[c][q]}"
						except KeyError:
							pass

		if not B == '':
			self.ERRORS += "\nBooter Errors"
			self.ERRORS += B
		time.sleep(2)

	#######  Kernel  #######
	def checkKernel(self):
		print("Checking Kernel")
		check = 'Kernel'
		K = ''
		if check in self.config:
			for c in self.config[check]:
				print(f' - Checking {c}')
				time.sleep(0.05)
				if 'Add' == c:
					qu = []
					for q in self.config[check][c]:
						print(f" - {q['BundlePath']}")
						qu.append(q['BundlePath'])
					
					try:
						for k in self.Kexts:
							if not k in qu:
								K += f"\n - {k} is missing from config"
					except:
						for k in qu:
							if not k in self.KEXTS:
								K += f"\n - {k} is missing from config"

				if 'Quirks' == c:
					for q in self.config[check][c]:
						try:
							if self.config[check][c][q] != self.KERNEL[c][q]:
								K += f"\n - {q} needs to be set to {self.KERNEL[c][q]}"
						except KeyError:
							pass
		if not K == "":
			self.ERRORS += "\nMissing Kernels"
			self.ERRORS += K
		time.sleep(2)

	#######  Misc  #######
	def checkMisc(self):
		check = 'Misc'
		M = ''
		print('Checking Misc')
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f" - Checking {c}")
				if 'Security' == c or 'Debug' == c or 'Boot' == c:
					for q in self.config[check][c]:
						try:
							if self.config[check][c][q] != self.MISC[c][q]:
								M += f"\n - {q} needs to be set to {self.MISC[c][q]}"
						except KeyError:
							pass

		if not M == '':
			self.ERRORS += "\nMisc Errors"
			self.ERRORS += M
		time.sleep(2)

	#######  NVRAM  #######
	def checkNVRAM(self):
		print('Checking NVRAM')
		check = 'NVRAM'
		E = ''
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f' - Checking {c}')
				if 'LegacyEnable' == c:
					try:
						if self.NVRAM[c] != self.config[check][c]:
							E += f"\n - {c} needs to be set to {self.NVRAM[c]}"
					except KeyError:
						pass

				if c == 'WriteFlash':
					try:
						if self.NVRAM[c] != self.config[check][c]:
							E += f"\n - {c} needs to be set to {self.NVRAM[c]}"
					except KeyError:
						pass

		if not E == '':
			self.ERRORS += '\nNVRAM Error'
			self.ERRORS += E

		time.sleep(2)

	#######  Platforminfo  #######
	def checkPlat(self):
		print("Checking Platform Info")
		check = 'PlatformInfo'
		P = ''
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f' - Checking {c}')
				if 'UpdateSMBIOS' in c or 'UpdateNVRAM' in c or 'UpdateDataHub' in c or 'Automatic' in c or 'UpdateSMBIOSMode' in c:
					if self.config[check][c] != self.PLATINFO[c]:
						if self.PLATINFO[c] != self.config[check][c]:
							P += f" - \n{c} needs to be set to {self.PLATINFO[c]}"

				if 'Generic' in c:
					for g in self.config[check][c]:
						time.sleep(0.05)
						print(f' = Checking {g}')
						try:
							if str(self.config[check][c][g]) in str(self.PLATINFO[c][g]):
								if 'AdviseWindows' in g:
									P += f"\n - {g} needs to be Changed from {self.PLATINFO[c][g]} to True"
								else:	
									P += f"\n - {g} needs to be Changed from {self.PLATINFO[c][g]} to a Valid {g}"
						except KeyError as e:
							pass
		if not P == '':
			self.ERRORS += '\nPlatform Info Errors'
			self.ERRORS += P
			self.ERRORS += '\n######  Use GenSMBIOS From CorpNewt  ######\n'
		time.sleep(2)

	#######  UEFI #######
	def checkUEFI(self):
		print('Checking UEFI')
		check = 'UEFI'
		U = ''
		if check in self.config:
			for c in self.config[check]:
				time.sleep(0.05)
				print(f' - Checking {c}')
				if 'Drivers' == c:
					for ud in self.config[check][c]:
						time.sleep(0.05)
						print(f' = Checking {ud}')
						if not ud in self.DF:
							U += f"\n - {ud} Not Found In Folder"

				if 'ConnectDrivers' == c and self.config[check]['ConnectDrivers'] == False:
					U += f" - {self.config[check]['ConnectDrivers']} set to True\n"
					
				if 'Protocols' == c:
					for q in self.config[check][c]:
						time.sleep(0.05)
						print(f' = Checking {q}')
						try:
							if self.config[check][c][q] != self.UEFI[c][q]:
								U += f"\n - {q} needs to be set to {self.UEFI[c][q]}"
						except KeyError:
							pass

				if 'Quirks' == c:
					for q in self.config[check][c]:
						time.sleep(0.05)
						print(f' = Checking {q}')
						try:
							if self.config[check][c][q] != self.UEFI[c][q]:
								U += f"\n - {q} needs to be set to {self.UEFI[c][q]}"
						except KeyError:
							pass
		if not U == '':
			self.ERRORS += '\nUEFI Errors'
			self.ERRORS += U
		time.sleep(2)

	#######  Display Errors  #######
	def DisplayERRORS(self):
		if self.ERRORS != '':
			print(self.ERRORS)
			input('[enter] to return back to menu')
			return ''
		else:
			txt = 'No Errors Were Found'
			return txt