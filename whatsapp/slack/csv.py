#!/usr/bin/env python3

import os
import sys
import argparse
import datetime

from typing import TextIO

# Static variables
console_prefix = "$ "
format_string = '{1}{0} "{2}"{0} "@{3}"{0} "{4}"'


def main():
	channel_name = "#whatsapp"
	description = "Transform exported whatsapp discussions into ready-for-import slack.com threads."
	delimiter = ","

	# Format for writting slack csv file
	
	parser = argparse.ArgumentParser(description=description)
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

	input_file = args.input
	output_file = open("Slack Import "+args.input.name, 'w') if args.output is None else args.output
	
	print("{0}input filename:     '{1}'".format(console_prefix, input_file.name))
	print("{0}output filename:    '{1}'".format(console_prefix, output_file.name))
	print("{0}slack channel name: '{1}'".format(console_prefix, channel_name))
	print("{0}delimiter: '{1}'".format(console_prefix, delimiter))
	print("{0}usernames: '{1}'".format(console_prefix, args.username))

	generateFile(input_file, output_file, delimiter, channel_name, args.username)
	
	print("\n  🌖 {0}Done. Enjoy!\n".format(console_prefix))



def generateFile(input_file: TextIO, output_file: TextIO, delimiter: str, channel_name: str, change_username: bool):

	print("{0}Reading input file...".format(console_prefix))
	input_lines = input_file.readlines()
	usernames_mapping = {}
	
	# Looping through raw lines to group combine lines
	output_line = None
	output_elements = {}
	my_line_number = 0
    
	with open(output_file.name, 'w') as outfile:	
	
		for line in input_lines:

			my_line_number += 1

			print("Line Number: " , my_line_number)

			try:
				dt = datetime.datetime.strptime(line[:22].strip(), "[%d/%m/%Y, %H:%M:%S]")
			except ValueError:
				# We cannot find a date, it's a continuation of a line, most probably...
				output_elements["content"] += "\n"+line.strip()
			else:
				if output_elements.get("content", None) is not None:
					new_line = format_string.format(delimiter, int(output_elements["date"].timestamp()), channel_name, output_elements["username"], output_elements["content"])
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
					input_username = line[23:].split(':')[0].strip()
					if input_username not in usernames_mapping.keys():

						output_username = ""

						if change_username:
							output_username = input("\n{0}Unknown username '{1}'. Enter corresponding Slack.com username (<Enter>=identical): ".format(console_prefix, input_username))

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
			new_line = format_string.format(delimiter, int(output_elements["date"].timestamp()), channel_name, output_elements["username"], output_elements["content"])
			print(new_line)
			outfile.write(new_line+"\n")
			output_elements = {}

if __name__ == "__main__":
	main()
