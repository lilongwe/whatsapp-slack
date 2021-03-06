from datetime import datetime
from io import IOBase, StringIO, TextIOWrapper
from typing import Dict, Union

from whatsapp_slack.Line import Line
from whatsapp_slack.ParameterValidator import ParameterValidator
from whatsapp_slack.writer.Writer import Writer


class CSVFileWriter(Writer):

	FORMAT_STRING: str = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'
	CONSOLE_PREFIX: str = "$ "
	DEFAULT_CHANNEL_NAME: str = "whatsapp"
	DEFAULT_DELIMITER: str = ","

	TYPE_ERROR_EXCEPTION = (
							"Only type <File> or <string>"
							" or <StringIO> are allowed")

	def __init__(	
					self, 
					fileHandle: Union[StringIO, TextIOWrapper, str], 
					channel: str = None, 
					delimiter: str = None, 
					overrideUsername: bool = None,
					validator: ParameterValidator = ParameterValidator()):

		try:
			if isinstance(fileHandle, TextIOWrapper):
				if (fileHandle.mode.count("w")) == 0:
					raise IOError("File needs to be in write mode")
				self._file: TextIOWrapper = fileHandle
			elif isinstance(fileHandle, str):
				self._file: TextIOWrapper = open(fileHandle, "w")
			elif isinstance(fileHandle, StringIO):
				self._file: TextIOWrapper = fileHandle
			else:
				raise TypeError(self.TYPE_ERROR_EXCEPTION)
		except TypeError as error:
			raise error

		if (validator is not None and isinstance(validator, ParameterValidator)):
			self._validator = validator
		else:
			self._validator = ParameterValidator()

		self._channel = self._validator.validateString(
										channel, 
										self.DEFAULT_CHANNEL_NAME)

		self._delimiter = self._validator.validateString(
															delimiter, 
															self.DEFAULT_DELIMITER)

		if (overrideUsername is not None and type(overrideUsername) == bool):
			self._overrideUsername = overrideUsername
		else:
			self._overrideUsername = False

		self._usernames_mappings: Dict[str, str] = {}

	def close(self):
		self._file.close()

	def setOverrideUsername(self, override: bool):
		self._overrideUsername = bool(override)

	def write(self, line: Line):
		if line is not None and line.hasContent():

			username = line.getUsername()

			if self._overrideUsername:
				username = self._setUsername(username)

			new_line: str = self.FORMAT_STRING.format(
														self._delimiter,
														int(line.getDate().timestamp()),
														self._channel,
														username,
														line.getContent().replace('"', '""'))

			self._file.write(new_line+"\n")

	def _setUsername(self, username: str):

		username = self._validator.validateString(username)

		if username not in self._usernames_mappings.keys():

			output_username: str = ""

			output_username = input(
									"\n{0}Unknown username '{1}'. "
									"Enter corresponding Slack.com username (<Enter>=identical)"
									": ".format(self.CONSOLE_PREFIX, username))

			if len(output_username.strip()) > 0:
				usernames_mappings[username] = output_username.strip()
			else:
				usernames_mappings[username] = username
		
		return usernames_mappings.get(username, None)

	def self(self):
		return self

	def __repr__(self):
		return (
				f"{self.__class__.__name__}("
				f"{self._file!r}, {self._channel!r}, "
				f"{self._delimiter!r}, {self._overrideUsername!r}, "
				f"{self._validator!r})")
