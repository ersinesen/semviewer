#
# Scale obj file
#
# EE Jan '21

SCALE = 10000.0


with open('36158833.obj', 'r') as f:
	lines = f.read().splitlines()

# find center of mass
X = Y = Z = []
for line in lines:
	if line[0] == 'v':
		parts = line.split()
		X.append(float(parts[1]))
		Y.append(float(parts[2]))
		Z.append(float(parts[3]))

mx = sum(X) / len(X)
my = sum(Y) / len(Y)
mz = sum(Z) / len(Z)

# write centered and scaled coordinates
with open('my.obj', 'w') as f2:
	for line in lines:
		if line[0] == 'v':
			parts = line.split()
			x = (float(parts[1]) - mx) / SCALE
			y = (float(parts[2]) - my) / SCALE
			z = (float(parts[3]) - mz) / SCALE
			f2.write('v {:.2f} {:.2f} {:.2f}\n'.format(x,y,z))
		else:
			f2.write('{}\n'.format(line))
