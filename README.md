# semviwever: Scanning Electron Microscope Data Viwer

A three.js based web application that displays sem data in NRRD format.


# To run locally

* Run a web server locally to serve output.nrrd file

```
#install (it requires nodejs/npm)
npm install http-server -g

#run
http-server -p 3000 --cors
```

* Open semviewer.html in a browser


## Notes

* Sample NRRD header that Three.js can read

```
NRRD0004
# Complete NRRD file format specification at:
# http://teem.sourceforge.net/nrrd/format.html
type: short
dimension: 3
space: left-posterior-superior
sizes: 1000 1000 100
space directions: (0.93750000000000022,0,0) (0,-0.93750000000000022,0) (0,0,-1.5000000000000004)
kinds: domain domain domain
endian: little
encoding: ascii
space origin: (-119.53000000000002,119.53000000000007,84.000000000000028)
```
