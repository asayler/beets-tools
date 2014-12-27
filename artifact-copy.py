#!/usr/bin/env python3

import os
import os.path
import sys

_EXTS = [".cue", ".log", ".m3u"]

def copy(src, dst):

    src_base = os.path.abspath(src)
    dst_base = os.path.abspath(dst)

    for root, dirs, files in os.walk(src_base, topdown=False):

        for fle_name in files:

            fle_path = os.path.join(root, fle_name)
            fle_ext = os.path.splitext(fle_name)[1].lower()

            if fle_ext in _EXTS:

                fle_rel = os.path.relpath(fle_path, src_base)
                dst_path = os.path.join(dst_base, fle_rel)
                dst_dir = os.path.dirname(dst_path)
                print("Moving '{:s}' to '{:s}'".format(fle_path, dst_path))

                if os.path.exists(dst_dir):
                    os.rename(fle_path, dst_path)
                else:
                    print("FAIL: Destination '{:s}' Missing".format(dst_dir), file=sys.stderr)

        for dir_name in dirs:

            dir_path = os.path.join(root, dir_name)
            print("Removing Directory: '{:s}'".format(dir_path))

            if not os.listdir(dir_path):
                os.rmdir(dir_path)
            else:
                print("FAIL: Directory not empty", file=sys.stderr)

if __name__ == "__main__":

    copy(sys.argv[1], sys.argv[2])
