from datetime import datetime

import pytest
from pytest import raises

from utilities.Line import Line


def test_createLine():

	username:str = "username"
	content:str = "content"
	date:datetime = datetime.now()

	line:Line = Line(date, username, content)

	assert line.getDate() == date
	assert line.getContent() == content
	assert line.getUsername() == username
	assert line.hasContent() == True

def test_createNoneLine():

	username:str = None
	content:str = None
	date:datetime = None

	line:Line = Line(date, username, content)

	assert line.getDate() == None
	assert line.getContent() == None
	assert line.getUsername() == None
	assert line.hasContent() == False

def test_createLineWithNoParameters():

	line:Line = Line()

	assert line.getDate() == None
	assert line.getContent() == None
	assert line.getUsername() == None
	assert line.hasContent() == False

def test_createLineWithWrongTypes():

	username:int = 10
	content:int = 20
	date:str = "date"

	line:Line = Line(date, username, content)

	assert line.getDate() == None
	assert line.getContent() == None
	assert line.getUsername() == None
	assert line.hasContent() == False


@pytest.mark.parametrize("date,username,content", 
							[(None, "username", "content"), 
							(datetime.now(), None, "content"), 
							(datetime.now(), "username" , None)])
def test_anyNoneParameterHasNoContent(date, username, content):

	line:Line = Line(date, username, content)
	assert line.hasContent() == False

@pytest.mark.parametrize("date,username,content", 
							[(datetime.now(), "", "content"), 
							(datetime.now(), "     ", "content"), 
							(datetime.now(), "username" , ""),
							(datetime.now(), "username" , "\r\t   \n")])
def test_emptyStrings(date, username, content):

	line:Line = Line(date, username, content)
	assert line.hasContent() == False
