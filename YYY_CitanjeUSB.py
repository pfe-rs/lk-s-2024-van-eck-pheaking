import usbtmc
import numpy
#from YYY_biblioteka import *


#o = Oscilloscope()
o=usbtmc.Instrument(0x5345, 0x1235)

print(o.ask(':DATA:WAVE:SCREen:CH2?'))

print(o.ask("*idn?"))

#print(o.ask('ch1:position?'))
#print(o.ask('ch2:position?'))
#o.write('ch1:position 0')
#o.write('ch2:position 0')
#o.write('ch1:scale 0.001')
#o.write('ch2:scale 0.001')
