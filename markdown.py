from useful_utilities import *


def markdown_video(
    title,
    content,
    thumbnail,
    video_link,
    license,
    source,
    authors,
    collection,
    location,
):
    template = """# {}
### {}
<a href="{}" target="_blank"><img src="{}" alt="Video" width="240" height="180" border="10" /></a>
##### *License*: {}
##### *Source*: {}
{}"""
    footnote = ""
    if len(authors) != 0:
        footnote += "##### Authors: "
        for author in authors[:-1]:
            footnote += "{}, ".format(author)
        footnote += "{}\n".format(authors[-1])
    if len(collection) != 0:
        footnote += "##### Collection: "
        for collec in collection[:-1]:
            footnote += "{}, ".format(collec)
        footnote += "{}\n".format(collection[-1])
    if len(location) != 0:
        footnote += "##### Location: "
        for loc in location[:-1]:
            footnote += "{}, ".format(loc)
        footnote += "{}".format(location[-1])
    return template.format(
        title, content, video_link, thumbnail, license, source, footnote
    )


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
    if len(authors) != 0:
        footnote += "##### Authors: "
        for author in authors[:-1]:
            footnote += "{}, ".format(author)
        footnote += "{}\n".format(authors[-1])
    if len(collection) != 0:
        footnote += "##### Collection: "
        for collec in collection[:-1]:
            footnote += "{}, ".format(collec)
        footnote += "{}\n".format(collection[-1])
    if len(location) != 0:
        footnote += "##### Location: "
        for loc in location[:-1]:
            footnote += "{}, ".format(loc)
        footnote += "{}".format(location[-1])
    return template.format(title, content, image, license, source, footnote)
