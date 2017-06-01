#!/usr/bin/env python2

from __future__ import print_function
import argparse, gzip, sys, re

parser = argparse.ArgumentParser(description='Sort gff per gene coordinate. Preserve the feature order of the original file (gene parent of [mRNA parent of [5_UTR, CDS, 3_UTR]]) etc.')

parser.add_argument('input_gff', help='gff to be sorted per chr per coordinate.', nargs=1)
parser.add_argument('output_gff', help='Name or the output sorted gff.', nargs=1)
parser.add_argument('-g', '--gzip', help='gzip result gff [True]', action='store_true')
args = parser.parse_args()

gff = args.input_gff[0]
out = args.output_gff[0]
do_gzip = args.gzip

if do_gzip and out[-3:]!=".gz": 
	out = out + ".gz"

print(out)

def read_open(fil):
	if fil[-3:]==".gz":
		con = gzip.open(fil)
	else:
		con = open(fil)
	return(con)

def write_open(fil):
	if fil[-3:]==".gz":
		con = gzip.open(fil, "wb")
	else:
		con = open(fil, "wb")
	return(con)

# sort gff
IDs = {}
with read_open(gff) as f:
	for l in f:
		if l[0]=="#":
			head = l.strip()
		elif "Parent=" not in l:
			ID = re.split("ID=|;", l)[1]
			chro, sta, sto = [ l.split()[x] for x in [0, 3, 4]]
			key = "%s_%s_%s_%s" % (chro, sta.zfill(10), sto.zfill(10), ID)
			IDs[key] = {'chr': chro, 'start': sta, 'block':[l.strip()]}
		else:	# just store all the lines relative to the ID feature in the same order
			if ID not in l:
				sys.exit("CRITICAL ERROR: sub-feature not parent to previous ID!")
			IDs[key]['block'].append(l.strip())


# print results
with write_open(out) as f:
	print(head, file=f)
	for k in sorted(IDs.keys()):
		for l in IDs[k]['block']:
			print(l, file=f)
