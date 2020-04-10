from slack.CVSFileWriter import FileWriter
from whatsapp.Line import Line
from datetime import datetime
import pathlib, hashlib
from pytest import raises
from io import StringIO


def test_createFileWriter():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = StringIO()
	fixture_file = open(path + "/slack_test_fixture.csv", "rb")

	fileWriter:FileWriter = FileWriter(output_file, delimiter="!", channel="test")

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	hash_reader = hashlib.md5()
	hash_reader.update(output_file.getvalue().encode("utf-8"))
	output_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(fixture_file.read())
	fixture_hash = hash_reader.hexdigest()

	assert output_hash == fixture_hash

def test_createFileWriterDefaults():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = StringIO()
	fixture_value = '1555110000, "whatsapp", "@username", "content"\n'

	fileWriter:FileWriter = FileWriter(output_file)

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	output_value = output_file.getvalue()

	assert output_value == fixture_value

def test_fileNotInWriteMode():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = open(path + "/slack_test_fixture.csv", "r")

	with raises(IOError):
		fileWriter:FileWriter = FileWriter(output_file)