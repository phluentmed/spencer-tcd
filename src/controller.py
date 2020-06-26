import argparse

parser = argparse.ArgumentParser(description='Program controller')

parser.add_argument('-b', '--baud', default='12400')
parser.add_argument('-o', '--outfile')
parser.add_argument('-w', '--web_out')

args = parser.parse_args()

print(args.baud)
print(args.outfile)
print(args.web_out)

if args.outfile == None and args.web_out == None:
	print('specify at least one output destination')
	exit()

