from whatsapp import FileReader
import pathlib, hashlib
from pytest import raises
from typing import Union, Dict
from datetime import datetime

def test_checkCreateFileReaderWithObject():

	path = str(pathlib.Path(__file__).parent.absolute())
	
	input_file = open(path + "/whatsapp.txt", "rb")

	fileReader:FileReader = FileReader.FileReader(input_file)

	assert fileReader.file() == input_file, "files are not equal"

def test_checkCreateFileReaderWithString():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader.FileReader(path)

	input_file = open(path, "rb")

	hash_reader = hashlib.md5()
	hash_reader.update(fileReader.file().read())
	existing_file_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(input_file.read())
	input_file_hash = hash_reader.hexdigest()

	assert existing_file_hash == input_file_hash, "files are not equal"

def test_checkParameterException():

	with raises(TypeError):
		fileReader:FileReader = FileReader.FileReader(1)

def test_checkFileNotFoundException():

	with raises(FileNotFoundError):
		fileReader:FileReader = FileReader.FileReader("")

def test_readLine():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader.FileReader(path)

	line = fileReader.read()
	count = 1
	keepReading = True

	while keepReading:
		keepReading = bool(line)
		line = fileReader.read()
		count += 1

	assert 19 == count

def test_checkTypesAndCountOfKeys():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader.FileReader(path)

	line:Dict[str,Union[str,datetime]] = fileReader.read()

	assert type(line[fileReader.CONTENT]) == str
	assert type(line[fileReader.DATE]) == datetime
	assert type(line[fileReader.USERNAME]) == str
	
	assert len(line.keys()) == 3

def test_outputValues():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader.FileReader(path)

	line:Dict[str,Union[str,datetime]] = None

	for i in range(4):
		line = fileReader.read()

	assert line[fileReader.CONTENT] == "Not bad, I’m living the \"dream\" with a really handsome man"
	assert line[fileReader.USERNAME] == "Elena Rosa Brunet"
	assert line[fileReader.DATE].strftime(fileReader.DATE_FORMAT) == "[26/03/2020, 10:47:47]"

def test_multilineContent():
	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader.FileReader(path)

	line:Dict[str,Union[str,datetime]] = None

	for i in range(13):
		line = fileReader.read()

	assert line[fileReader.CONTENT].count("\n") == 3