from defaults import defaultPageMargin, defaultMargin, defaultGap, defaultCols, defaultRows


# Rectangular page (width, height) made up of a matrix of cells (N columns x M rows)
# The page has four margins: left, right, top, and bottom
# Each cell represents an image 
# Cells can have their own internal margins
# There can be horizontal and vertical spaces between cells (gap)
class Page:

    def __init__(
        self,
        width,  # page width
        height,  # page height
        # page margins: left, right, top, down
        margins=(defaultPageMargin, defaultPageMargin, defaultPageMargin, defaultPageMargin),
        # horizontal and vertical spacing between cells
        gap=(defaultGap, defaultGap),  
        # number of horizontal and vertical cells
        cells=(defaultCols, defaultRows),  
        # cell margins
        cellMargins=(defaultMargin, defaultMargin, defaultMargin, defaultMargin)  
    ):
        self.pageWidth = width
        self.pageHeight = height
        self.horizontalGap, self.verticalGap = gap
        self.cols, self.rows = cells
        self.pageLeft, self.pageRight, self.pageTop, self.pageBottom = margins
        self.cellLeft, self.cellRight, self.cellTop, self.cellBottom = cellMargins

    # page size
    @property
    def size(self):
        return self.pageWidth, self.pageHeight

    # cells per page
    @property
    def numCells(self):
        return self.rows * self.cols

    # page width without horizontal margins
    @property
    def internalWidth(self):
        return self.pageWidth - (self.pageLeft + self.pageRight)

    # page width without horizontal margins and horizontal spacing between cells
    @property
    def effectiveWidth(self):
        return self.internalWidth - (self.horizontalGap * (self.cols - 1))

    # cell width including its horizontal margins
    @property
    def cellWidth(self):
        return self.effectiveWidth // self.cols

    # cell width without its horizontal margins
    @property
    def cellInternalWidth(self):
        return self.cellWidth - (self.cellLeft + self.cellRight)

    # page height without vertical margins
    @property
    def internalHeight(self):
        return self.pageHeight - (self.pageTop + self.pageBottom)

    # page height without vertical margins and vertical spacing between cells
    @property
    def effectiveHeight(self):
        return self.internalHeight - (self.verticalGap * (self.rows - 1))

    # cell height including its vertical margins
    @property
    def cellHeight(self):
        return self.effectiveHeight // self.rows

    # cell height without its vertical margins
    @property
    def cellInternalHeight(self):
        return self.cellHeight - (self.cellTop + self.cellBottom)

    # each page has N cells (N = ROWS x COLUMNS)
    # we assign an index to each cell
    # 0 is the index of the upper left corner cell
    # N-1 is the index of the lower right corner cell
    def cellPosition(self, index):
        row, col = divmod(index, self.cols)
        return col, row

    # calculates the origin of the graphical coordinates of the cell on the sheet
    # reportlab places the origin of coordinates (0,0) in the lower left corner of the sheet
    # we calculate the origin of the lower left corner of the cell inside the sheet
    # note that the cells with lower indexes are placed at the top of the sheet
    # and those with higher indexes at the bottom of the sheet.
    # This implies that the cells with lower indexes have vertical coordinates greater than those with lower indexes
    # the horizontal coordinates work naturally (from left to right).
    def cellCoords(self, cell):
        try:
            col, row = cell  # cell is a tuple indicating the postition of the cell: (col, row)
        except TypeError:
            col, row = self.cellPosition(cell)  # cell is the index of the cell, an integer
        except Exception as e:
            raise e
        
        xOrigin = self.pageLeft + (self.cellWidth + self.horizontalGap) * col
        # we reverse the direction of the vertical indexes to adjust it to the reportlab coordinate system
        invertedRow = (self.numCells - 1) // self.cols - row
        yOrigin = self.pageBottom + (self.cellHeight + self.verticalGap) * invertedRow
        return xOrigin, yOrigin
