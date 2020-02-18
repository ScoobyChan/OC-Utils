import os
class Utils:
	def __init__(self):
		pass

	def clear(self):
		try:
			os.system('clear')
		except:
			os.system('cls')

	def title(self, title):
		num =len(title)
		space = num + 8
		print(f'#####{"#"*space}#####')
		print(f"#####{' '*space}#####")
		print(f"#####    {title}    #####")
		print(f"#####{' '*space}#####")
		print(f'#####{"#"*space}#####')

# Utils().title('Hello Everybody')