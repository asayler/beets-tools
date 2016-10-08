#!/usr/bin/env python3

import os
import os.path
import sys
import re
import mimetypes

_RE_END = 'a-zA-Z0-9_\-,!.\''
_RE_START = _RE_END + ' '
_RE_FIELD = "[{}]*[{}]".format(_RE_START, _RE_END)

_MIME_MV = ["audio/flac"]
_MIME_RM = ["image/jpeg"]

def combine(src):

    src_base = os.path.abspath(src)

    for root, dirs, files in os.walk(src_base, topdown=True):

        processed = []
        for dir_name in dirs:

            # Search for Multi-Disk Pattern
            src_dir = os.path.join(root, dir_name)
            res = re.search('^({0}) \[({0})\]$'.format(_RE_FIELD), dir_name)
            if res:

                # Combine
                print("Combining '{}'".format(src_dir))
                major = res.group(1)
                minor = res.group(2)
                dst_dir = os.path.join(root, major)
                os.makedirs(dst_dir, exist_ok=True)
                for fle_name in os.listdir(src_dir):
                    src_fle = os.path.join(src_dir, fle_name)
                    typ, enc = mimetypes.guess_type(fle_name)
                    if typ in _MIME_MV:
                        dst_fle = os.path.join(dst_dir, fle_name)
                        print("Moving '{}' to '{}'".format(fle_name, dst_dir))
                        os.rename(src_fle, dst_fle)
                    elif typ in _MIME_RM:
                        print("Removing '{}'".format(fle_name))
                        os.remove(src_fle)
                    else:
                        print("Ignoring '{}'".format(fle_name))

                # Remove Empties
                print("Removing '{:s}'".format(src_dir))
                if not os.listdir(src_dir):
                    os.rmdir(src_dir)
                else:
                    print("FAIL: Directory not empty", file=sys.stderr)
                if dir_name not in processed:
                    processed.append(dir_name)

            else:
                print("Skipping '{}'".format(src_dir))

        # Remove Processed Dirs
        for dir_name in processed:
            dirs.remove(dir_name)

if __name__ == "__main__":

    combine(sys.argv[1])
