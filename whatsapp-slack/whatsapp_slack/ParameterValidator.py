
class ParameterValidator(object):

	def validateString(self, string: str, default: str = None) -> str:		

		if (string is not None and type(string) == str and len(string.strip()) > 0):
			string = string
		elif (default is None):
			string = default
		else:
			string = str(default)

		return string

	def validateInteger(self, integer: int, default: int = None) -> int:

		try:

			if (integer is not None and type(integer) == int):
				integer = integer
			elif (default is None):
				integer = default
			else:
				integer = int(default)

		except ValueError:

			integer = None

		return integer
