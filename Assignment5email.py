# -*- coding: utf-8 -*-
"""
Spyder Editor
Programmer: Eve Jimenez Sagastegui
Class: Independent Study
Date: 08/05/19

"""
import argparse, sys

import re


class EmailType(object):
    """
    Supports checking email agains different patterns. (http://www.ietf.org/rfc/rfc5322.txt)
    """

    patterns = {
        'RFC5322': re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    }

    def __init__(self, pattern):
        if pattern not in self.patterns:
            raise KeyError('{} is not a supported email pattern, choose from:'
                           ' {}'.format(pattern, ','.join(self.patterns)))
        self._rules = pattern
        self._pattern = self.patterns[pattern]

    def __call__(self, value):
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError(
                "'{}' is not a valid email - does not match {} rules".format(value, self._rules))
        return value


def main():

    import ftputil
    import datetime


    ap = argparse.ArgumentParser(description='This script will outputs the file name and last modified time for the following files: gene2pubtator.gz, disease2pubtator.gz, mutation2pubtator.gz, chemical2pubtator.gz')
    ap.add_argument("email", type=EmailType('RFC5322'),help = "display email")

    if len(sys.argv)==1:
        ap.print_help(sys.stderr)
        sys.exit(1)

    args = vars(ap.parse_args())
    

    email = args['email']
#dancikg@easternct.edu
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

if __name__ == '__main__':
    main()