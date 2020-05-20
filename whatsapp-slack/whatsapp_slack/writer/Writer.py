import abc

from whatsapp_slack.Base import Base
from whatsapp_slack.Line import Line


class Writer(Base):

	@abc.abstractmethod
	def write(self, line: Line):
		pass

	@abc.abstractmethod
	def setOverrideUsername(self, override: bool):
		pass
	
	@abc.abstractmethod
	def close(self):
		pass