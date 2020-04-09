from whatsapp.FileReader import FileReader
from whatsapp.Line import Line
import pathlib, hashlib
from pytest import raises
from datetime import datetime

def test_checkCreateFileReaderWithObject():

	path = str(pathlib.Path(__file__).parent.absolute())
	
	input_file = open(path + "/whatsapp.txt", "rb")

	fileReader:FileReader = FileReader(input_file)

	assert fileReader.file() == input_file, "files are not equal"

def test_checkCreateFileReaderWithString():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader(path)

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
		fileReader:FileReader = FileReader(1)

def test_checkFileNotFoundException():

	with raises(FileNotFoundError):
		fileReader:FileReader = FileReader("")

def test_readLine():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader(path)

	line:Line = fileReader.read()

	assert type(line) == Line

	line.getContent()
	count = 1
	keepReading = True

	while keepReading:
		keepReading = line.hasContent()
		line = fileReader.read()
		count += 1

	assert 19 == count

def test_checkTypesAndCountOfKeys():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader(path)

	line:Line = fileReader.read()

	assert type(line.getContent()) == str
	assert type(line.getDate()) == datetime
	assert type(line.getUsername()) == str
	
def test_outputValues():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader(path)

	line:Line = None

	for i in range(4):
		line = fileReader.read()

	assert line.getContent() == "Not bad, I’m living the \"dream\" with a really handsome man"
	assert line.getUsername() == "Elena Rosa Brunet"
	assert line.getDate().strftime(fileReader.DATE_FORMAT) == "[26/03/2020, 10:47:47]"

def test_multilineContent():
	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:FileReader = FileReader(path)

	line:Line = None

	for i in range(13):
		line = fileReader.read()

	assert line.getContent().count("\n") == 3