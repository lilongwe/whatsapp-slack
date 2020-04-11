from io import IOBase, TextIOWrapper, StringIO
from typing import Union, Dict
from datetime import datetime
from reader.Line import Line
from utilities.ParameterValidator import ParameterValidator

class CVSFileWriter(object):

	FORMAT_STRING:str = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'

	def __init__(self, 
				fileHandle:Union[StringIO,TextIOWrapper,str], 
				channel:str=None, 
				delimiter:str=None, 
				overrideUsername:bool=None,
				validator:ParameterValidator=ParameterValidator()):

		try:
			if isinstance(fileHandle, TextIOWrapper):
				if (fileHandle.mode.count("w")) == 0:
					raise IOError("File needs to be in write mode")
				self._file:TextIOWrapper = fileHandle
			elif isinstance(fileHandle, str):
				self._file:TextIOWrapper = open(fileHandle, "w")
			elif isinstance(fileHandle, StringIO):
				self._file:TextIOWrapper = fileHandle
			else:
				raise TypeError("Only type <File> or <string> or <StringIO> are allowed")
		except TypeError as error:
			raise error

		self._channel = validator.validateString(channel, "whatsapp")

		self._delimiter = validator.validateString(delimiter, ",")

		self._overrideUsername = overrideUsername if (overrideUsername is not None 
									and type(overrideUsername) == bool) else False


	def setOverrideUsername(self, override:bool):
		self._overrideUsername = bool(override)

	def write(self, line:Line):

		new_line:str = self.FORMAT_STRING.format(self._delimiter,
						int(line.getDate().timestamp()),
						self._channel,
						line.getUsername(),
						line.getContent().replace('"','""'))

		self._file.write(new_line+"\n")