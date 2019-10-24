
from scipy.io.netcdf import netcdf_file
import os.path
#import math
#import numpy as np
import sys
import getopt
   
template_domains="""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <Style id="transBluePoly">
      <LineStyle>
        <width>1.5</width>
      </LineStyle>
      <PolyStyle>
        <color>7dff0000</color>
      </PolyStyle>
    </Style>
    XPLACEMARKX
  </Document>
</kml>
"""

template_placemark="""<Placemark>
        <name>XDOMAINX</name>
        <visibility>1</visibility>
        <LineString>
          <tessellate>1</tessellate>
          <coordinates>
XCOORDSX
          </coordinates>
        </LineString>
      </Placemark>"""

class Usage(Exception):
   def __init__(self, msg):
      self.msg = msg
      
def usage():
   
   print("""
Usage: python plotdomains.py


   -h or --help:     Prints this message
   -o or --output=   The name of the output file (default=domains.kml)
   -d or --ncdir=    Where the geo_em.* files are found (./)
   --step=           The space between each point to use for drawing (20)
""")
        
def main(argv=None):
   
   ncdir='.'
   step=20
   output='domains.kml'
   
   if argv is None: argv=sys.argv
   
   try:
      try:
         opts, args = getopt.getopt(argv[1:], "ho:d:",\
                                    ["help","output=","step=","ncdir="])
      except error:
             raise Usage(msg)
      # more code, unchanged
      for o,a in opts:
         if o in ('-h','--help'):
            usage()
         elif o in ('-o','--output'):
            output=a
         elif o == '--step':
            step=a
         elif o in ('-d','--ncdir'):
            ncdir=a
         else:
            assert False, "unhandled option"
  
   except err:
      print(sys.stderr, err.msg)
      print(sys.stderr, "for help use --help")
      return 2
   
   args=sys.argv   
   
   # loop through domains
   count=0
   D=1
   pstr=""
   fn=ncdir+"/geo_em.d02.nc"
   while os.path.isfile(fn):
      count+=1
      f=netcdf_file(fn,'r')
      lon=f.variables['XLONG_M'][0,:,:]
      sz=lon.shape
      lat=f.variables['XLAT_M'][0,:,:]
      S='d%02d, nlat: %03d, nlon: %03d' %(D,sz[0],sz[1])
      print("-->"+S)
      M=[]
      M.extend(zip(lon[0,::step],lat[0,::step]))
      M.extend(zip(lon[::step,-1],lat[::step,-1]))
      M.extend(zip(lon[-1,::-step],lat[-1,::-step]))
      M.extend(zip(lon[::-step,0],lat[::-step,0]))
      M.append(M[0]) # close the loop
      L="\n".join(["%.5f,%.5f" %tuple(elem) for elem in M])
      #print(L)
      a=template_placemark
      a=a.replace("XCOORDSX",L)
      a=a.replace("XDOMAINX",S)
      pstr+=a
      # next domain
      D+=1
      fn=ncdir+"/geo_em.d%02d.nc" %(D)
   
   if(count<1):
      print("No netcdf files found!")
      sys.exit()
   
   a=template_domains
   a=a.replace("XPLACEMARKX",pstr)
   fid=open(output,'w')
   fid.write(a)
   fid.close()
   
if __name__ == "__main__":
   sys.exit(main())
