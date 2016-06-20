#!/usr/bin/python

# this script require:
#   apt-get install libimage-exiftool-perl


import os
import shutil
import subprocess
import sys

PATH_OFFEN = "/mnt/_k/__offen"
PATH_JPG   = "/mnt/_k/owncloud/_fwe-photo-offen-jpg"
PATH_RAW   = "/mnt/_k/owncloud/_fwe-photo-offen-raw"
PATH_MOV   = "/mnt/_k/owncloud/_fwe-video-offen"


def error(msg):
    print("----> Error: %s" % msg)
    raise NameError(msg)


def is_jpgfile(f):
    return (len(f) > 4 and f[-4:].lower() == ".jpg")


def is_movfile(f):
    return (len(f) > 4 and f[-4:].lower() == ".mov")


def jpgfile_date(jpg_file):
    output = subprocess.check_output(['exiftool', '-q', jpg_file])

    for line in output.split('\n'):
        if "Create Date" in line:
            # Image timestamp : 2014:10:04 17:17:58
            year   = line[34:38]
            month  = line[39:41]
            day    = line[42:44]
            return "%s-%s-%s" % (year, month, day)

    error("No timestamp information in file '%s' " % (raw_file))


def movfile_timestamp(jpg_file):
    output = subprocess.check_output(['exiftool', '-q', jpg_file])

    for line in output.split('\n'):
        if "Media Create Date" in line:
            # Zeitstempel des Bildes: 2014:10:04 17:17:58
            year   = line[34:38]
            month  = line[39:41]
            day    = line[42:44]
            hour   = line[45:47]
            minut  = line[48:50]
            secs   = line[51:53]
            return ("%s-%s-%s" % (year, month, day), "%s:%s.%s" % (hour, minut, secs))

    error("No timestamp information in file '%s' " % (raw_file))


def rename_photo(jpgfile, date, nr):
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


def rename_video(movfile, date, timestamp, nr):
    path_mov    = PATH_MOV + '/' + date
    new_movfile = "%s/%s__%s__%04d.mov" % (path_mov, date, timestamp, nr)

    if not os.path.exists(path_mov):
        os.mkdir(path_mov, 0750)

    shutil.move(movfile, new_movfile)


def main():
    date = "xxxx"
    nr   = 0

    for f in sorted(os.listdir(PATH_OFFEN)):
        f = PATH_OFFEN + "/" + f

        if not os.path.isfile(f) or not is_jpgfile(f):
            continue

        new_date = jpgfile_date(f)
 
        if (new_date != date):
            date = new_date
            nr   = 0
       
        rename_photo(f, date, nr)
        nr += 1
        continue

    date = "xxxx"
    nr   = 0

    for f in sorted(os.listdir(PATH_OFFEN)):
        f = PATH_OFFEN + "/" + f

        if not os.path.isfile(f) or not is_movfile(f):
            continue

        new_date, timestamp = movfile_timestamp(f)
 
        if (new_date != date):
            date = new_date
            nr   = 0
       
        rename_video(f, date, timestamp, nr)
        nr += 1
        continue

main()
