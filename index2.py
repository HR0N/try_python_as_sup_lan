import urllib

url = "https://kbp.aero/ru/glavnaya/"
file = urllib.request.urlopen(url)

for line in file:
	decoded_line = line.decode("utf-8")
	print(decoded_line)