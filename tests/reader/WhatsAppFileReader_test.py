from reader.WhatsAppFileReader import WhatsAppFileReader
from writer.CSVFileWriter import CSVFileWriter
from utilities.Line import Line
import pathlib, hashlib
from pytest import raises
from datetime import datetime
from io import StringIO

def test_checkCreateFileReaderWithObject():

	path = str(pathlib.Path(__file__).parent.absolute())
	
	input_file = open(path + "/whatsapp.txt", "rb")

	fileReader:WhatsAppFileReader = WhatsAppFileReader(input_file)

	assert fileReader.file() == input_file, "files are not equal"

def test_checkCreateFileReaderWithString():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:WhatsAppFileReader = WhatsAppFileReader(path)

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
		fileReader:WhatsAppFileReader = WhatsAppFileReader(1)

def test_checkFileNotFoundException():

	with raises(FileNotFoundError):
		fileReader:WhatsAppFileReader = WhatsAppFileReader("")

def test_readLine():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:WhatsAppFileReader = WhatsAppFileReader(path)

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

	fileReader:WhatsAppFileReader = WhatsAppFileReader(path)

	line:Line = fileReader.read()

	assert type(line.getContent()) == str
	assert type(line.getDate()) == datetime
	assert type(line.getUsername()) == str
	
def test_outputValues():

	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:WhatsAppFileReader = WhatsAppFileReader(path)

	line:Line = None

	for i in range(4):
		line = fileReader.read()

	assert line.getContent() == "Not bad, I’m living the \"dream\" with a really handsome man"
	assert line.getUsername() == "Elena Rosa Brunet"
	assert line.getDate().strftime(fileReader.DATE_FORMAT) == "[26/03/2020, 10:47:47]"

def test_multilineContent():
	path = str(pathlib.Path(__file__).parent.absolute()) + "/whatsapp.txt"

	fileReader:WhatsAppFileReader = WhatsAppFileReader(path)

	line:Line = None

	for i in range(13):
		line = fileReader.read()

	assert line.getContent().count("\n") == 3

def test_processWithContent():

	path = str(pathlib.Path(__file__).parent.absolute())
	
	whatsappFilePath = path + "/whatsapp.txt"
	csvFile = open(path + "/../utilities/slack_original.csv", "r")

	fileReader:WhatsAppFileReader = WhatsAppFileReader(whatsappFilePath)
	
	contents:StringIO = StringIO()

	fileWriter:CSVFileWriter = CSVFileWriter(contents, channel="test-channel", delimiter="|")

	fileReader.process(fileWriter)

	hash_reader = hashlib.md5()
	hash_reader.update(csvFile.read().encode("utf-8"))
	existing_file_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(contents.getvalue().encode("utf-8"))
	output_file_hash = hash_reader.hexdigest()

	assert existing_file_hash == output_file_hash