# Imatologue

Create a PDF document from a collection of images.

**Usage:**  

    python imatologue.py 
    [-h] 
    [-p {A4,A0,A1,A2,A3,A5,A6,B0,B1,B2,B3,B4,B5,B6,legal,letter}] 
    [-l] 
    [-c {1,2,3,4,5,6,7,8,9,10}]
    [-w {1,2,3,4,5,6,7,8,9,10}] 
    [-o OUTPUTFILENAME] 
    [-r] 
    [--dump] 
    [-t] 
    [-d] 
    [-n] 
    [-b] 
    [-s FONTSIZE] 
    [--header HEADER]
    [-mt MARGINTOP] [-mb MARGINBOTTOM] [-ml MARGINLEFT] [-mr MARGINRIGHT] 
    [-i INTERNALMARGIN] 
    [-gv GAPVERTICAL] [-gh GAPHORIZONTAL] 
    [-k BACKGROUND] 
    [-e] 
    [-x EXCLUDE]
    fileOrFolder

**Positional arguments:**    

  *fileOrFolder*   
  Text file containing a list of image paths or a folder containing the image collection.       

**Optional arguments:**    

  *-h, --help*   
  Show the help message.

  *-p {A4,A0,A1,A2,A3,A5,A6,B0,B1,B2,B3,B4,B5,B6,legal,letter}, --page {A4,A0,A1,A2,A3,A5,A6,B0,B1,B2,B3,B4,B5,B6,legal,letter}*    
  Page format. Default: A4.

  *-l, --landscape*      
  Orient the page horizontally (landscape). Default: vertical.

  *-c {1,2,3,4,5,6,7,8,9,10}, --columns {1,2,3,4,5,6,7,8,9,10}*   
  Number of columns. Value between 1 and 10. Default: 3.

  *-w {1,2,3,4,5,6,7,8,9,10}, --rows {1,2,3,4,5,6,7,8,9,10}*   
  Number of rows. Value between 1 and 10. Default: 4.

  *-o OUTPUTFILENAME, --outputFileName OUTPUTFILENAME*
  Path and name of the generated PDF.

  *-r, --recursive*       
  Traverse the input folder recursively.

  *--dump*               
  Dump the list of images and their description into a file with the extension .txt. This file can be used to
  regenerate the catalog.

  *-t, --text*            
  Remove the text of the images.

  *-d, --date*            
  Write current date and time in the page footer.

  *-n, --numberPages*     
  Write the page number in the page footer.

  *-b, --border*          
  Remove the images border.

  *-s FONTSIZE, --fontSize FONTSIZE*    
  Font size. Default: 10.

  *--header HEADER*       
  Page header. Use quotations marks if text contains spaces.

  *-mt MARGINTOP, --marginTop MARGINTOP*    
  Top margin of the page, in mm. Default: 5.0.

  *-mb MARGINBOTTOM, --marginBottom MARGINBOTTOM*    
  Bottom margin of the page, in mm. Default: 5.0.

  *-ml MARGINLEFT, --marginLeft MARGINLEFT*    
  Left margin of the page, in mm. Default: 5.0.

  *-mr MARGINRIGHT, --marginRight MARGINRIGHT*    
  Right margin of the page, in mm. Default: 5.0.

  *-i INTERNALMARGIN, --internalMargin INTERNALMARGIN*    
  Margin of the images, in mm. Default: 1.0.

  *-gv GAPVERTICAL, --gapVertical GAPVERTICAL*    
  Vertical space between images, in mm. Default: 0.0.

  *-gh GAPHORIZONTAL, --gapHorizontal GAPHORIZONTAL*    
  Horizontal space between images, in mm. Default: 0.0.

  *-k BACKGROUND, --background BACKGROUND*    
  Background image of the pages

  *-e, --expand*          
  Make the background image fit the page size

  *-x EXCLUDE, --exclude EXCLUDE*   
  Text pattern. Exclude all images containing this pattern in their full path.
  
