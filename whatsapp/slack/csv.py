#!/usr/bin/env python3

import os
import sys
import argparse
import datetime
from argparse import ArgumentParser

from typing import TextIO, Set, Dict, Union

# Static variables
CONSOLE_PREFIX:str = "$ "
FORMAT_STRING:str = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'
DATE_FORMAT:str = "[%d/%m/%Y, %H:%M:%S]"


def main():
	channel_name:str = "#whatsapp"
	description:str = "Transform exported whatsapp discussions into ready-for-import slack.com threads as a csv file."
	delimiter:str = ","

	# Format for writting slack csv file
	
	parser:ArgumentParser = argparse.ArgumentParser(description=description)
	parser.add_argument("input", type=argparse.FileType('r'), help="Input filename")
	parser.add_argument("-c", "--channel", default=channel_name, help="Slack.com channel name, default: "+channel_name)
	parser.add_argument("-d", "--delimiter", default=delimiter, help="CVS delimiter, default: '"+ delimiter + "'")
	parser.add_argument("-o", "--output", type=argparse.FileType('w'), help="Output filename")
	parser.add_argument("-u", "--username", action="store_true", help="Modify usernames, default: 'FALSE'")
	# parser.print_help()
	
	args = parser.parse_args()

	# Assign arguments to variables
	channel_name = args.channel
	delimiter = args.delimiter
	
	# Print description in case of parse success
	print("\n 🚀  {0}: {1}\n".format(os.path.basename(sys.argv[0]), description))

	input_file:TextIO = args.input
	output_file:TextIO = open("Slack Import "+args.input.name, 'w') if args.output is None else args.output
	
	print("{0}input filename:     '{1}'".format(CONSOLE_PREFIX, input_file.name))
	print("{0}output filename:    '{1}'".format(CONSOLE_PREFIX, output_file.name))
	print("{0}slack channel name: '{1}'".format(CONSOLE_PREFIX, channel_name))
	print("{0}delimiter: '{1}'".format(CONSOLE_PREFIX, delimiter))
	print("{0}usernames: '{1}'".format(CONSOLE_PREFIX, args.username))

	generateFile(input_file, output_file, delimiter, channel_name, args.username)
	
	print("\n  🌖 {0}Done. Enjoy!\n".format(CONSOLE_PREFIX))

	closeFiles({input_file,output_file})


def closeFiles(allFiles: Set[TextIO]):
	for aFile in allFiles:
		aFile.close()


def generateFile(input_file: TextIO, output_file: TextIO, delimiter: str, channel_name: str, change_username: bool):

	print("{0}Reading input file...".format(CONSOLE_PREFIX))
	input_lines:list = input_file.readlines()
	usernames_mapping:Dict[str,str] = {}
	
	# Looping through raw lines to group combine lines
	output_line:str = None
	output_elements:Dict[str,Union[str,datetime]] = {}
	my_line_number:int = 0
    
	with open(output_file.name, 'w') as outfile:	
	
		for line in input_lines:

			my_line_number += 1

			print("Line Number: " , my_line_number)

			try:
				dt = datetime.datetime.strptime(line[:22].strip(), DATE_FORMAT)
			except ValueError:
				# We cannot find a date, it's a continuation of a line, most probably...
				output_elements["content"] += "\n"+line.strip()
			else:
				if output_elements.get("content", None) is not None:
					new_line:str = FORMAT_STRING.format(delimiter, int(output_elements["date"].timestamp()), channel_name, output_elements["username"], output_elements["content"])
					print(new_line)
					outfile.write(new_line+"\n")
					output_elements = {}
	
				# We can find a date at start of line, it's a new line
				output_line = line.strip()
				output_elements["date"] = dt
				
				# Make sure to change all double quotes to standard ones
				for quote in ['"', '‟', '″', '˝', '“']:
					output_line = output_line.replace(quote, '\"')

				# Oh, by the way, look for a username. The presence of a username followed by a colon is the only fkag we can use.
				if line[23:].count(':') > 0: 
					input_username:str = line[23:].split(':')[0].strip()
					if input_username not in usernames_mapping.keys():

						output_username:str = ""

						if change_username:
							output_username = input("\n{0}Unknown username '{1}'. Enter corresponding Slack.com username (<Enter>=identical): ".format(CONSOLE_PREFIX, input_username))

						if len(output_username.strip()) > 0:
							usernames_mapping[input_username] = output_username.strip()
						else:
							usernames_mapping[input_username] = input_username
					
					output_username = usernames_mapping.get(input_username, None)
					if output_username is not None:
						output_elements["username"] = output_username
						output_elements["content"] = line[23:].replace(input_username+":", "").strip()					

		# We need this to get the last line...			
		if output_elements.get("content", None) is not None:
			new_line:str = FORMAT_STRING.format(delimiter, int(output_elements["date"].timestamp()), channel_name, output_elements["username"], output_elements["content"])
			print(new_line)
			outfile.write(new_line+"\n")
			output_elements = {}

if __name__ == "__main__":
	main()
