import urllib2
import optparse
import os
import Queue
import threading

parser = optparse.OptionParser("usage <prog> -t <target>")
parser.add_option('-t', dest='target', type='string', \
		help='Specify Target')
(options, args) = parser.parse_args()

target = options.target
if target == None:
	print parser.usage
	exit(0)

filters = [".jpg", ".gif", ".png", ".css"]
directory = "./wordpress"
os.chdir(directory)

web_paths = Queue.Queue()

for r,d,f in os.walk("."):
	for fil in f:
		remote_path = "%s/%s" % (r, fil)
		if remote_path.startswith("."):
			remote_path = remote_path[1:]
		if os.path.splitext(fil)[1] not in filters:
			web_paths.put(remote_path)

def test_remote():
	while not web_paths.empty():
		path = web_paths.get()
		url = "%s%s" % (target,path)
		request = urllib2.Request(url)
		try:
			response = urllib2.urlopen(request)
			content = response.read()
			print "[%d] => %s" % (response.code, path)
			response.close()
		except urllib2.HTTPError as error:
			if error.code != 404:
				print "Failed [%s] => %s" % (error.code, path)
			pass

for i in range(10):
	print "Spawning thread: %d" % i
	t = threading.Thread(target=test_remote)
	t.start()
