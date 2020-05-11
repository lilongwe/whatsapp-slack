from datetime import datetime

import pytest
from pytest import raises

from utilities.Line import Line


def test_createLine():

	username: str = "username"
	content: str = "content"
	date: datetime = datetime.now()

	line: Line = Line(date, username, content)

	assert line.getDate() == date
	assert line.getContent() == content
	assert line.getUsername() == username
	assert line.hasContent() is True

def test_createNoneLine():

	username: str = None
	content: str = None
	date: datetime = None

	line: Line = Line(date, username, content)

	assert line.getDate() is None
	assert line.getContent() is None
	assert line.getUsername() is None
	assert line.hasContent() is False

def test_createLineWithNoParameters():

	line: Line = Line()

	assert line.getDate() is None
	assert line.getContent() is None
	assert line.getUsername() is None
	assert line.hasContent() is False

def test_createLineWithWrongTypes():

	username: int = 10
	content: int = 20
	date: str = "date"

	line: Line = Line(date, username, content)

	assert line.getDate() is None
	assert line.getContent() is None
	assert line.getUsername() is None
	assert line.hasContent() is False


@pytest.mark.parametrize(
						"date,username,content",
						[
							(None, "username", "content"),
							(datetime.now(), None, "content"),
							(datetime.now(), "username", None)
						])
def test_anyNoneParameterHasNoContent(date, username, content):

	line: Line = Line(date, username, content)
	assert line.hasContent() is False


@pytest.mark.parametrize(
						"date,username,content",
						[
							(datetime.now(), "", "content"), 
							(datetime.now(), "     ", "content"), 
							(datetime.now(), "username", ""),
							(datetime.now(), "username", "\r\t   \n")
						])
def test_emptyStrings(date, username, content):

	line: Line = Line(date, username, content)
	assert line.hasContent() is False
