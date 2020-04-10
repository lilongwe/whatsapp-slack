
class ParameterValidator(object):

	def __init__(self):
		"""
		Nothing to see here
		"""

	def validateString(self, string:str, default:str=None) -> str:
				
		string = string if (string is not None 
									and type(string) == str 
									and len(string) > 0) else (default if default is None else str(default))

		return string