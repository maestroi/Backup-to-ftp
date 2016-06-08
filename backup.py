#!/usr/bin/env python
from ftplib import FTP
from subprocess import call
import os
import sys
import time

def header():
    print "  __  __                 _             "
    print " |  \/  |               | |            "
    print " | \  / | __ _  ___  ___| |_ _ __ ___  "
    print " | |\/| |/ _` |/ _ \/ __| __| '__/ _ \ "
    print " | |  | | (_| |  __/\__ \ |_| | | (_) |"
    print " |_|  |_|\__,_|\___||___/\__|_|  \___/|"
    print "                                       "
    print "                                       "
    print "Version: %s" % versie

##Global settings
versie = '0.3'                                                              ## Version program
datum = time.strftime("%d-%m-%Y")                                           ## Way date is noted
connectftp = FTP('FTPADRES', 'USERNAME', 'PASSWORD' )                       ## FTP Information
backupfolders = '/home /var/www/html'                                       ## Backup Directory's
webbestand = 'backup-%s.7z'% datum                                          ## Backup file name
logbestand = 'backup-%s.log'% datum                                         ## Log File of files being backupped.

header()

### cleaner! this checks if there is a file that is older than 7 days and delete it.
try:
    now = time.time()
    cutoff = now - (7 * 86400)
    files = os.listdir("/backup")
    for xfile in files:
        if os.path.isfile("/backup/" + xfile):
            t = os.stat("/backup/" + xfile)
            c = t.st_ctime

            # delete file if older than a week
            if c < cutoff:
                os.remove("/backup/" + xfile)
except:
    print "Nothing to clean :)"
    pass

### this is the main compression section. it needs tqdm and 7z installed to make it work (provided in setupfile).
try:
    print 40 * "-"
    os.system("7z a -bd -r /backup/%s %s | grep Compressing | tqdm --total $(find %s -type f | wc -l) --unit files >> /backup/%s" %(webbestand, backupfolders, backupfolders, logbestand))
    print 40 * "-"
    print 'Backup Complete!'
except:
    print 40 * "-"
    print "Could not make backup!!"
    print 40 * "-"

### this will make a directory on your ftp server en store the newly created backup.
try:
    try:
        connectftp.mkd(datum)
    except:
        connectftp.cwd(datum)
        file = open('/backup/%s' % webbestand, 'rb')
        connectftp.storbinary('STOR %s' % webbestand, file)
        file.close()
        connectftp.quit()
        print 40 * "-"
        print 'Upload Complete!'
        print 40 * "-"
except:
    print 40 * "-"
    print "Could not connect to FTP"
    print 40 * "-"
sys, exit()
