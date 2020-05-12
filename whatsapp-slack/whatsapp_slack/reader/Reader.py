import abc
from io import BufferedReader

from whatsapp_slack.Line import Line
from whatsapp_slack.writer.Writer import Writer


class Reader(abc.ABC):

	@abc.abstractmethod
	def file(self) -> BufferedReader:
		pass

	@abc.abstractmethod
	def read(self) -> Line:
		pass
	
	@abc.abstractmethod
	def process(self, writer: Writer):
		pass
