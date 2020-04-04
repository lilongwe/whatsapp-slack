from io import IOBase, BufferedReader
from typing import Union, Dict
import pathlib, os
from datetime import datetime


class FileReader(object):

	CONSOLE_PREFIX:str = "$ "
	FORMAT_STRING:str = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'
	DATE_FORMAT:str = "[%d/%m/%Y, %H:%M:%S]"

	CONTENT:str = "content"
	DATE:str = "date"
	USERNAME:str = "username"

	def __init__(self, fileHandle):

		try:
			if isinstance(fileHandle, IOBase):
				if (fileHandle.mode.count("b")) == 0:
					raise FileNotFoundError("File needs to be in binary read mode")
				self._file:BufferedReader = fileHandle
			elif isinstance(fileHandle, str):
				self._file:BufferedReader = open(fileHandle, "rb")
			else:
				raise TypeError("Only integers are allowed")
		except TypeError as error:
			raise error

		_seek = 0


	def file(self) -> BufferedReader:
		return self._file

	def read(self) -> Dict[str,Union[str,datetime]]:
		
		output_elements:Dict[str,Union[str,datetime]] = {}
		readNext = True

		while readNext:
			orig_line = self._file.readline()
			line = orig_line.decode().strip()

			try:
				dt = self._getDate(line.strip())
			except ValueError:
				readNext = len(orig_line) > 0
				if readNext:
					output_elements[self.CONTENT] += "\n"+line.strip()
			else:
				if output_elements.get("content", None) is not None:
					self._file.seek(0 - len(orig_line), os.SEEK_CUR)
					return output_elements

				# We can find a date at start of line, it's a new line
				line = line.strip()
				line = self._normaliseQuotes(line)

				output_elements[self.DATE] = dt

				output_elements[self.USERNAME] = self._getUsername(line)
				output_elements[self.CONTENT] = self._getContents(line, output_elements["username"])
		
		return output_elements


	def _getDate(self, line:str, format:str = DATE_FORMAT) -> datetime:
		return datetime.strptime(line[:22], format)

	def _normaliseQuotes(self, line:str) -> str:
		# Make sure to change all double quotes to standard ones
		for quote in ['"', '‟', '″', '˝', '“']:
			line = line.replace(quote, '\"')

		return line

	def _getUsername(self, line:str) -> str:
		
		username:str = None
		
		if line[23:].count(':') > 0: 
			username = line[23:].split(':')[0].strip()

		if username is None or len(username.strip()) == 0:
			raise NameError("No username found")

		return username

	def _getContents(self, line:str, username:str) -> str:
		
		content:str - None

		return line[23:].replace(username+":", "").strip()