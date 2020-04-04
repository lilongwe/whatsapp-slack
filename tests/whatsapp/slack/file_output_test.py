from whatsapp.slack.csv import generateFile, closeFiles
import pathlib, hashlib


def test_generateFile():

    path = str(pathlib.Path(__file__).parent.absolute())

    input_file = open(path + "/../whatsapp.txt", "r")
    output_file = open(path + "/slack.csv", "r+")
    original_file = open(path + "/slack_original.csv", "r")

    generateFile(input_file, output_file, "|", "test-channel", False)

    output_hash = hashlib.md5(output_file.read().encode('utf-8')).hexdigest()
    original_hash = hashlib.md5(original_file.read().encode('utf-8')).hexdigest()

    input_file.close()
    output_file.close()
    original_file.close()

    assert output_hash == original_hash

def test_closeFiles():

    path = str(pathlib.Path(__file__).parent.absolute())

    input_file = open(path + "/../whatsapp.txt", "r")
    output_file = open(path + "/slack.csv", "r+")
    original_file = open(path + "/slack_original.csv", "r")

    closeFiles({input_file,output_file,original_file})

    assert input_file.closed == output_file.closed == original_file.closed