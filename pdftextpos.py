from pathlib import Path
from typing import Iterable, Any
from pdfminer.high_level import extract_pages
import sys
import os

#Global page counter
page = 1

def show_ltitem_hierarchy(o: Any, depth=0):
    """Show location and text of LTItem and all its descendants"""
    if depth == 0:
        print('element                        x1  y1  x2  y2   text')
        print('------------------------------ --- --- --- ---- -----')

    #Comment nex condition to have individual characters position on page
    if o.__class__.__name__ == "LTChar":
       return

    if o.__class__.__name__ == "LTAnno":
       return

    if o.__class__.__name__ != "LTTextBoxHorizontal":
       print(
          f'{get_indented_name(o, depth):<30.30s} '
          f'{get_optional_bbox(o)} '
          f'{get_optional_text(o)}'
       )
    
    if isinstance(o, Iterable):
        for i in o:
            show_ltitem_hierarchy(i, depth=depth + 1)


def get_indented_name(o: Any, depth: int) -> str:
    """Indented name of LTItem"""
    
    if o.__class__.__name__ == "LTPage":
       global page
       ctrl=' '+str(page)
       page+=1
    else:
       ctrl=''

    return '  ' * depth + o.__class__.__name__ + ctrl


def get_optional_bbox(o: Any) -> str:
    """Bounding box of LTItem if available, otherwise empty string"""
    if hasattr(o, 'bbox'):
        return ''.join(f'{i:<4.0f}' for i in o.bbox)
    return ''


def get_optional_text(o: Any) -> str:
    """Text of LTItem if available, otherwise empty string"""
    if hasattr(o, 'get_text'):
        return o.get_text().strip()
    return ''

if len(sys.argv) != 2:
    print("Input pdf file must be specified")
    print('fg.:',sys.argv[0], 'input.pdf')
    sys.exit()

path = Path(sys.argv[1]).expanduser()

if not os.path.isfile(path):
   print('Specified file does not exists!')
   sys.exit()

pages = extract_pages(path)
show_ltitem_hierarchy(pages)
