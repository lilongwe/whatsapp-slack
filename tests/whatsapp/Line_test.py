from whatsapp.Line import Line
from pytest import raises
from datetime import datetime

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

def test_createLineWithWrongTypes():

	username:int = 10
	content:int = 20
	date:str = "date"

	line:Line = Line(date, username, content)

	assert line.getDate() == None
	assert line.getContent() == None
	assert line.getUsername() == None
	assert line.hasContent() == False

def test_anyNoneParameterHasNoContent():

	username:str = "username"
	content:str = "content"
	date:datetime = datetime.now()

	line:Line = Line(None, username, content)
	assert line.hasContent() == False

	line:Line = Line(date, None, content)
	assert line.hasContent() == False

	line:Line = Line(date, username, None)
	assert line.hasContent() == False

def test_emptyStrings():

	username:str = "username"
	content:str = "content"
	date:datetime = datetime.now()

	line:Line = Line(date, "", content)
	assert line.hasContent() == False

	line:Line = Line(date, "   ", content)
	assert line.hasContent() == False

	line:Line = Line(date, username, "")
	assert line.hasContent() == False

	line:Line = Line(date, username, "\r\t   \n")
	assert line.hasContent() == False