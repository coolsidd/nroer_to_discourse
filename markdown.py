from useful_utilities import *

@debug_func
def markdown(title,content,image,license,source,authors,collection,location):
	template = """# {}

def markdown_image(
    title, content, image, license, source, authors, collection, location
):
    template = """# {}
### {}
![alt text]({})
##### *License*: {}
##### *Source*: {}
{}"""
	footnote = ""
	if len(authors)!=0:
		footnote += "##### Authors: "
		for author in authors[:-1]:
			footnote += "{}, ".format(author)
		footnote += "{}\n".format(authors[-1])
	if len(collection)!=0:
		footnote += "##### Collection: "
		for collec in collection[:-1]:
			footnote += "{}, ".format(collec)
		footnote += "{}\n".format(collection[-1]) 
	if len(location)!=0:
		footnote += "##### Location: "
		for loc in location[:-1]:
			footnote += "{}, ".format(loc)
		footnote += "{}".format(location[-1])
	return template.format(title, content, image, license, source, footnote)
