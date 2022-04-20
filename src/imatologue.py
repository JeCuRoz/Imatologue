'''
This script creates a PDF catalog from a list of images.
Allowed image formats are JPG, PNG and GIF.
The list of images can be provided as a text file, with each line representing the path to an image, 
or it can be obtained by browsing a folder (perhaps recursively) for the images contained in the folder.
Each image can have a text associated with it. In addition, there are multiple options for PDF creation: 
paper formats, paper orientation, headers and footers, .....
More information by running the script with the -h parameter and in the comments.
'''

import os
import os.path

from reportlab.pdfgen import canvas
from reportlab.lib.utils import Image
from reportlab.lib.pagesizes import landscape

from defaults import defaultFontName, defaultFontSize, newLine, textMargin, AUTHOR, CREATOR, headerFlag, now, \
    nameSeparator, wordSeparator, imageFileExtensions, fieldSeparator, commentChar, defaultName, defaultExtension, \
    unit, pages, dumpExtension

from cliparser import parseArgs
from page import Page


# draws the image in the cell
def drawCell(
        pdfCanvas, cellIndex, cellData, page,
        cellBorder=True, cellTitle=True, fontName=defaultFontName, fontSize=defaultFontSize
):

    pdfCanvas.saveState()  # save the initial context

    # font settings
    pdfCanvas.setFont(fontName, fontSize)
    
    # We move the origin of coordinates to coincide with the lower left corner of the cell
    # This is just a convenience to simplify the calculations
    xOrigin, yOrigin = page.cellCoords(cellIndex)
    pdfCanvas.translate(xOrigin, yOrigin)
    
    # width and height of the cell
    width = page.cellWidth
    height = page.cellHeight

    textHeight = fontSize  # height of the font
    textY = height - textHeight  # vertical position of the first line of text in the image

    # internal cell dimensions without margins
    internalWidth = page.cellInternalWidth
    # using the smallest one to avoid overlapping, at least in the first line
    internalHeight = min(page.cellInternalHeight, textY)

    # cellData is a tuple
    # first field is the header text of the image
    # the second one is the path of the image
    imageText, imagePath = cellData

    # get the image size
    with Image.open(imagePath) as image:
        imageWidth, imageHeight = image.size

    # scale the image while maintaining the aspect ratio to fit within the inner area of the cell
    factor = min(internalWidth / imageWidth, internalHeight / imageHeight)  # factor de escalado
    imageNewWidth = imageWidth * factor
    imageNewHeight = imageHeight * factor

    # draws the scaled image inside the cell
    # centered horizontally and separated by the lower margin from the lower end of the cell
    pdfCanvas.drawImage(
        imagePath,
        (width - imageNewWidth) // 2,
        page.cellBottom,
        imageNewWidth,
        imageNewHeight
    )

    # the borders and text are above the image to avoid being covered by the image
    if cellBorder:
        # draws a frame around the cell
        pdfCanvas.rect(0, 0, width, height)

    if cellTitle:
        # put the image title on the top of the cell, horizontally centered
        halfWidth = width // 2
        textData = imageText

        # split the text in lines and write one below the other
        for line in textData.split(newLine):
            pdfCanvas.drawCentredString(halfWidth, textY, line)
            textY -= textHeight  # we lower the vertical position where the text will be written

    print("Image added: {0}".format(imagePath))
    pdfCanvas.restoreState()  # restore the initial context


# add a new page to the PDF document
# the new page will be formatted as desired: page number, background, header,....
# the first page is not added only formatted
def addNewPage(
        pdfCanvas, page, fontName, fontSize, pageNumber,
        showPageNumber=None, header=None, timeStamp=None, background=None, x=0, y=0, width=0, height=0
):
    if pageNumber > 1:
        # only need to add the second and succesives pages
        pdfCanvas.showPage()

    # set the name and size of the font
    pdfCanvas.setFont(fontName, fontSize)

    # horizontal center of the page
    center = page.pageWidth // 2

    if background:
        # add the background image to the page
        pdfCanvas.drawImage(background, x, y, width, height)

    if timeStamp:
        # write date and time in the page footer
        pdfCanvas.drawString(page.pageLeft, textMargin, timeStamp)

    if showPageNumber:
        # write the page number in the footer page
        pdfCanvas.drawString(center, textMargin, str(pageNumber))

    if header:
        # set the page header
        pdfCanvas.drawCentredString(center, page.pageHeight - textMargin - fontSize, header)


