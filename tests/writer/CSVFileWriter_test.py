from writer.CSVFileWriter import CSVFileWriter
from reader.Line import Line
from datetime import datetime
import pathlib, hashlib
from pytest import raises
from io import StringIO
import pytest


def test_createFileWriter():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = StringIO()
	fixture_file = open(path + "/slack_test_fixture.csv", "rb")

	fileWriter:CSVFileWriter = CSVFileWriter(output_file, delimiter="!", channel="test", overrideUsername="True")

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	hash_reader = hashlib.md5()
	hash_reader.update(output_file.getvalue().encode("utf-8"))
	output_hash = hash_reader.hexdigest()

	hash_reader = hashlib.md5()
	hash_reader.update(fixture_file.read())
	fixture_hash = hash_reader.hexdigest()

	assert output_hash == fixture_hash

@pytest.mark.xfail(raises=OSError,reason="Uses input which cannot be used when pytest is capturing output")
def test_createFileWriterOverrideUsername():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = StringIO()
	fixture_file = open(path + "/slack_test_fixture.csv", "rb")

	fileWriter:CSVFileWriter = CSVFileWriter(output_file, delimiter="!", channel="test", overrideUsername=True)

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

	fileWriter:CSVFileWriter = CSVFileWriter(output_file)

	fileWriter.write(Line(datetime(2019, 4, 13), "username", "content"))

	output_value = output_file.getvalue()

	assert output_value == fixture_value

def test_fileNotInWriteMode():

	path = str(pathlib.Path(__file__).parent.absolute())

	output_file = open(path + "/slack_test_fixture.csv", "r")

	with raises(IOError):
		fileWriter:CSVFileWriter = CSVFileWriter(output_file)