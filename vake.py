import sys, os
import subprocess
import re
import select

"""
Runs an instance of make, echoing the stdout and storing the stderr
line by line.
"""
def run_make(args):
	p = subprocess.Popen(["make"] + args,
	    stdout = subprocess.PIPE, stderr = subprocess.PIPE)

	stderr = []
	while p.poll() == None:
	    reads = [p.stdout.fileno(), p.stderr.fileno()]
	    ret = select.select(reads, [], [])

	    for fd in ret[0]:
	        if fd == p.stdout.fileno():
	            read = p.stdout.readline()
	            sys.stdout.write(read)
	        if fd == p.stderr.fileno():
	            read = p.stderr.readline()
	            sys.stderr.write(read)
	            stderr.append(read)

	return stderr

"""
Parse the output of a Make instance.
"""
def parse_output(stderr):
	parsed_output = []

	for line in stderr:
		# Regex to extract file, line, column number and error message
		m = re.search(r"(.*?):([0-9]+):([0-9]+):\s(error|warning):\s(.*)", line)
		if m:
			parsed_output.append(m.groups())

	return parsed_output

"""
Get the nth line of a file.
"""
def get_nth_line(file_name, n):
	with open(file_name) as f:
		for i, line in enumerate(f):
		    if i == n - 1:
		        return line

if __name__ == "__main__":
	VAKE_HEADER = '\033[41m'
	ENDC = '\033[0m'

	parsed_output = parse_output(run_make(sys.argv[1:]))
	if len(parsed_output) > 0:
		# Give the user a choice of running vake or not
		choice = raw_input(VAKE_HEADER + 'vake: ' + str(len(parsed_output)) + ' errors or warnings. Run vake? [Y/n]' + ENDC + ' ')
		if (choice == "" or choice.lower() == 'y'):
			# Print the instructions
			print "<Enter> to edit. 'q' to skip."

			for output in parsed_output:
				# Print out the error message
				file_name, line_no, col_no, errwarn, msg = output
				print "{0}:{1}:{2} {3}".format(file_name, line_no, col_no, errwarn) + ':', msg
				print '   ', get_nth_line(file_name, int(line_no)),
				print '  ', ' ' * (int(col_no) - 1), '^'

				cmd = raw_input(":")
				subprocess.call(['vim', file_name,
					'+call cursor({0}, {1})'.format(line_no, col_no), '+{0}'.format(cmd)])