'''Parser of the command line parameters'''

import argparse

from defaults import pageNames, mm, defaultPageMargin, defaultMargin, defaultGap, defaultPage, \
    minCols, maxCols, defaultCols, minRows, maxRows, defaultRows,  defaultFontSize, dumpExtension

def parseArgs():    

    parser = argparse.ArgumentParser(description='Create a PDF document from a collection of images')

    marginMM = defaultPageMargin/mm  # default page margin in mm

    gapMM = defaultGap/mm  # defaul space between images in mm

    # page size
    parser.add_argument(
        '-p',
        '--page',
        choices=pageNames,
        default=defaultPage,
        type=str.upper,  # case insensitive
        help=f'Page format. Default: {defaultPage}'
    )

    # page orientation
    parser.add_argument(
        '-l',
        '--landscape',
        action='store_true',
        help=f'Orient the page horizontally (landscape). Default: vertical'
    )

    # number of columns (images showed horizontally)
    parser.add_argument(
        '-c',
        '--columns',
        choices=range(minCols, maxCols+1),
        type=int,
        default=defaultCols,
        help=f'Number of columns. Value between {minCols} and {maxCols}. Default: {defaultCols}'
    )

    # number of rows (images showed vertically)
    parser.add_argument(
        '-w',
        '--rows',
        choices=range(minRows, maxRows+1),
        type=int,
        default=defaultRows,
        help=f'Number of rows. Value between {minRows} and {maxRows}. Default: {defaultRows}'
    )

    # path and name ot the generated PDF
    parser.add_argument(
        '-o',
        '--outputFileName',
        help='Path and name of the generated PDF'
    )

    # if fileOrFolder is a folder and this flag is true, it traverses the folder recursively 
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help='Traverse the input folder recursively'
    )

    # create a text file with the list of images and their descriptions
    # using the created file as input, the same catalog will be generated
    # however, the created file may not be the same as the input file: images may have been deleted or text may have been added.
    parser.add_argument(
        '--dump',
        action='store_true',
        help=f'Dump the list of images and their description into a file with the extension {dumpExtension}. '
             'This file can be used to regenerate the catalog'
    )

    # remove the text of the images
    parser.add_argument(
        '-t',
        '--text',
        action='store_false',
        help='Remove the text of the images'
    )

    # write current date and time in the page footer
    parser.add_argument(
        '-d',
        '--date',
        action='store_true',
        help='Write current date and time in the page footer'
    )

    # write the page number in the page footer
    parser.add_argument(
        '-n',
        '--numberPages',
        action='store_true',
        help='Write the page number in the page footer'
    )

    # remove the images border
    parser.add_argument(
        '-b',
        '--border',
        action='store_false',
        help='Remove the images border'
    )

    # font size
    parser.add_argument(
        '-s',
        '--fontSize',
        type=int,
        default=defaultFontSize,
        help=f'Font size. Default: {defaultFontSize}'
    )

    # page header
    parser.add_argument(
        '--header',
        type=str,
        default="",
        help='Page header. Use quotations marks if text contains spaces'
    )

    # top margin of the page
    parser.add_argument(
        '-mt',
        '--marginTop',
        type=int,
        default=defaultPageMargin,
        help=f'Top margin of the page, in mm. Default: {marginMM}'
    )

    # bottom margin of the page
    parser.add_argument(
        '-mb',
        '--marginBottom',
        type=int,
        default=defaultPageMargin,
        help=f'Bottom margin of the page, in mm. Default: {marginMM}'
    )

    # left margin of the page
    parser.add_argument(
        '-ml',
        '--marginLeft',
        type=int,
        default=defaultPageMargin,
        help=f'Left margin of the page, in mm. Default: {marginMM}'
    )

    # right margin of the page
    parser.add_argument(
        '-mr',
        '--marginRight',
        type=int,
        default=defaultPageMargin,
        help=f'Right margin of the page, in mm. Default: {marginMM}'
    )

    # margins of the cells, the same for top, bottom, left and right
    parser.add_argument(
        '-i',
        '--internalMargin',
        type=int,
        default=defaultMargin,
        help=f'Margin of the images, in mm. Default: {defaultMargin/mm}'
    )

    # vertical space between images
    parser.add_argument(
        '-gv',
        '--gapVertical',
        type=int,
        default=defaultGap,
        help=f'Vertical space between images, in mm. Default: {gapMM}'
    )

    # horizontal space between images
    parser.add_argument(
        '-gh',
        '--gapHorizontal',
        type=int,
        default=defaultGap,
        help=f'Horizontal space between images, in mm. Default: {gapMM}'
    )

    # the path to an image to be used as the background of the pages
    parser.add_argument(
        '-k',
        '--background',
        help='Background image of the pages'
    )

    # background image will fit the page size
    # by default, the size of the background image will be used
    parser.add_argument(
        '-e',
        '--expand',
        action='store_true',
        help='Make the background image fit the page size'
    )

    # text pattern
    # if the full path of an image contains this pattern it will be excluded from the catalog
    # for example, use -x .thumbnails to exclude all images of the .thumbnails folder
    parser.add_argument(
        '-x',
        '--exclude',
        help='Text pattern. Exclude all images containing this pattern in their full path'
    )

    # file or folder to be processed
    # in the case of a folder, all images with the allowed extensions will be added to the catalog
    # the folder will be traversed recursively if the -r flag is used
    # in the case of a file, each line of the file is a list of fields separated by semicolons
    # only the first field is mandatory and it is the path to the image
    # the rest of the fields, if any, are strings and will be used as the image description, each field on its own line, from top to bottom.
    parser.add_argument(
        'fileOrFolder',
        help='File or folder containing the image collection'
    )

    return parser.parse_args()
