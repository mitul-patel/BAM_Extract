#!/usr/bin/python

"""
This script will extract all unmapped reads from the BAM file and write to reads_1.fastq, reads_2.fastq and reads.unpaired.fastq.
"""

__author__ = 'Mitul Patel'
__copyright__ = "Copyright 2017-18"
__license__ = "GPL"
__version__ = "v1.0"
__maintainer__ = "Mitul Patel"
__email__ = "Mitul.Patel@immunocore.com"
__status__ = "Production"

import csv
import sys
import os
import argparse
from optparse import OptionParser, OptionGroup, IndentedHelpFormatter

def help():
    '''Display help message if no arguments provided'''
    help_formatter = IndentedHelpFormatter(indent_increment=2, width=100)

    usage1 = "To extract unmapped reads:\n\t samtools view -f 0x4 mappingFILE.bam | %s --outbase <filebase>" % sys.argv[0]
    usage2 = "To extract mapped reads:\n\t samtools view -F 0x4 mappingFILE.bam | %s --outbase <filebase>" % sys.argv[0]
    version="Extract_unmapped_SAM "+__version__
    description=("Script to extract all unmapped/mapped reads from the BAM file and write to reads_1.fastq, reads_2.fastq and reads_unpaired.fastq. For bug reports, suggestions or questions mail to Mitul Patel: Mitul.Patel@immunocore.com")
    #author=__author__+__email__
    usage = "\n" + usage1 + "\n" + usage2
    parser = OptionParser(usage,version=version,description=description,formatter=help_formatter)

    # Main Input files
    group1 = OptionGroup(parser, "Inputs",
                '')
    group1.add_option('-i', '--in', action="store", dest='inFile',
                help='Read mapping file in BAM format [MANDATORY].')
    parser.add_option_group(group1)

    # Main Output files
    group2 = OptionGroup(parser, "Outputs",
                '')
    group2.add_option('-o', '--outbase', action="store", dest='outFile',
                help='Base name for output files in Fastq format [MANDATORY].')
    parser.add_option_group(group2)


    if(len(sys.argv) <= 2):
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()

def main():

    try:
        (options, args) = help()
        Extractor(options)
    except Exception, e:
        sys.exit(1)
        #print "The BAM file is empty of does not exists. Check input BAM file."
    
def Extractor(options):

    csvFILE = open(options.inFile)

    bamFILE = csv.reader(csvFILE, dialect="excel-tab")

    outbase = options.outFile

    PE1 = open("%s_1.fastq" % outbase, "w")
    PE2 = open("%s_2.fastq" % outbase, "w")
    unpaired = open("%s_unpaired.fastq" % outbase, "w")

    last = None
    for line in bamFILE:
        if(last == None):
            last = [line[0], line[9], line[10]]
        else:
            if(last[0] == line[0]):
                PE1.write("@%s\n%s\n+\n%s\n" % (last[0], last[1], last[2]))
                PE2.write("@%s\n%s\n+\n%s\n" % (line[0], line[9], line[10]))
                last = None
            else:
                unpaired.write("@%s\n%s\n+\n%s\n" % (last[0], last[1], last[2]))
                last = [line[0], line[9], line[10]]
    if(last != None):
        unpaired.write("@%s\n%s\n+\n%s\n" % (last[0], last[1], last[2]))
    PE1.close()
    PE2.close()
    unpaired.close()

if __name__ == '__main__':
    main()
