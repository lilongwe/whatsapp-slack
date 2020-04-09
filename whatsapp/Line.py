from datetime import datetime
from typing import Union, Dict

class Line(object):

	def __init__(self, date:datetime=None, username:str=None, content:str=None):
		self._date = date if type(date) == datetime else None
		self._username = username if (username is not None 
										and type(username) == str
										and len(username) > 0) else None
		self._content = content if (content is not None 
										and type(content) == str
										and len(content) > 0) else None

	def getDate(self) -> datetime:
		return self._date

	def getContent(self) -> str:
		return self._content

	def getUsername(self) -> str:
		return self._username

	def hasContent(self) -> bool:
		return (self._content is not None 
				and self._date is not None
				and self._username is not None)