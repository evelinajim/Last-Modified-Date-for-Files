# -*- coding: utf-8 -*-
"""
Spyder Editor
Programmer: Eve Jimenez Sagastegui
Class: Independent Study
Date: 08/05/19

"""

import ftputil
import datetime


import argparse, sys
ap = argparse.ArgumentParser(description='This script will outputs the file name and last modified time for the following files: gene2pubtator.gz, disease2pubtator.gz, mutation2pubtator.gz, chemical2pubtator.gz')
ap.add_argument("email", help = "display email")

if len(sys.argv)==1:
    ap.print_help(sys.stderr)
    sys.exit(1)

args = vars(ap.parse_args())


email = args['email'] 

# connect to FTP server using name (anonymous) and password (email address)
host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', email)


# list all files/folders in current directory
host.listdir('pub')

#changes directory to pub
host.chdir('pub')
host.chdir('lu')
host.chdir('PubTator')


files = ['disease2pubtator.gz',
         'gene2pubtator.gz',
         'mutation2pubtator.gz',
         'chemical2pubtator.gz']

#Gathering up the attributions of the files
disease = host.stat('disease2pubtator.gz')
gene = host.stat('gene2pubtator.gz')
mutation = host.stat('mutation2pubtator.gz')
chemical = host.stat('chemical2pubtator.gz')


lastModifiedDate = {'disease2pubtator.gz': datetime.datetime.fromtimestamp(disease[8]).strftime('%c'),
                    'gene2pubtator.gz' : datetime.datetime.fromtimestamp(gene[8]).strftime('%c'),
                    'mutation2pubtator.gz': datetime.datetime.fromtimestamp(mutation[8]).strftime('%c'),
                    'chemical2pubtator.gz': datetime.datetime.fromtimestamp(chemical[8]).strftime('%c')}

for i in lastModifiedDate:
    print("File Name: " + i)
    print("Last Modified Date: " + lastModifiedDate[i])
