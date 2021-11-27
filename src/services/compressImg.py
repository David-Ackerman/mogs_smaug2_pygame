import os
import shutil
import sys
import os.path


def decompressAssets():
    if os.path.isfile("assets/images.tar.gz"):
        shutil.unpack_archive("assets/images.tar.gz",
                              './assets/images', 'gztar')
        os.remove("assets/images.tar.gz")
    return


def compressAssets():
    if os.path.exists("assets/images"):
        shutil.make_archive('assets/images', 'gztar', 'assets/images')
        deleteDescompressed("assets/images")
    return


def deleteDescompressed(removed: str):
    try:
        shutil.rmtree(removed, False, None)
    except Exception as e:
        print(e)
