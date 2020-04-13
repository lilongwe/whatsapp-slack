import abc
from utilities.Line import Line
from writer.Writer import Writer

class Reader(abc.ABC):

	@abc.abstractmethod
	def read(self) -> Line:
		pass
	
	@abc.abstractmethod
	def process(self, writer:Writer):
		pass