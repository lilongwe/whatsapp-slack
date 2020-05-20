import hashlib
import pathlib
from datetime import datetime
from io import StringIO, BytesIO
from tempfile import SpooledTemporaryFile, TemporaryFile

import pytest
from pytest import raises

from whatsapp_slack.reader.WhatsAppFileReader import WhatsAppFileReader
from whatsapp_slack.Line import Line
from whatsapp_slack.writer.CSVFileWriter import CSVFileWriter

import inspect


@pytest.fixture
def absolute_path():
	return str(pathlib.Path(__file__).parent.absolute())


@pytest.fixture
def whatsapp_file_path(absolute_path):
	return absolute_path + "/whatsapp.txt"


@pytest.fixture
def whatsapp_file(whatsapp_file_path):
	return open(whatsapp_file_path, "rb")

def test_checkCreateFileReaderWithObject(whatsapp_file):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file)

	assert fileReader.file() == whatsapp_file, "files are not equal"

def test_checkBinaryMode():

	temp = SpooledTemporaryFile(mode="w")

	with raises(Exception) as e:
		fileReader: Reader = WhatsAppFileReader(temp)

	assert WhatsAppFileReader.READ_MODE_EXCEPTION in str(e.value)

def test_checkSpooledTemporaryFile():

	temp = SpooledTemporaryFile()
	fileReader: Reader = WhatsAppFileReader(temp)

def test_checkBytesIO():

	temp = BytesIO()
	fileReader: Reader = WhatsAppFileReader(temp)

def test_checkCreateFileReaderWithString(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	input_file = open(whatsapp_file_path, "rb")

	hash_reader = hashlib.md5()
	hash_reader.update(fileReader.file().read())
	existing_file_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(input_file.read())
	input_file_hash = hash_reader.hexdigest()

	assert existing_file_hash == input_file_hash, "files are not equal"

def test_checkParameterException():

	with raises(TypeError):
		fileReader: Reader = WhatsAppFileReader(1)

def test_checkFileNotFoundException():

	with raises(FileNotFoundError):
		fileReader: Reader = WhatsAppFileReader("")

def test_readLine(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	line: Line = fileReader.read()

	assert type(line) == Line

	line.getContent()
	count = 1
	keepReading = True

	while keepReading:
		keepReading = line.hasContent()
		line = fileReader.read()
		count += 1

	assert 19 == count

def test_checkTypesAndCountOfKeys(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	line: Line = fileReader.read()

	assert type(line.getContent()) == str
	assert type(line.getDate()) == datetime
	assert type(line.getUsername()) == str

def test_close(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	line: Line = fileReader.read()

	assert line is not None

	fileReader.close()

	with raises(ValueError):
		line = fileReader.read()

def test_outputValues(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	line: Line = None

	for i in range(4):
		line = fileReader.read()

	assert line.getContent() == ("Not bad, I’m living the \"dream\" "
								"with a really handsome man")
	assert line.getUsername() == "Elena Rosa Brunet"
	assert line.getDate().strftime(fileReader.DATE_FORMAT) == (	
																"[26/03/2020,"
																" 10:47:47]")

def test_multilineContent(whatsapp_file_path):

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)

	line: Line = None

	for i in range(13):
		line = fileReader.read()

	assert line.getContent().count("\n") == 3


def test_processWithContent(absolute_path, whatsapp_file_path):
	
	csvFile = open(absolute_path + "/../utilities/slack_original.csv", "r")

	fileReader: Reader = WhatsAppFileReader(whatsapp_file_path)
	
	contents: StringIO = StringIO()

	fileWriter: Writer = CSVFileWriter(
		contents, 
		channel="test-channel", 
		delimiter="|")

	fileReader.process(fileWriter)

	hash_reader = hashlib.md5()
	hash_reader.update(csvFile.read().encode("utf-8"))
	existing_file_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(contents.getvalue().encode("utf-8"))
	output_file_hash = hash_reader.hexdigest()

	assert existing_file_hash == output_file_hash
