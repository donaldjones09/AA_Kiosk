#!C:\Users\jones\Documents\GitHub\AA_ARCHIVES\arch\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Flask','console_scripts','flask'
__requires__ = 'Flask'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Flask', 'console_scripts', 'flask')()
    )
