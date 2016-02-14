#!/usr/bin/python

# this script require:
#   apt-get install exiv2


import os
import shutil
import subprocess
import sys

PATH_OFFEN = "/mnt/_k/__offen"
PATH_RAW   = "/mnt/_k/media/__offen"


def error(msg):
    print("----> Error: %s" % msg)
    raise NameError(msg)


def is_rawfile(f):
    return (len(f) > 4 and f[-4:].lower() == ".orf")


def rawfile_date(raw_file):
    output = subprocess.check_output(['exiv2', raw_file])

    for line in output.split('\n'):
        if "Zeitstempel des Bildes" in line:
            # Image timestamp : 2014:10:04 17:17:58
            # Zeitstempel des Bildes: 2014:10:04 17:17:58
            year   = line[24:28]
            month  = line[29:31]
            day    = line[32:34]
            return "%s-%s-%s" % (year, month, day)
 
    error("No timestamp information in file '%s' " % (raw_file))


def rename(rawfile, date, nr):
    path_raw    = PATH_RAW + '/' + date
    new_rawfile = "%s/%s-%04d.orf" % (path_raw, date, nr)
    new_jpgfile = "%s  JPG/%s-%04d.jpg" % (path_raw, date, nr)


    if not os.path.exists(path_raw):
        os.mkdir(path_raw, 0750)

    shutil.move(rawfile, new_rawfile)

    jpgfile = rawfile[:-4] + '.JPG'

    if not os.path.exists(jpgfile):
        return

    path_raw += '  JPG'

    if not os.path.exists(path_raw):
        os.mkdir(path_raw, 0750)

    shutil.move(jpgfile, new_jpgfile)


def main():
    date = "xxxx"
    nr   = 0

    for f in sorted(os.listdir(PATH_OFFEN)):
        f = PATH_OFFEN + "/" + f

        if not os.path.isfile(f):
            continue

        if not is_rawfile(f):
           continue

        new_date = rawfile_date(f)
 
        if (new_date != date):
            date = new_date
            nr   = 0
       
        rename(f, date, nr)
        nr  += 1


main()
