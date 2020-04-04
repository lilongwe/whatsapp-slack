from io import IOBase
from typing import TextIO

class FileReader:

	def __init__(self, fileHandle):

		if isinstance(fileHandle, IOBase):
			self._file:TextIO = fileHandle
		elif isinstance(fileHandle, str):
			self._file:TextIO = open(fileHandle, "r")


	def file(self) -> TextIO:
		return self._file
