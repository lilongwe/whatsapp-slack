import abc
from io import BufferedReader

from whatsapp_slack.Line import Line
from whatsapp_slack.Base import Base
from whatsapp_slack.writer.Writer import Writer


class Reader(Base):

	@abc.abstractmethod
	def file(self) -> BufferedReader:
		pass

	@abc.abstractmethod
	def read(self) -> Line:
		pass
	
	@abc.abstractmethod
	def process(self, writer: Writer):
		pass

	@abc.abstractmethod
	def close(self):
		pass