# create the catalog
def createPDF(
        images, outputPDFName, page, withBorder, withTitle, fontSize,
        fontName=defaultFontName, background=None, expand=False, header=None, withDate=False, withNumberPages=False
):

    # images: list of 2-uples
    # the first field is a text that will be the image header
    # the second one is the image path
    # Watch out! In the input file, the first field is the path and the rest the text

    # outputPDF: name of the generated PDF

    # page: page information: number of cells, margins, spacing,...

    # withBorder: add a border to each image

    # withTitle: add a text to each image

    # background: path of the background image of the pages

    # expand: background image will fit page size

    cellIndex = 0  # index of the cell within the page
    numberOfimages = 0  # number of images added to the PDF
    numberOfpages = 0  # number of pages added to the PDF
    newPage = 1  # a new page will be added if true

    # background image is optional

    # the background image is always placed in the upper left corner of the page
    # set the x coordinate of the background
    bkX = 0
 
    # adjust the size of the background image to fit the page size
    bkWidth, bkHeight = page.size

    if background and not expand:
        # there is a background image and it won't fit the page size
        # get the size of the background image
        bkImage = Image.open(background)
        bkWidth, bkHeight = bkImage.size
        bkImage.close()

    # set the y coordinate of the background
    bkY = page.pageHeight - bkHeight

    # create the initial document
    c = canvas.Canvas(outputPDFName, pagesize=page.size, pageCompression=1)

    # set author and application name
    c.setAuthor(AUTHOR)
    c.setCreator(CREATOR)
    c.setProducer(CREATOR) 

    headerText = header

    for n, image in enumerate(images):

        imageText, imagePath = image
        if n == 0 and imageText == headerFlag:
            # the first line (only the first one) can be used in the page header
            # in this case it is not an image path but a text to be used as a page header
            # this text will be used instead of the header parameter value
            headerText = imagePath
            continue

        # add a new page if necessary
        # we check this at the beginning because images is a generator and we don't know how many images it contains
        # if we check this at the end, it is possible that images is empty and a blank page has been added unnecessarily
        if newPage:
            numberOfpages += 1
            addNewPage(
                c, page, fontName, fontSize, numberOfpages,
                showPageNumber=withNumberPages,
                timeStamp=now() if withDate else None,
                background=background, x=bkX, y=bkY, width=bkWidth, height=bkHeight,
                header=headerText
            )

        # draw the current cell
        drawCell(
            c, cellIndex, image, page,
            cellBorder=withBorder, cellTitle=withTitle, fontSize=fontSize, fontName=fontName
        )
        # Increases the index of the cells inside the pages.
        # If the number of cells is exceeded create a new page
        # and resets the index
        newPage, cellIndex = divmod(cellIndex + 1, page.numCells)
        numberOfimages += 1

    # save the PDF document
    c.save()

    # give some info to the user
    print(
        f'The PDF file has been created: {outputPDFName}. {numberOfpages} page/s containing {numberOfimages} image/s'
    )


# each image has a text associated with it that can be used as the title of the image
# when creating a catalog from a folder or if a list of files is used but no text is provided
# use the filename of the image as the image text by formatting it first
# replacing the _ characters with spaces, removing redundant spaces and capitalizing the first letter of each word.
def imageTitle(imageFileName):
    baseName = os.path.basename(imageFileName.strip())  # name of the file with extension
    name, _ = os.path.splitext(baseName)  # name of the file without extension
    words = name.replace(nameSeparator, wordSeparator).split()
    return wordSeparator.join(words).title()


# check if an image can be included in the catalog
def validImage(im, excludePattern=None):

    if not os.path.isfile(im):
        # path is not a file, omit
        return False

    _, extension = os.path.splitext(im)

    if extension not in imageFileExtensions:
        # extension not allowed, omit
        return False

    if excludePattern and excludePattern in im:
        # file contains the exclusion pattern, omit
        return False

    # image is valid, will be added to the catalog
    return True


# create an iterator using a text file as input.
# each line of the file will consist of one or more fields, separated by ;
# the first field is mandatory and is the path to the image file 
# the other fields are strings that are considered to be information relative to the image and will be displayed in the catalog
# at the top of the image, each field as a line of text
# lines starting with # are ignored
def imagesFromFile(f, separator=fieldSeparator):
    with open(f) as imagesList:
        for line in imagesList:
            # lines starting with # are ignored
            if line.startswith(commentChar):
                continue
            components = line.strip().split(separator)
            # first field is the image path
            image = components.pop(0)
            # all other fields are returned as a string, replacing each ; by \n
            imageText = newLine.join(components) if components else None
            yield imageText, image


def dump(dumpFile, iterator):
    # dumpFile is a text file where we will dump the PDF images and the text associated with them
    # dumpFile could be used as an input file to generate the same PDF
    try:
        with open(dumpFile, 'w') as dumpStore:
            for imageText, image in iterator:
                yield imageText, image
                if imageText == headerFlag:
                    # the image is not a path, but a text to be used as a page header
                    # write the text without any other fields
                    dumpStore.write(image + newLine)
                else:
                    fields = [image] + imageText.split(newLine)
                    dumpStore.write(fieldSeparator.join(fields) + newLine)

        print(f'{dumpFile} has been created, containing the list of images and associated data')

    except IOError as e:
        print('An I/O error has occurred')
        raise e
    except Exception as e:
        raise e


