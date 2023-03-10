# WIKIFILE (wf) FORMAT:

#### Github Note
To run the reader I've prepared a simple wf.file that
can be decoded by running `./reader.py test.wf`

## Intro:
Wikifile is supposed to compress any wikipedia article into one file.
Having this ability proves that it can be used to compose and archive
anything.


## Creator:
-Imalaia3


## Specification:
Currently wikifile uses string syntax with some pros and cons:
-PROS:
--ease of use (encode and decode)
-COBS:
--large file size (MB)

#### NOTE: Wikifile will, at some point, be rewritten to support binary format

This is how the format works:
Tokens are always sepereated by \n EXCEPT for when the last token was T_TEXTB.
The \n sepereation continiues normally after T_TEXTS.


### Token definition with no specific order:
```T_TEXTB: actual:T_TEXTBEGIN, Marks the start of a text block, data:YES (Title of text)
T_TEXTS: actual:T_TEXTSTOP,  Marks the end   of a text block, data: NO
T_LSWRI: actual:T_LISTWRITER, Lists writer(s) of the article, data:YES (writers)
T_IMAGE: actual:T_IMAGE, Marks an Image, data: YES: (Image alias (for later use))
T_IMGEN: actual:T_IMAGEEND, Marks Image Block End, data:NO
T_HEADI: actual:T_HEADERONE, Contains useful info about writers, location, hosted device, etc. data: YES (info, split with ",")
T_ENDIN: actual: T_ENDING , Defines the end of a wiki file. This is reserved for creating a wiki transfer protocol in which wikis will be split.
T_IMREF: actual: T_IMAGEREFERAL, Marks a spot for an already defined image to be placed
T_WIKII: actual: T_WIKIINFO, Defines info about wiki title, pages, etc, data: YES (same as T_HEADI)
```
### PROPER LAYOUT: (This will probalby not be inforced, but some compact optimized readers might require it in the future)
```T_WIKII
T_LSWRI
T_IMAGE
...
T_IMAGE
T_TEXTB...T_TEXTS or T_IMREF
T_HEADI
T_ENDIN
```

### IMAGES:
Sadly, due to many complications, we will have to use base64 images, a speedy,yet EXTREMELY inneficient (1/3 more size)
format. In later revisions (rev 2) this format will use byte encoding which will result in 1 to 1 file encoding, allowing
not only smaller size but also possibilities for actual files (exe, iso, zip) 
