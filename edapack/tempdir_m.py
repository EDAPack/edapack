#****************************************************************************
#* tempdir_m.py
#*
#* Manage temp directories for EDAPack
#****************************************************************************
import atexit
import shutil
import tempfile

tempdirs = []

def cleanup():
    if len(tempdirs) > 0:
        print("Note: cleaning up temp directories")

    for dir in tempdirs:
        shutil.rmtree(dir)
    
def mktempdir():
    dir =  tempfile.mkdtemp(prefix="edapack_")
    tempdirs.append(dir)
    return dir
    
    
atexit.register(cleanup)