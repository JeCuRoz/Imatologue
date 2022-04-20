'''Default values'''

from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4, A5, A6, B0, B1, B2, B3, B4, B5, B6, legal, letter, landscape
from datetime import datetime


# author and application name
# showed in the generated PDF
AUTHOR = 'JeCuRoz'
APPNAME = 'Imatologue'
CREATOR = '{} (developed by {})'.format(APPNAME, AUTHOR)

unit = mm  # millimeter is the unit of measurement

# allowed page sizes
# they are tuples: (width, height)
pageSizes = [A4, A0, A1, A2, A3, A5, A6, B0, B1, B2, B3, B4, B5, B6, legal, letter]
# names of the valid pages
pageNames = ['A4', 'A0', 'A1', 'A2', 'A3', 'A5', 'A6', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'legal', 'letter']
# page sizes dict
pages = {key: value for key, value in zip(pageNames, pageSizes)}

# default page size
defaultPage = pageNames[0]  # A4

# number of rows: minimum, maximum and default
minRows = 1
maxRows = 10
defaultRows = 4

# number of columns: minimum, maximum and default
minCols = 1
maxCols = 10
defaultCols = 3

# allowed image formats
imageFileExtensions = ['.jpg', '.png', '.gif']

# when using an input file, each line of the file is a list of fields separated by a separator
# only the first field is mandatory and it is the path to the image
# the rest of the fields, if any, are strings and will be used as the image description instead of the file names
# here, we define the field separator
fieldSeparator = ';'

# default font name and size
defaultFontName = 'Helvetica'
defaultFontSize = 10

# default internal margin of the cells
defaultMargin = 1 * unit

# default spacing between cells
defaultGap = 0  # 0 * unit

# default page margin
defaultPageMargin = 5 * unit

# header and footer margins
textMargin = 5 * mm

# default catalog name
defaultName = 'catalogue'

# default catalog extension
defaultExtension = '.pdf'

# extension of output text files
dumpExtension = '.txt'

nameSeparator = '_'
wordSeparator = ' '

newLine = '\n'

commentChar = '#'  # when using an input file, the lines starting with # will be ignored

# when using an input file, this flag is used to indicate that the first line of the file 
# is the header of the page and not an image
headerFlag = '@header@'


# the current date and time
def now():
    return datetime.now().strftime("%d/%m/%Y -- %H:%M:%S")
