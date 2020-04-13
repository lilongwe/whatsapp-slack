
class ParameterValidator(object):

	def __init__(self):
		"""
		Nothing to see here
		"""

	def validateString(self, string:str, default:str=None) -> str:
				
		string = string if (string is not None 
									and type(string) == str 
									and len(string.strip()) > 0) else (default if default is None else str(default))

		return string

	def validateInteger(self, integer:int, default:int=None) -> str:
		
		try:
			integer = integer if (integer is not None 
										and type(integer) == int) else (default if default is None else int(default))
		except ValueError:
			integer = None

		return integer