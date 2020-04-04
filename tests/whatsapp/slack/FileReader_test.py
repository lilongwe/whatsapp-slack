import whatsapp.slack.FileReader

def test_checkFile():

	path = str(pathlib.Path(__file__).parent.absolute())

    input_file = open(path + "/whatsapp.txt", "r")

	fileReader:FileReader = new FileReader(input_file)

	assert fileReader.file() == input_file
