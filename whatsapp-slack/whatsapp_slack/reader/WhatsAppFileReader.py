import os
import pathlib
from datetime import datetime
from io import BufferedReader
from typing import Dict, Union

from whatsapp_slack.Line import Line
from whatsapp_slack.reader.Reader import Reader
from whatsapp_slack.writer.Writer import Writer


class WhatsAppFileReader(Reader):

	CONSOLE_PREFIX: str = "$ "
	FORMAT_STRING: str = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'
	DATE_FORMAT: str = "[%d/%m/%Y, %H:%M:%S]"
	LINE_DATE_INDEX = 22
	LINE_USERNAME_INDEX = 23

	CONTENT: str = "content"
	DATE: str = "date"
	USERNAME: str = "username"

	def __init__(self, fileHandle: Union[BufferedReader, str]):

		try:
			if isinstance(fileHandle, BufferedReader):
				if (fileHandle.mode.count("b")) == 0:
					raise FileNotFoundError("File needs to be in binary read mode")
				self._file: BufferedReader = fileHandle
			elif isinstance(fileHandle, str):
				self._file: BufferedReader = open(fileHandle, "rb")
			else:
				raise TypeError("Only type <File> or <string> are allowed")
		except TypeError as error:
			raise error

	def close(self):
		self._file.close()

	def file(self) -> BufferedReader:
		return self._file

	def read(self) -> Line:
		
		output_elements: Dict[str, Union[str, datetime]] = {}
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
				if output_elements.get(self.CONTENT, None) is not None:
					self._file.seek(0 - len(orig_line), os.SEEK_CUR)
					return Line(
								output_elements[self.DATE], 
								output_elements[self.USERNAME], 
								output_elements[self.CONTENT])

				# We can find a date at start of line, it's a new line
				line = line.strip()
				line = self._normaliseQuotes(line)

				output_elements[self.DATE] = dt

				output_elements[self.USERNAME] = self._getUsername(line)
				output_elements[self.CONTENT] = self._getContents(
																	line, 
																	output_elements[self.USERNAME])
		
		if bool(output_elements):
			new_line: Line = Line(output_elements[
													self.DATE], 
													output_elements[self.USERNAME], 
													output_elements[self.CONTENT])
		else:
			new_line: Line = Line()

		return new_line

	def process(self, writer: Writer):

		line: Line = self.read()

		while True:
			writer.write(line)

			line = self.read()

			if line.hasContent() is False:
				break

	def _getDate(self, line: str, format: str = DATE_FORMAT) -> datetime:
		return datetime.strptime(line[:self.LINE_DATE_INDEX], format)

	def _normaliseQuotes(self, line: str) -> str:
		# Make sure to change all double quotes to standard ones
		for quote in ['"', '‟', '″', '˝', '“']:
			line = line.replace(quote, '\"')

		return line

	def _getUsername(self, line: str) -> str:
		
		username: str = None
		
		if line[self.LINE_USERNAME_INDEX:].count(':') > 0: 
			username = line[self.LINE_USERNAME_INDEX:].split(':')[0].strip()

		if username is None or len(username.strip()) == 0:
			raise NameError("No username found")

		return username

	def _getContents(self, line: str, username: str) -> str:
		
		content: str - None

		return line[self.LINE_USERNAME_INDEX:].replace(username+":", "").strip()

	def __str__(self):
		return (
				"<WhatsAppFileReader> File: {self._file}".format(self=self))
