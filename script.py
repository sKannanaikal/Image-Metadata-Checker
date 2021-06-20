import optparse
import urlib2
from bs4 import BeautifulSoup
from urlparse import urlsplit
from os.path import basename
from PIL import Image

NUMOFIMAGES = 0

def locateImages(url):
	print('[+] Searching {website} for all images'.format(website=url))
	
	website = urlib2.urlopen(url).read()
	soup = BeautifulSoup(website)
	images = soup.findAll('img')

	return images

def downloadImage(image):
	try:
		source = image['src']
		imageContent = urlib2.urlopen(source).read()
		NUMOFIMAGES += 1
		imageName = basename(urlsplit(source)[2])
		localCopy = open(imageName, 'wb')
		localCopy.write(imageContent)
		localCopy.close()
		return imageName
	
	except:
		return None

def checkForMetaData(imageName):
	try:
		image = Image.open(imageName)
		metadata = image._getexif()
		if metadata:
			for (tag, value) in metadata:
				print("[+] {title} : {item}".format(title=tag, item=value))
		else:
			print("[-] File Does Not Have Any Metadata Available")
	except:
		return None


def main():
	command = optparse.OptionParser('usage%prog -u <target url>')
	command.add_option('-u', dest='target', type='string', help='specify the target url you want to download from')
	
	url = command.target
	
	images = locateImages(url)

	for image in images:
		imageName = downloadImage(image)
		checkForMetaData(imageName)

	print('[+] A total of {count} images were found on {website}! They have all been reviewed for inclusion of metadata!'.format(count=NUMOFIMAGES, website=url))


if __name__ == "__main__":
	main()