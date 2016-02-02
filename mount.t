#!/bin/bash 

## *** created by puppet ***
## *************************
 
# /usr/local/bin/mount.t
#


/bin/df | /bin/grep /mnt/_t

if [[ $? == 0 ]] ; then
	/bin/echo "encfs already mounted"
	exit 0
fi

sudo /usr/bin/encfs --public --idle=15 /mnt/_g/.trust.enc /mnt/_t
