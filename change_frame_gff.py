#!/usr/bin/env python2
# usage:
usage = "./change_frame_gff.py <gff_file> <new_gff_file>"

__author__ = "Ludovic Duvaux"
__maintainer__ = "Ludovic Duvaux"
__license__ = "GPL_v3"

import sys, re
v=0

argv = sys.argv
if len(argv) is not 3:
    print "Usage: " + usage
    sys.exit()

fgff = argv[1]
outp = argv[2]
gff2 = open(outp, "w")

with open(fgff) as gff:
    for l in gff:
        # 1) does the line "l" contain 'Parent=mRNA'?
        #~test = re.search(r"ID=exon:[0-9]{9}g[0-9]{5}[.]1;Parent=mRNA", l)
        test1 = re.search(r"ID=exon:.+g.+[.]1;Parent=mRNA", l)  # for EuGene gff3 files
        test2 = re.search(r"Parent=.+[.]mrna1;Target", l)   # for GMAP gff files
        if test1 or test2:
            lsp = l.split()
            strand = lsp[6]
            frame = int(lsp[7])
            
            # does the frame start at position zero?
            if frame == 0:
                print "frame_ok"
                gff2.write(l)
            # if not, change the frame for positive strand or...
            elif strand == "+":
                print "frame is " + str(frame) + " and strand is " + strand
                sstart = int(lsp[3])
                sstart2 = sstart + frame
                beg = "\t".join(lsp[:3])
                end = "\t".join(lsp[4:])
                ll = str(beg) + "\t" + str(sstart2) + "\t" + end
                gff2.write(l)
            # for negative strand.
            else:
                print "frame is " + str(frame) + " and strand is " + strand
                send = int(lsp[4])
                send2 = send - frame
                beg = "\t".join(lsp[:4])
                end = "\t".join(lsp[5:])
                ll = str(beg) + "\t" + str(send2) + "\t" + end
                gff2.write(l)

        # 2) if not, just print l
        else:
            #~print "just print line l"
            gff2.write(l)

gff2.close()
