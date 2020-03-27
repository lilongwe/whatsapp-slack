from whatsapp.slack.csv import generateFile
import hashlib
import pathlib


def test_generateFile():
    print("hello")
    path = str(pathlib.Path(__file__).parent.absolute())

    input_file = open(path + "/whatsapp.txt", "r")
    output_file = open(path + "/slack.csv", "r+")
    original_file = open(path + "/slack_original.csv", "r")

    generateFile(input_file, output_file, "|", "test-channel", False)

    output_hash = hashlib.md5(output_file.read().encode('utf-8')).hexdigest()
    original_hash = hashlib.md5(original_file.read().encode('utf-8')).hexdigest()

    assert output_hash == original_hash

