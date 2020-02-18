import os, time, urllib, sys, json, shutil, requests

if sys.version_info >= (3,0):
	import zipfile
	from urllib.parse import urlparse
	from urllib.request import urlopen, Request
else:
	import urllib2
	from urllib2 import urlopen, Request
	from urlparse import urlparse

try:
	import patoolib
	import magic
	from pyunpack import Archive
	import wget
except:
	os.system('pip install --user pyunpack patool python-magic patool wget')
	import magic
	from pyunpack import Archive
	import patoolib
	import wget

class Downloader:
	def __init__(self, **kwargs):
		self.ua = kwargs.get('useragent',{'User-Agent':'Mozilla'})

	def openUrl(self, url, headers=None):
		headers = self.ua if headers == None else headers
		try:
			response = urlopen(Request(url, headers=headers))
		except Exception as e:
			print(e)
			return
		return response
		
	def OpenAsJSON(self, u):
		with self.openUrl(u) as url:
			data = json.loads(url.read().decode())
			return data

	def Download(self, url=None, path=None, output=None, wgetForce=False):
		if not path: path = ''
		if not os.path.exists(path): os.mkdir(path)
		if not url: return print('No URL Given')
		if not 'http://' in url and not 'https://' in url: return print('Not a URL')
		response = self.openUrl(url)
			
		a = urlparse(url)
		name = a.path
		if not output:
			FILE = name.replace('/','_')
			FILE = FILE.split('_')[len(FILE.split('_'))-1]
		else:
			FILE = output

		time.sleep(0.05)
		_path = f'{path}/{FILE}'
		try:
			if os.path.exists(_path):
				os.remove(_path)
		except IsADirectoryError:
			pass
		
		if wgetForce == False:
			try:
				r = requests.get(url)
				with open(_path, 'wb') as f:
					f.write(r.content)
			except Exception as e:
				datatowrite = response.read()
				with open(_path, 'wb') as f:
					f.write(datatowrite)
		else:
			wget.download(url, out=path)
		
		time.sleep(2)
		print('\nDownload Complete')

	def GitDL(self, url, path):
		if not 'https://api.github.com' in url and not 'https://api.github.com' in url: return print('Not a valid API Link')
		ocu = self.OpenAsJSON(url)
		for k in ocu[0]['assets']:
			if "RELEASE" in k['browser_download_url']:
				self.Download(url=k['browser_download_url'], path=path)

	def unZipper(self, path, file=None, folder=None):
		try:
			if not file:
				f = os.listdir(path)
				for file in f:
					if file.endswith('.zip'):
						xfile, ext = os.path.splitext(file)
						if ext:
							if folder: 
								self.zip = folder
							else:
								self.zip = f'-{file}'

							# file_name, ext = os.path.splitext(file)
							if not os.path.exists(f'{path}/{self.zip}'):
								os.mkdir(f'{path}/{self.zip}')
							
							if ext == '.x-xar':
								file = xfile+'.zip'
								print(file)

						break

			print('Unzipping')
			if os.path.isfile(f'{path}/{file}'):
				try:
					patoolib.extract_archive(f'{path}/{file}', outdir=f'{path}/{self.zip}')
				except Exception as e:
					with zipfile.ZipFile(f'{path}/{file}', 'r') as zip_ref:
						zip_ref.extractall(f'{path}/{self.zip}')
			
			if os.path.isfile(f'{path}/{self.zip}'):
				try:
					os.remove(f'{path}/{file}')
				except IsADirectoryError:
					if sys.platform == "linux":
						os.system(f'sudo rm -r {path}/{file}')
					else:
						shutil.rmtree(f'{path}/{file}')
				time.sleep(0.05)
			print('Unzipped')
		except FileNotFoundError:
			return print(f'No Path: {path}')

	def Zipper(self, path, folder=None):
		pass
		
# Downloader(url='https://github.com/acidanthera/OpenCorePkg/releases/download/0.5.3/OpenCore-0.5.3-RELEASE.zip', path='OpenCore', Zip='EFI').downloadDef()