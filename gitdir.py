import requests
import re
import os
import urllib.request
import sys
import signal
import argparse

# this ansii code lets us erase the current line
ERASE_LINE = '\x1b[2K'


def create_url(url):
	"""
	modifying the given url so that it returns JSON data when
	we do a GET requests later in this script
	"""
	
	api_url = url.replace("https://github.com", "https://api.github.com/repos")

	# extract the branch name from the given url (e.g master)
	branch = re.findall(r"\/tree\/(.*?)\/", api_url)[0]

	api_url = re.sub(r"\/tree\/.*?\/", "/contents/", api_url)
		
	api_url = api_url+"?ref="+branch

	return api_url


def main():
    # disbale CTRL+Z
	signal.signal(signal.SIGTSTP, signal.SIG_IGN)

	parser = argparse.ArgumentParser(description = "Download directories/folders from GitHub")
	parser.add_argument('url', action="store")

	args = parser.parse_args()

	repo_url = args.url

	download_dir = repo_url.split("/")[-1]

	# generate the url which returns the JSON data
	api_url = create_url(repo_url)

	r = requests.get(api_url)
	data = r.json()

	# make a directory with the name which is taken from the 
	# actual repo
	os.makedirs(download_dir, exist_ok=True)

	# getting the total number of files so that we
	# can use it for the output information later
	total_files = len(data)

	for index, file in enumerate(data):
		file_url = file["download_url"]
		fname = file["name"]
		path = file["path"]
		
		try:
			# download the file
			urllib.request.urlretrieve(file_url, path)

			# bring the cursor to the beginning, erase the current line, and dont make a new line
			print('\r'+ERASE_LINE, end='')
			print("\033[1;92m▶ Downloaded {}/{}: \033[0m{}".format(index+1, total_files, fname), end="", flush=True)
		
		except KeyboardInterrupt:
		    # when CTRL+C is pressed during the execution of this script,
			# bring the cursor to the beginning, erase the current line, and dont make a new line
			print('\r'+ERASE_LINE, end='')
			print("\033[1;94mExiting...\033[0m")
			exit()
	
	print('\r'+ERASE_LINE, end='')
	print("\033[1;92m✔ Finished downloading {} file(s)\033[0m".format(total_files))


if __name__=="__main__":
	main()
