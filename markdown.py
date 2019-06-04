from useful_utilities import *


def markdown_video(
    title,
    content,
    video_link,
    license,
    source,
    authors,
    collection,
    location,
    annotations,
):
    template = """# {}
### {}
{}
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
    if len(annotations) != 0:
        footnote += "##### Annotation: "
        for ano in annotations[:-1]:
            footnote += "{}, ".format(ano)
        footnote += "{}".format(annotations[-1])
    return template.format(title, content, video_link, license, source, footnote)


def markdown_image(
    title, content, image, license, source, authors, collection, location, annotations
):
    template = """# {}
### {}
{}
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
    if len(annotations) != 0:
        footnote += "##### Annotation: "
        for ano in annotations[:-1]:
            footnote += "{}, ".format(ano)
        footnote += "{}".format(annotations[-1])
    return template.format(title, content, image, license, source, footnote)
