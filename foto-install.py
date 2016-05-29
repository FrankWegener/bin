#!/usr/bin/python

# this script require:
#   apt-get install exiv2


import os
import shutil
import subprocess
import sys

PATH_OFFEN = "/mnt/_k/__offen"
PATH_JPG   = "/mnt/_k/owncloud/fwe/_fwe-photo-offen-jpg"
PATH_RAW   = "/mnt/_k/owncloud/fwe/_fwe-photo-offen-raw"


def error(msg):
    print("----> Error: %s" % msg)
    raise NameError(msg)


def is_jpgfile(f):
    return (len(f) > 4 and f[-4:].lower() == ".jpg")


def jpgfile_date(jpg_file):
    output = subprocess.check_output(['exiv2', '-q', jpg_file])

    for line in output.split('\n'):
        if "Image timestamp" in line:
            # Image timestamp : 2014:10:04 17:17:58
            # Zeitstempel des Bildes: 2014:10:04 17:17:58
            year   = line[18:22]
            month  = line[23:25]
            day    = line[26:28]
            return "%s-%s-%s" % (year, month, day)
 
    error("No timestamp information in file '%s' " % (raw_file))


def rename(jpgfile, date, nr):
    path_raw    = PATH_RAW + '/' + date
    path_jpg    = PATH_JPG + '/' + date
    new_rawfile = "%s/%s-%04d.orf" % (path_raw, date, nr)
    new_jpgfile = "%s/%s-%04d.jpg" % (path_jpg, date, nr)

    if not os.path.exists(path_raw):
        os.mkdir(path_raw, 0750)

    if not os.path.exists(path_jpg):
        os.mkdir(path_jpg, 0750)

    shutil.move(jpgfile, new_jpgfile)

    rawfile = jpgfile[:-4] + '.ORF'

    if os.path.exists(rawfile):
        shutil.move(rawfile, new_rawfile)


def main():
    date = "xxxx"
    nr   = 0

    for f in sorted(os.listdir(PATH_OFFEN)):
        f = PATH_OFFEN + "/" + f

        if not os.path.isfile(f):
            continue

        if not is_jpgfile(f):
           continue

        new_date = jpgfile_date(f)
 
        if (new_date != date):
            date = new_date
            nr   = 0
       
        rename(f, date, nr)
        nr  += 1


main()