# builds an iterator that generates the list of images to be used in the catalog
def imagesIterator(f, recursive=False, excludePattern=None):
    try:
        isDir = os.path.isdir(f)

        if isDir and recursive:
            # if f is a directory and the recursive flag is active
            # a generator will be created with all the files contained in f and its subdirectories
            iterator = (
                (None, os.path.join(path, fileName))
                for path, folders, files in os.walk(f) for fileName in sorted(files)
            )
        elif isDir:
            # if f is a directory and the recursive flag is not active
            # a generator is created with all the files contained in f
            iterator = (
                (None, os.path.join(f, fileName))
                for fileName in sorted(os.listdir(f))
            )
        elif os.path.isfile(f):
            # f is a file
            # f is a text file where each line contains the path to a file and data (text) related to it.
            iterator = imagesFromFile(f)
        else:
            # error: f is neither a file nor a directory
            raise Exception(f'{f} is neither a file nor a folder')

        for n, item in enumerate(iterator):

            imageText, image = item
            if n == 0 and not imageText and not os.path.isfile(image):
                # if a text file is used as input
                # the first line (only the first line) can be used to indicate a text (title)
                # that will be inserted in the header of each page and will take precedence over 
                # the possible value indicated on the command line (--header parameter)
                # headerFlag will be a flag to indicate that the image value should be used in the header
                imageText = headerFlag
            elif not validImage(image, excludePattern):
                # the previous iterators provide a list of files
                # here we filter to keep only the ones we're interested in, ignoring the rest
                print(f'The file {image} is not an allowed image. Omitted')
                continue
            elif not imageText:
                # if f is a directory or no text has been supplied for the image
                # the name of the image file will be used as the text associated with the image
                imageText = imageTitle(image)

            yield imageText, image

    except IOError as e:
        print('An I/O error has occurred')
        raise e
    except Exception as e:
        raise e


def main():
    
    from pprint import pprint

    print(os.getcwd())
    
    args = parseArgs()

    f = args.fileOrFolder
    if not(os.path.isfile(f) or os.path.isdir(f)):
        raise Exception(f'{f} is neither a file nor a folder')

    if not args.outputFileName:
        # the name of the output file has not been specified
        # if f is a file, the same file will be used as path and output name changing the extension to PDF
        # if f is a directory, the directory will be used as path and filename will be the directory name with PDF extension
        fullPath = os.path.realpath(f)
        path = os.path.dirname(fullPath)
        basename = os.path.basename(fullPath)
        name, _ = os.path.splitext(basename)
        args.outputFileName = os.path.join(path, name + nameSeparator + defaultName + defaultExtension)

    if args.background and not os.path.isfile(args.background):
        raise Exception(f'The background parameter is not a file: {args.background}')

    pprint(args)

    pageWidth, pageHeight = pages[args.page] if not args.landscape else landscape(pages[args.page])

    # information about the page and cells
    pageFormat = Page(
        pageWidth,
        pageHeight,
        cells=(args.columns, args.rows),
        margins=(args.marginLeft*unit, args.marginRight*unit, args.marginTop*unit, args.marginBottom*unit),
        cellMargins=(
            args.internalMargin*unit, args.internalMargin*unit, args.internalMargin*unit, args.internalMargin*unit
        ),
        gap=(args.gapHorizontal*unit, args.gapVertical*unit)
    )

    dumpFile = None

    if args.dump:
        # will dump the image information (path and text) to a text file
        # will use the same path and name as for the output file changing the extension to .txt
        basename, extension = os.path.splitext(args.outputFileName)
        dumpFile = basename + dumpExtension
        if os.path.isfile(args.fileOrFolder) and dumpFile == args.fileOrFolder:
            # if the name of the input file matches the dump file name
            # we put a suffix in the name of the latter so that they do not coincide
            dumpFile = basename + nameSeparator + dumpExtension

    # create the images generator
    imagesList = imagesIterator(args.fileOrFolder, args.recursive, excludePattern=args.exclude)

    # all the necessary information has been collected
    # create the PDF
    createPDF(
        dump(dumpFile, imagesList) if dumpFile else imagesList,
        args.outputFileName,
        pageFormat,
        withBorder=args.border,
        withTitle=args.text,
        fontSize=args.fontSize,
        background=args.background,
        expand=args.expand,
        withDate=args.date,
        withNumberPages=args.numberPages,
        header=args.header
    )

if __name__ == "__main__":

    main()
