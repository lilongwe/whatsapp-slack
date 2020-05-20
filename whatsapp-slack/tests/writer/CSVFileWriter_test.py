import hashlib
import pathlib
from datetime import datetime
from io import StringIO, BytesIO

import pytest
from pytest import raises

from whatsapp_slack.Line import Line
from whatsapp_slack.writer.CSVFileWriter import CSVFileWriter


@pytest.fixture
def absolute_path():
	return str(pathlib.Path(__file__).parent.absolute())


@pytest.fixture
def fixture_csv_file(absolute_path):
	return open(absolute_path + "/slack_test_fixture.csv", "rb")

def test_createFileWriter(fixture_csv_file):

	output_file = StringIO()

	fileWriter: CSVFileWriter = CSVFileWriter(
												output_file, 
												delimiter="!", 
												channel="test", 
												overrideUsername="True", 
												validator="None")

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	hash_reader = hashlib.md5()
	hash_reader.update(output_file.getvalue().encode("utf-8"))
	output_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(fixture_csv_file.read())
	fixture_hash = hash_reader.hexdigest()

	assert output_hash == fixture_hash

def test_checkTypeError():

	fileWriter1: CSVFileWriter = CSVFileWriter(StringIO())
	
	with raises(TypeError) as e:
		fileWriter2: CSVFileWriter = CSVFileWriter(BytesIO())

	assert CSVFileWriter.TYPE_ERROR_EXCEPTION in str(e.value)


@pytest.mark.xfail(
	raises=OSError, 
	reason="Uses input which cannot be used when pytest is capturing output")
def test_createFileWriterOverrideUsername(fixture_csv_file):

	output_file = StringIO()

	fileWriter: CSVFileWriter = CSVFileWriter(
		output_file, 
		delimiter="!", 
		channel="test", 
		overrideUsername=True)

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	hash_reader = hashlib.md5()
	hash_reader.update(output_file.getvalue().encode("utf-8"))
	output_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(fixture_csv_file.read())
	fixture_hash = hash_reader.hexdigest()

	assert output_hash == fixture_hash

def test_createFileWriterDefaults():

	output_file = StringIO()
	fixture_value = '1555110000, "whatsapp", "@username", "content"\n'

	fileWriter: CSVFileWriter = CSVFileWriter(output_file)

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	output_value = output_file.getvalue()

	assert output_value == fixture_value

def test_close():

	output_file = StringIO()
	fixture_value = '1555110000, "whatsapp", "@username", "content"\n'

	fileWriter: CSVFileWriter = CSVFileWriter(output_file)

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	output_value = output_file.getvalue()

	assert output_value == fixture_value

	fileWriter.close()

	with raises(ValueError):
		fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

def test_fileNotInWriteMode(fixture_csv_file):

	output_file = open(fixture_csv_file.name, "r")

	with raises(IOError):
		fileWriter: CSVFileWriter = CSVFileWriter(output_file)
