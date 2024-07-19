#! /usr/bin/python



__author__ = 'Predrag Pejovic'
__license__ = 'GPLv3+'
__date__ = '2021-10-23'



from pylab import *
import usbtmc
import time
import os



################################################################################
#
# timestamp
#
################################################################################
#
def timestamp():
    t = time.localtime()
    tx = '{:04d}'.format(t.tm_year)
    tx += '-'
    tx += '{:02d}'.format(t.tm_mon)
    tx += '-'
    tx += '{:02d}'.format(t.tm_mday)
    tx += '_'
    tx += '{:02d}'.format(t.tm_hour)
    tx += '-'
    tx += '{:02d}'.format(t.tm_min)
    tx += '-'
    tx += '{:02d}'.format(t.tm_sec)
    return tx
#
################################################################################



################################################################################
#
# fname
#
################################################################################
#
def fname(filename, ts):
    fn = filename
    if ts:
        t = timestamp()
        if fn == '':
            fn = t
        else:
            fn += '_' + t
    return fn
#
################################################################################



################################################################################
#
# prikslik
#
################################################################################
#
def prikslik(slika):
    rcParams['figure.dpi'] = 600
    img = imread(slika)
    imshow(img)
    xticks(())
    yticks(())
    print()
#
################################################################################



################################################################################
#
# scope
#
################################################################################
#
class Oscilloscope(object):
    #
    def __init__(self, idVendor = 0x5345, idProduct = 0x1235, shy = False):
        try:
            self.port = usbtmc.Instrument(idVendor, idProduct)
            scopeid = self.ask('*idn?')
            if scopeid == '':
                print('cannot find oscilloscope ' + \
                'idVendor = {:4x}, idProduct = {:4x}'.format(idVendor, 
                idProduct))
            else:
                self.write('header 0')
                self.write('data:encdg ascii')
                self.shy = shy
                if not self.shy:
                    print(scopeid)
                self.ranges = array([0.002, 0.005, 0.010, 0.020, 0.050, 0.1, 
                0.2, 0.5, 1.0, 2.0, 5.0])
        except:
            print('cannot reach oscilloscope ' + \
            'idVendor = {:4x}, idProduct = {:4x}'.format(idVendor, idProduct))
    #
    def __del__(self):
        self.port.close()
    #
    def write(self, string):
        self.port.write(string)
    #
    def read(self):
        return self.port.read()
    #
    def bread(self):
        return self.port.read_raw()
    #
    def ask(self, question):
        return self.port.ask(question)
    #
    def id(self):
        return self.ask('*idn?')
    #
    #
    #
    def getwfm(self, ch, start = 1, stop = 2500):
        #
        self.write('data:start ' + str(start))
        self.write('data:stop ' + str(stop))
        #
        self.write('data:source ch' + str(ch))
        #
        self.write('curve?')
        #
        s = self.read()
        if s == '':
            return float64([])
        else:
            return float64(s.split(',')) * 0.04
    #
    #
    #
    def getsamples(self, ch, start = 1, stop = 2500):
        #
        x = self.getwfm(ch, start, stop)
        s = self.ask('ch' + str(ch) + '?').split('?')
        print(s)
        probe = float(s[0])
        scale = float(s[2])
        position = float(s[3])
        return (x - position) * scale * probe
        #return 0
    #
    #
    #
    def savesamples(self, ch, start = 1, stop = 2500, dataformat = 'npy', 
    filename = '', ts = True):
        #
        isiton = int(self.ask('select:ch' + str(ch) + '?'))
        if isiton != 1:
            print('channel', str(ch), 'is off, no action performed')
            return
        #
        if not(dataformat == 'npy' or dataformat == 'txt'):
            print('unrecognized format', dataformat, 'no action performed')
            return
        #
        x = self.getsamples(ch, start, stop)
        #
        fn = fname(filename, ts)
        #
        if dataformat == 'npy':
            np.save(fn + '.npy', x)
        else:
            np.savetxt(fn + '.txt', x)
    #
    #
    #
    def drawfig(self, filename = '', ts = True, dots = '', fmt = 'pdf'):
        #
        astatebool = bool(int(self.getstate()))
        if astatebool:
            self.stop()
        settings = ''
        #
        oneon = int(self.ask('select:ch1?'))
        if oneon == 1:
            if not self.shy:
                print('ch1 . . .')
            s1 = self.ask('ch1?').split(';')
            settings += 'CH1:\n'
            settings += 'probe = ' + s1[0] + '\n'
            settings += 'scale = ' + s1[2] + '\n'
            settings += 'position = ' + s1[3] + '\n'
            settings += 'coupling = ' + s1[4] + '\n'
            settings += 'bandwidth = ' + s1[5] + '\n\n'
            ch1 = self.getwfm(1)
        #
        twoon = int(self.ask('select:ch2?'))
        if twoon == 1:
            if not self.shy:
                print('ch2 . . .')
            s2 = self.ask('ch2?').split(';')
            settings += 'CH2:\n'
            settings += 'probe = ' + s2[0] + '\n'
            settings += 'scale = ' + s2[2] + '\n'
            settings += 'position = ' + s2[3] + '\n'
            settings += 'coupling = ' + s2[4] + '\n'
            settings += 'bandwidth = ' + s2[5] + '\n\n'
            ch2 = self.getwfm(2)
        #
        hrange = linspace(- 5, 5, 2500)
        hs = self.ask('horizontal:main:scale?')
        settings += 'HORIZONTAL:\nscale = ' + hs + '\n'
        #
        if astatebool:
            self.run()
        #
        close('all')
        figure(1, figsize = (5, 4))
        if oneon == 1:
            plot(hrange, ch1, 'y' + dots)
        if twoon == 1:
            plot(hrange, ch2, 'c' + dots)
        xlim(- 5, 5)
        ylim(- 4, 4)
        xticks(range(-5, 6), 11 * '')
        yticks(range(-4, 5), 9 * '')
        grid()
        fn = fname(filename, ts)
        savefig(fn + '.' + fmt, bbox_inches = 'tight')
        close()
        #
        sf = open(fn + '_settings.txt', 'w')
        sf.write(settings)
        sf.close()
    #
    #
    #
    def drawxy(self, filename = '', ts = True, dots = '', fmt = 'pdf'):
        #
        oneon = int(self.ask('select:ch1?'))
        twoon = int(self.ask('select:ch2?'))
        if not (oneon and twoon):
            print('both channels should be displayed, no action performed')
            return
        #
        astatebool = bool(int(self.getstate()))
        if astatebool:
            self.stop()
        settings = ''
        #
        if not self.shy:
            print('ch1 . . .')
        s1 = self.ask('ch1?').split(';')
        settings += 'CH1:\n'
        settings += 'probe = ' + s1[0] + '\n'
        settings += 'scale = ' + s1[1] + '\n'
        settings += 'position = ' + s1[2] + '\n'
        settings += 'coupling = ' + s1[3] + '\n'
        settings += 'bandwidth = ' + s1[4] + '\n\n'
        ch1 = self.getwfm(1)
        #
        if not self.shy:
            print('ch2 . . .')
        s2 = self.ask('ch2?').split(';')
        settings += 'CH2:\n'
        settings += 'probe = ' + s2[0] + '\n'
        settings += 'scale = ' + s2[1] + '\n'
        settings += 'position = ' + s2[2] + '\n'
        settings += 'coupling = ' + s2[3] + '\n'
        settings += 'bandwidth = ' + s2[4] + '\n\n'
        ch2 = self.getwfm(2)
        #
        hs = self.ask('horizontal:main:scale?')
        settings += 'HORIZONTAL:\nscale = ' + hs + '\n'
        #
        if astatebool:
            self.run()
        #
        close('all')
        figure(1, figsize = (5, 4))
        plot(ch1, ch2)
        xlim(- 5, 5)
        ylim(- 4, 4)
        xticks(range(-5, 6), 11 * '')
        yticks(range(-4, 5), 9 * '')
        grid()
        fn = fname(filename, ts)
        savefig(fn + '.' + fmt, bbox_inches = 'tight')
        close()
        #
        sf = open(fn + '_settings.txt', 'w')
        sf.write(settings)
        sf.close()
    #
    #
    #
    def getbmpraw(self):
        #
        astatebool = bool(int(self.getstate()))
        if astatebool:
            self.stop()
        self.write('hardcopy:port usb')
        self.write('hardcopy:format bmp')
        self.write('hardcopy start')
        f = self.bread()
        if astatebool:
            self.run()
        #
        return f
    #
    #
    #
    def getbmp(self, filename = '', ts = True):
        #
        f = self.getbmpraw()
        #
        fn = fname(filename, ts)
        ff = open(fn + '.bmp', 'wb')
        ff.write(f)
        ff.close()
    #
    #
    #
    def getjpg(self, filename = '', ts = True): 
        #, show = False, showname = False):
        #
        astatebool = bool(int(self.getstate()))
        if astatebool:
            self.stop()
        self.write('hardcopy:port usb')
        self.write('hardcopy:format jpeg')
        self.write('hardcopy start')
        f = self.bread()
        if astatebool:
            self.run()
        #
        fn = fname(filename, ts)
        ff = open(fn + '.jpg', 'wb')
        ff.write(f)
        ff.close()
        #
        #if show:
        #    prikslik(fn + '.jpg')
        #
        #if showname:
        #    print(fn + '.jpg')
        #
        return
    #
    #
    #
    def getpdf(self, filename = '', ts = True):
        #
        f = self.getbmpraw()
        #
        fn = fname(filename, ts)
        ff = open(fn + '.bmp', 'wb')
        ff.write(f)
        ff.close()
        #
        os.system('convert -quiet ' + fn + '.bmp ' + fn + '.pdf')
        os.remove(fn + '.bmp')
        #
        return
    #
    #
    #        
    def getpng(self, filename = '', ts = True, show = False, showname = False):
        #
        f = self.getbmpraw()
        #
        fn = fname(filename, ts)
        ff = open(fn + '.bmp', 'wb')
        ff.write(f)
        ff.close()
        #
        os.system('convert -quiet ' + fn + '.bmp ' + fn + '.png')
        os.remove(fn + '.bmp')
        #
        if show:
            prikslik(fn + '.png')
        #
        if showname:
            print(fn + '.png')
        #
        return
    #
    #
    #   
    def getstate(self):
        return self.ask('acquire:state?')
    #
    #
    #
    def run(self):
        self.write('acquire:state 1')
    #
    #
    #
    def stop(self):
        self.write('acquire:state 0')
    #
    #
    #
    def getvalue(self):
        return float(self.ask('measurement:immed:value?'))
    #
    #
    #
    def waituntilready(self):
        busy = True
        while busy:
            busy = bool(int(self.ask('busy?')))
            if not self.shy:
                print('w', )
        if not self.shy:
            print()
    #
    #
    #
    def autorange(self, ch):
        #
        self.write('ch' + str(ch) + ':position 0')
        probe = float(self.ask('ch' + str(ch) + ':probe?'))
        scale = float(self.ask('ch' + str(ch) + ':scale?'))
        normedscale = scale / probe
        scaleindex = where(self.ranges == normedscale)[0][0]
        #
        nextflag = False
        while True:
            #
            self.write('acquire:stopafter sequence')
            while self.ask('acquire:state?') == '1':
                time.sleep(0.1)
            wfm = self.getwfm(ch)
            self.write('acquire:stopafter runstop')
            self.run()
            #
            wfmmax = max(wfm)
            wfmmin = min(wfm)
            wfmextreme = max([wfmmax, - wfmmin])
            if wfmextreme > 4:
                if scaleindex == len(self.ranges) - 1:
                    # can't autorange
                    return
                else:
                    scaleindex += 1
                    self.write('ch' + str(ch) + ':scale ' + str(probe * self.ranges[scaleindex]))
                    nextflag = True
            elif nextflag:
                return
            else:            
                if scaleindex == 0:
                    # can't reduce the scale any more
                    return
                elif wfmextreme / self.ranges[scaleindex - 1] * self.ranges[scaleindex] > 4:
                    # reduction of the scale would kick the waveform out of frame
                    return
                else:
                    scaleindex -= 1
                    self.write('ch' + str(ch) + ':scale ' + str(probe * self.ranges[scaleindex]))
    #
    #
    #
    def autorangemath(self):
        #
        counter = 0
        dtautorange = 3 * self.timeframe()
        time.sleep(dtautorange)
        sold = float(self.ask('math:vertical:scale?'))
        #
        while True:
            counter += 1
            self.write('measurement:immed:type pk2pk; source math')
            self.waituntilready()
            r = self.getvalue() / 8.0
            if r > 5.0:
                s = 5.0
            else:
                s = self.ranges[where(self.ranges >= r)[0][0]]
            if s == sold or counter == 12:
                break
            self.write('math:vertical:scale ' + str(s))
            self.waituntilready()
            time.sleep(dtautorange)
            sold = s
    #
    #
    #
    def timeframe(self):
        #
        tscale = float(self.ask('horizontal:main:scale?'))
        return 10 * tscale
    #
    #
    #
################################################################################
