#!/usr/bin/env python3

import sys
import os
import shutil
from configparser import DEFAULTSECT, RawConfigParser
from tempfile import mkstemp

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = "config.ini"

oconfig = RawConfigParser()
oconfig.read(filename)

fd, path = mkstemp()

with os.fdopen(fd, "w") as fp:
    if oconfig.defaults():
        fp.write("[%s]\n" % DEFAULTSECT)
        for key, value in oconfig.defaults().items():
            fp.write("{} = {}\n".format(key, str(value).replace("\n", "\n\t")))
        fp.write("\n")

    result = {}
    for section in sorted(oconfig.sections()):
        if section == "Planet":
            fp.write("[%s]\n" % section)
        for key, value in oconfig.items(section, raw=True):
            if key != "__name__":
                if section == "Planet":
                    fp.write("{} = {}\n".format(key, str(value).replace("\n", "\n\t")))
                else:
                    result[value.replace('"', "")] = section
        if section == "Planet":
            fp.write("\n")

    for key, value in sorted(result.items()):
        fp.write("[%s]\n" % value)
        name = key
        if "'" in key:
            name = '"%s"' % key
        fp.write("name = %s\n" % name)
        fp.write("\n")

shutil.move(path, filename)
