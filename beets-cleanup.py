#!/usr/bin/env python3

import os
import sys
import mimetypes

_MIME_MV = ["audio/flac"]
_MIME_RM = ["image/jpeg"]

def clean(src, dst):

    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    for root, dirs, files in os.walk(src, topdown=False):

        mime_cnts = {}
        files_types = []

        for name in files:

            typ, enc = mimetypes.guess_type(name)
            if typ in mime_cnts:
                mime_cnts[typ] += 1
            else:
                mime_cnts[typ] = 1
            files_types.append((name, typ, enc))

        for tup in files_types:

            name, typ, enc = tup
            src_path = os.path.join(root, name)

            if typ in _MIME_MV:
                if mime_cnts[typ] == 1:
                    base_dir, src_dir = os.path.split(root)
                    dst_dir = os.path.join(dst, src_dir)
                    os.makedirs(dst_dir, exist_ok=True)
                    print("Moving: '{:s}' -> '{:s}'".format(src_path, dst_dir))
                    dst_path = os.path.join(dst_dir, name)
                    if not os.path.exists(dst_path):
                        os.rename(src_path, dst_path)
                    else:
                        print("FAIL: Destination already exists")
                else:
                    print("Multiple {:s} Files, Skipping: '{:s}'".format(typ, src_path))

            if typ in _MIME_RM:
                print("Removing: {:s}".format(src_path))
                os.remove(src_path)

        for name in dirs:
            dir_path = os.path.join(root, name)
            print("Removing Directory: {:s}".format(dir_path))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
            else:
                print("FAIL: Directory not empty")

if __name__ == "__main__":

    clean(sys.argv[1], sys.argv[2])
