import abc
from utilities.Line import Line

class Writer(abc.ABC):

	@abc.abstractmethod
	def write(self, line:Line):
		pass

	@abc.abstractmethod
	def setOverrideUsername(self, override:bool):
		pass