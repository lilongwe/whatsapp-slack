from datetime import datetime

class Line(object):

	def __init__(
					self, 
					date: datetime = None, 
					username: str = None, 
					content: str = None):

		if (type(date) == datetime):
			self._date = date
		else:
			self._date = None

		if (
			username is not None 
			and type(username) == str 
			and len(username.strip()) > 0):
			
			self._username = username
		else:
			self._username = None

		if (
			content is not None 
			and type(content) == str 
			and len(content.strip()) > 0):

			self._content = content
		else:
			self._content = None

	def getDate(self) -> datetime:
		return self._date

	def getContent(self) -> str:
		return self._content

	def getUsername(self) -> str:
		return self._username

	def hasContent(self) -> bool:
		return (
				self._content is not None 
				and self._date is not None
				and self._username is not None)

	def __str__(self):
		return '<Line> Date: {self._date} , Content: {self._content}, Username: {self._username}'.format(self=self)