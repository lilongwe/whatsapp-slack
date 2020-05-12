from setuptools import setup, find_packages

from whatsapp_slack import __version__, __github__, __author__


setup(
		name='whatsapp_slack', 
		version=str(__version__),
		description='Convert WhatsApp messages to Slack format',
		author=str(__author__), 
		url=str(__github__),
		packages=find_packages(),
		license='OSI Approved :: MIT License',
		classifiers=[
			"Development Status :: 5 - Production/Stable",
			"Environment :: Console",
			"Intended Audience :: System Administrators",
			"Intended Audience :: Science/Research",
			"Natural Language :: English",
			"Operating System :: POSIX",
			"Programming Language :: Python"
			])