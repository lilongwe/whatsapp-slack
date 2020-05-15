import abc


class Base(abc.ABC):

	def fullName(self):
		return self.__module__ + "." + self.__class__.__name__
