from io import StringIO, BytesIO

from flask import Flask, render_template, request, flash, Response
from werkzeug.datastructures import FileStorage

from whatsapp_slack.reader.WhatsAppFileReader import WhatsAppFileReader
from whatsapp_slack.writer.CSVFileWriter import CSVFileWriter

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/")
def hello() -> "html":

	return render_template(
				"entry.html",
				the_title="Welcome to whatsapp_slack on the web!",
				the_delimiter=CSVFileWriter.DEFAULT_DELIMITER,
				the_channel=CSVFileWriter.DEFAULT_CHANNEL_NAME)


@app.route("/download", methods=["GET", "POST"])
def download() -> Response:

	csv = '1,2,3\n4,5,6\n'
	csvFile = request.form["slack_file"]

	return Response(
		csvFile,
		mimetype="text/csv",
		headers={
				"Content-disposition":
				"attachment; filename=slack.csv"})


@app.route("/process", methods=["GET", "POST"])
def process() -> "html":

	fileToProcess = None
	original_file = None
	slack_file = StringIO()

	delimiter = request.form["delimiter"]
	channel = request.form["channel"]

	if "whatsapp_file" in request.files:

		file = request.files["whatsapp_file"]

		if file.filename != "":
			fileToProcess = file

	if fileToProcess is None:

		whatsapp_text = request.form["whatsapp_text"]

		if whatsapp_text != "":

			fileToProcess = BytesIO(whatsapp_text.encode("utf-8"))

	if fileToProcess is not None:
		original_file = fileToProcess.read().decode("utf-8")

		fileToProcess.seek(0, 0)

		if isinstance(fileToProcess, FileStorage):
			reader = WhatsAppFileReader(fileToProcess.stream)
		else:
			reader = WhatsAppFileReader(fileToProcess)

		writer = CSVFileWriter(slack_file, channel=channel, delimiter=delimiter)

		try:
			reader.process(writer)
		except Exception as e:
			slack_file = StringIO("ERROR: " + str(e))

	return render_template(
				"results.html",
				the_title="Welcome to whatsapp_slack on the web!",
				original_file=original_file,
				slack_file=slack_file.getvalue(),
				the_delimiter=delimiter,
				the_channel=channel)


if __name__ == "__main__":
	app.debug = True
	app.run()