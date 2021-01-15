#
# Scale obj file
#
# EE Jan '21

SCALE = 10000.0

with open('36158833.obj', 'r') as f:
	lines = f.read().splitlines()
	with open('my.obj', 'w') as f2:
		for line in lines:
			if line[0] == 'v':
				parts = line.split()
				x = float(parts[1]) / SCALE
				y = float(parts[2]) / SCALE
				z = float(parts[3]) / SCALE
				f2.write('v {} {} {}\n'.format(x,y,z))
			else:
				f2.write('{}\n'.format(line))
