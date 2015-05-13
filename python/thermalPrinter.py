#!/usr/bin/env python 
#coding=utf-8

import serial, time, argparse

#===========================================================#
# This library is made for use with the a 701 micro thermal
# printer I bought on Aliexpress but should also work for
# those ones from Adafruit or Sparkfun (not sure about the
# character tables).
#
# Since I spent an inconsiderate time on trying to find
# a "not so chinese documentation", I eventually chose to
# work by trying and testing everything I found on the
# internet to get a pretty good result so far.
# By the way the documents stored in the "doc" folder aren't
# really related to this printer, like I said they are just
# a little help for having the most examples and data
# to work with.
# 
# This project started with the code from :
# "https://github.com/luopio/py-thermal-printer" but after
# rewriting so many details it becomes a stand-alone project.
# If you use the Raspberry Pi you can still use the original
# code since these projects and their authors aren't related
# at all.
#===========================================================#

class ThermalPrinter(object):
    SERIALPORT = '/dev/ttyUSB0'

    BAUDRATE = 9600
    TIMEOUT = 1

    # pixels with more color value (average for multiple channels) are counted as white
    # tweak this if your images appear too black or too white
    black_threshold = 48

    printer = None

    _ESC = '\x1b'                 # Oftenly used character
    _ChangeTable = _ESC + '\x74'  # String sent to change the character table
    _DefaultTable = chr(19)       # Default character table (page19), read further for more details
    _lineWidth = 384;            # Line width in pixels (for pictures)

    def __init__(self, serialport=SERIALPORT):
        self.printer = serial.Serial(serialport, self.BAUDRATE, timeout=self.TIMEOUT, bytesize=serial.EIGHTBITS, rtscts=True, dsrdtr=True)

############################################

    def initialize_printer(self, heatTime=170, heatInterval=2, heatingDots=7):  # Feel free to tweak these values according to your device (read the following lines for more details)
        self.check()
        self.reset()
        self.printer.write('\x1d\x61\x20')       # GS a 32 - Enable RTS
        self.printer.write(self._ESC + '\x37')   # ESC 7 [3 FOLLOWING VALUES] - Set parameters
        self.printer.write(chr(heatingDots))     # 0-255   Max printing dots, unit : 8dots, default : 7(64dots), actual : 7
        self.printer.write(chr(heatTime))        # 3-255   Heating time, unit : 10us, default : 80(800us), actual : 170
        self.printer.write(chr(heatInterval))    # 0-255   Heat interval, unit : 10us, default : 2(20us), actual : 2

        # Description of print density from page 23 of the manual (A2-user manual.pdf) :
        # DC2 # n Set printing density
        # Decimal: 18 35 n
        # D4..D0 of n is used to set the printing density. Density is 50% + 5% * n(D4-D0) printing density.
        # D7..D5 of n is used to set the printing break time. Break time is n(D7-D5)*250us.
        printDensity = 12 # 120% (? can go higher, text is darker but fuzzy)
        printBreakTime =  15 # 500 uS
        self.printer.write('\x12\x23')  # DC2 # [FOLLOWING LINE]
        self.printer.write(chr((printDensity << 4) | printBreakTime))

        self.printer.write('\x1c\x2e')  # FS . - Unable chinese table

        # The next command will set the characters table.
        # Since I live in france, in this case I selected the "Multilingual Latin + Euro" (page19)
        # Open your books (701print-driver-board.pdf) on page 42 and choose yours, then you should also review the "characters_conv" definition according to the set you selected.
        # Otherwise you could just add with you special character in "characters_conv" and use the same trick I did for the "Omega" sign.
        # In other words, in the "Omega" sign line, I chose to change the character set (page0 where the omega is present), then to put the character and finally to come back to the default set.
        self.printer.write(self._ChangeTable)  # Refer to the "_ChangeTable" variable  - ESC t [FOLLOWING LINE] - Set table
        self.printer.write(self._DefaultTable) # Refer to the "_DefaultTable" variable - I chose the table on page19 because of the 'Euro' sign.

        time.sleep(0.2)

        print('Printer successfully initialized')

############################################

    def reset(self):
        self.printer.write(self._ESC + '\x40')

    def check(self):
        self.printer.write(self._ESC + '\x76\x00')
        n = self.printer.inWaiting()
        data = self.printer.read(1)
        data = data + self.printer.read(n)
        if data == chr(36) :
            print('No more paper !')
        if data != chr(32) :
            self.check()

    def linefeed(self, n=1):
        line = '\x0a' * n
        self.printer.write(line)

    def justify(self, align='L'):
        pos = 0
        if align == 'L':
            pos = 0
        elif align == 'C':
            pos = 1
        elif align == 'R':
            pos = 2
        self.printer.write(self._ESC + '\x61' + chr(pos))

    def bold_off(self):
        self.printer.write(self._ESC + '\x45\x00')

    def bold_on(self):
        self.printer.write(self._ESC + '\x45\x01')

    def font_b_off(self):
        self.printer.write(self._ESC + '\x21\x00')

    def font_b_on(self):
        self.printer.write(self._ESC + '\x21\x01')

    def wide_off(self):
        self.printer.write(self._ESC + '\x14\x00')

    def wide_on(self):
        self.printer.write(self._ESC + '\x0e\x02')

    def underline_off(self):
        self.printer.write(self._ESC + '\x2d\x00')

    def underline_on(self):
        self.printer.write(self._ESC + '\x2d\x01')

    def inverse_off(self):
        self.printer.write('\x1d\x42\x00')

    def inverse_on(self):
        self.printer.write('\x1d\x42\x01')

    def upsidedown_off(self):
        self.printer.write(self._ESC + '\x7b\x00')

    def upsidedown_on(self):
        self.printer.write(self._ESC + '\x7b\x01')
        
    def barcode_chr(self, msg):
        self.printer.write(chr(29)) # Leave
        self.printer.write(chr(72)) # Leave
        self.printer.write(msg)     # Print barcode # 1:Abovebarcode 2:Below 3:Both 0:Not printed
        
    def barcode_height(self, msg):
        self.printer.write(chr(29))  # Leave
        self.printer.write(chr(104)) # Leave
        self.printer.write(msg)      # Value 1-255 Default 50
        
    def barcode_height(self):
        self.printer.write(chr(29))  # Leave
        self.printer.write(chr(119)) # Leave
        self.printer.write(chr(2))   # Value 2,3 Default 2
        
    def barcode(self, msg):
        """ Please read http://www.adafruit.com/datasheets/A2-user%20manual.pdf
            for information on how to use barcodes. """
        # CODE SYSTEM, NUMBER OF CHARACTERS        
        # 65=UPC-A    11,12    #71=CODEBAR    >1
        # 66=UPC-E    11,12    #72=CODE93    >1
        # 67=EAN13    12,13    #73=CODE128    >1
        # 68=EAN8    7,8    #74=CODE11    >1
        # 69=CODE39    >1    #75=MSI        >1
        # 70=I25        >1 EVEN NUMBER           
        length = len(msg)
        self.printer.write(chr(29))  # LEAVE
        self.printer.write(chr(107)) # LEAVE
        self.printer.write(chr(73))  # USE ABOVE CHART
        self.printer.write(chr(length))  # USE CHART NUMBER OF CHAR 
        self.printer.write(msg)
        
    def print_text(self, msg):
        msg = self.characters_conv(msg)
        self.printer.write(msg)

    def characters_conv(self, msg):
        line = msg.replace('\\B',self._ESC + '\x45\x01')        # Bold ON
        line = line.replace('\\b',self._ESC + '\x45\x00')       # Bold OFF
        line = line.replace('\\U',self._ESC + '\x2d\x01')       # Underline ON
        line = line.replace('\\u',self._ESC + '\x2d\x00')       # Underline OFF
        line = line.replace('\\S',self._ESC + '\x21\x42')       # Strike ON
        line = line.replace('\\s',self._ESC + '\x21\x00')       # Strike OFF
        line = line.replace('\\F',self._ESC + '\x21\x01')       # Font B ON
        line = line.replace('\\f',self._ESC + '\x21\x00')       # Font B OFF
        line = line.replace('\\H','\x1b\x21' + chr(16))       	# Long font ON
        line = line.replace('\\h','\x1b\x21' + chr(0))       	# Long font OFF
        line = line.replace('\\W','\x1b\x21' + chr(32))       	# Long font ON
        line = line.replace('\\w','\x1b\x21' + chr(0))       	# Long font OFF
        line = line.replace('\\G','\x1b\x21' + chr(48))       	# Great font ON
        line = line.replace('\\g','\x1b\x21' + chr(0))       	# Great font OFF
#        line = line.replace('\\W',self._ESC + '\x0e\x02')       # Wide font ON
#        line = line.replace('\\w',self._ESC + '\x14\x00')       # Wide font OFF
        line = line.replace('\\D',self._ESC + '\x7b\x01')       # Upside/down ON
        line = line.replace('\\d',self._ESC + '\x7b\x00')       # Upside/down OFF
        line = line.replace('\\I','\x1d\x42\x01')               # Colors reverse ON
        line = line.replace('\\i','\x1d\x42\x00')               # Colors reverse OFF
        line = line.replace('\\L',self._ESC + '\x61\x00')       # Align : Left
        line = line.replace('\\C',self._ESC + '\x61\x01')       # Align : Center
        line = line.replace('\\R',self._ESC + '\x61\x02')       # Align : Right
        line = line.replace('\\t','\x09')                       # Next Tab position
        line = line.replace('\\n','\x0a')                       # New line

        line = line.replace('É','\x90')
        line = line.replace('é','\x82')
        line = line.replace('È','\xd4')
        line = line.replace('è','\x8a')
        line = line.replace('Ë','\xd3')
        line = line.replace('ë','\x89')
        line = line.replace('Ê','\xd2')
        line = line.replace('ê','\x88')
        line = line.replace('Ï','\xd8')
        line = line.replace('ï','\x8b')
        line = line.replace('À','\xb7')
        line = line.replace('à','\x85')
        line = line.replace('Â','\xb6')
        line = line.replace('â','\x83')
        line = line.replace('Ô','\xe2')
        line = line.replace('ô','\x93')
        line = line.replace('Ù','\xeb')
        line = line.replace('ù','\x97')
        line = line.replace('Ç','\x80')
        line = line.replace('ç','\x87')
        line = line.replace('€','\xd5')
        line = line.replace('£','\x9c')
        line = line.replace('\\o',self._ChangeTable + chr(0) + '\xea' + self._ChangeTable + self._DefaultTable)  # Omega sign
        line = line.replace('\\m','\xe6')  # Micro sign
        line = line.replace('\\*','\x9e')  # Multiplication sign
        line = line.replace('\\14','\xac') # 1 quarter
        line = line.replace('\\12','\xab') # 1 half
        line = line.replace('\\34','\xf3') # 3 quarters
        line = line.replace('\\1','\xfb')  # power 1
        line = line.replace('\\2','\xfd')  # power 2
        line = line.replace('\\3','\xfc')  # power 3
        return line

    def print_markup(self, markup):
        """ Print text with markup for styling.

        Keyword arguments:
        markup -- text with a left column of markup as follows:
        first character denotes style (n=normal, b=bold, u=underline, i=inverse, f=font B)
        second character denotes justification (l=left, c=centre, r=right)
        third character must be a space, followed by the text of the line.
        """
        lines = markup.splitlines(True)
        for l in lines:
            style = l[0]
            justification = l[1].upper()
            text = l[3:]

            if style == 'b':
                self.bold_on()
            elif style == 'u':
               self.underline_on()
            elif style == 'i':
               self.inverse_on()
            elif style == 'f':
                self.font_b_on()
            elif style == 'n':
                self.linefeed()

            self.justify(justification)
            self.print_text(text)
            if justification != 'L':
                self.justify()

            if style == 'b':
                self.bold_off()
            elif style == 'u':
               self.underline_off()
            elif style == 'i':
               self.inverse_off()
            elif style == 'f':
                self.font_b_off()

    def convert_pixel_array_to_binary(self, pixels, w, h):
        """ Convert the pixel array into a black and white plain list of 1's and 0's
            width is enforced to 384 and padded with white if needed. """
        black_and_white_pixels = [1] * self._lineWidth * h
        if w > self._lineWidth:
            print "Bitmap width too large : %s. Needs to be under %s" % (w, self._lineWidth)
            return False
        elif w < self._lineWidth:
            print "Bitmap width under %s (%s), padding the rest with white" % (self._lineWidth, w)

        print "Bitmap size", w

        if type(pixels[0]) == int: # single channel
            print " => Printing picture"
            for i, p in enumerate(pixels):
                if p < self.black_threshold:
                    black_and_white_pixels[i % w + i / w * self._lineWidth] = 0
                else:
                    black_and_white_pixels[i % w + i / w * self._lineWidth] = 1
        else:
            print "Unsupported pixels array type."
            return False

        return black_and_white_pixels


    def print_bitmap(self, pixels, w, h, output_png=False):
        """ pixels = a pixel array. RGBA, RGB, or one channel plain list of values (ranging from 0-255).
            w = width of image
            h = height of image
            if "output_png" is set, prints an "print_bitmap_output.png" in the same folder using the same
            thresholds as the actual printing commands. Useful for seeing if there are problems with the 
            original image (this requires PIL).

            Example code with PIL:
                import Image, ImageDraw
                i = Image.open("lammas_grayscale-bw.png")
                data = list(i.getdata())
                w, h = i.size
                p.print_bitmap(data, w, h)
        """
        counter = 0
        if output_png:
            import ImageDraw
            test_img = Image.new('RGB', (self._lineWidth, h))
            draw = ImageDraw.Draw(test_img)

        black_and_white_pixels = self.convert_pixel_array_to_binary(pixels, w, h)        
        print_bytes = []

        # read the bytes into an array
        for rowStart in xrange(0, h, 256):
            chunkHeight = 255 if (h - rowStart) > 255 else h - rowStart
            print_bytes += (18, 42, chunkHeight, 48)
            for i in xrange(0, 48 * chunkHeight, 1):
                # read one byte in
                byt = 0
                for xx in xrange(8):
                    pixel_value = black_and_white_pixels[counter]
                    counter += 1
                    # check if this is black
                    if pixel_value == 0:
                        byt += 1 << (7 - xx)
                        if output_png: draw.point((counter % self._lineWidth, round(counter / self._lineWidth)), fill=(0, 0, 0))
                    # it's white
                    else:
                        if output_png: draw.point((counter % self._lineWidth, round(counter / self._lineWidth)), fill=(255, 255, 255))

                print_bytes.append(byt)
        
        # output the array all at once to the printer
        # might be better to send while printing when dealing with 
        # very large arrays...
        for b in print_bytes:
            self.printer.write(chr(b))   
        
        if output_png:
            test_print = open('print-output.png', 'wb')
            test_img.save(test_print, 'PNG')
            print "output saved to %s" % test_print.name
            test_print.close()

    def header(self):
            self.font_b_on()
            self.justify('C')
            self.print_text(time.strftime("%H:%M                           %d/%m/%Y\n"))
            self.separator(42)
            self.linefeed()

    def footer(self):
            self.linefeed()
            self.separator(42)
            self.font_b_on()
            self.justify('C')
            self.print_text(time.strftime("%H:%M                           %d/%m/%Y"))
            self.font_b_off()

    def separator(self, n=20):
            sep = '\xcd' * n
            self.font_b_on()
            self.justify('C')
            self.bold_on()
            self.print_text(sep + '\n')
            self.bold_off()
            self.font_b_off()
            self.justify('L')

    def memo(self):
            self.justify('C')
            self.bold_on()
            self.print_text('MEMO' + '\n')
            self.bold_off()

    def terminal(self):
            os.system('clear')
            print "\nHello and welcome in the live printing terminal !\n"
            i = j = False
            k = True
            while 1:
                line = raw_input('>>>> ')
                if line == '\\exit' or line == 'exit' :
                    print "\nGood bye !!!"
                    break
                elif line == '\\C' :
                    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
                             "no":"no",     "n":"no"}
                    if i == True :
                        self.linefeed()
                        i = False
                    j = True

                    while 1 :
                        cline = raw_input('\ncommand : ')
                        if cline == '\\exit' :
                            self.bold_on()
                            self.justify("C")
                            self.inverse_on()
                            self.print_text('\n\xb2\xb1\xb0Terminal session closed\xb0\xb1\xb2\n')
                            self.inverse_off()
                            self.bold_off()
                            self.print_text('at ' + time.strftime("%H:%M\n"))
                            self.justify("L")
                            break

                        elif not cline :
                            self.linefeed()

                        else :
                            output = os.popen(cline).read()
                            print output
                            done = False
                            while done == False :
                                printit = raw_input('Print it ? [Y/n] ')
                                if printit == '' :
                                    printit = 'y'
                                if printit in valid.keys():
                                    if valid[printit] == 'yes' :
                                        if k == True :
                                            self.bold_on()
                                            self.justify("C")
                                            self.inverse_on()
                                            self.print_text('\xb2\xb1\xb0Terminal session opened\xb0\xb1\xb2\n')
                                            self.inverse_off()
                                            self.bold_off()
                                            self.print_text('at ' + time.strftime("%H:%M\n"))
                                            self.justify("L")                                            
                                        self.font_b_on()
                                        if k == False :
                                            self.justify("C")                                        
                                            self.print_text(time.strftime("\n---- %H:%M ----\n"))
                                        k = False
                                        self.justify("L")
                                        self.print_text(" ")
                                        self.bold_on()
                                        self.underline_on()
                                        self.print_text('>' + cline + '\n')
                                        self.underline_off()
                                        self.bold_off()
                                        self.print_text(output)
                                        self.font_b_off()
                                    done = True
                                else:
                                    sys.stdout.write("Please respond with 'yes' or 'no' "\
                                                     "(or 'y' or 'n').\n")

                elif line > 0 :
                    if j == True :
                        self.linefeed()
                        j = False
                    self.print_text(line + '\n')
                    i = True

    def main(self):
        if args.initialize:
            self.initialize_printer()

        if args.open:
            self.header()

        if args.memo:
            self.memo()

        if args.center:
            self.justify('C')

        elif args.right:
            self.justify('R')

        else :
            self.justify('L')

        if args.text:
            tline = args.text
            if args.bold:
                self.bold_on()
            if args.wide:
                self.wide_on()
            if args.fontb:
                self.font_b_on()
            if args.underline:
                self.underline_on()
            if args.down:
                self.upsidedown_on()
            if args.inverse:
                self.inverse_on()
            self.print_text(tline + '\n')
            if args.bold:
                self.bold_off()
            if args.wide:
                self.wide_off()
            if args.fontb:
                self.font_b_off()
            if args.underline:
                self.underline_off()
            if args.down:
                self.upsidedown_off()
            if args.inverse:
                self.inverse_off()

        elif args.test:
            self.printer.write('\x12\x54')

        elif args.code:
            code = args.code
            self.barcode_chr("2")
            self.barcode(code)

        elif args.terminal:
            self.terminal()

        if args.separation:
            self.separator()
            self.linefeed()

        if args.file:
            import Image, io
            import urllib2 as urllib
            inputfile = args.file

            sock = urllib.urlopen(args.file)
            img_file = io.BytesIO(sock.read())
            sock.close()
            img = Image.open(img_file)
            w, h = img.size
            if img.size[0] > self._lineWidth:
                if h < w:
                    img = img.rotate(270)

            ratio = (self._lineWidth / float(img.size[0]))
            height = int((float(img.size[1]) * float(ratio)))
            if img.size[0] > self._lineWidth:
                img = img.resize((self._lineWidth, height), Image.ANTIALIAS)

            img = img.convert('1')
            data = list(img.getdata())
            w, h = img.size
            self.print_bitmap(data, w, h, False)

        if args.close:
            self.footer()

        if args.feed:
            self.linefeed(4)
            sys.exit()

if __name__ == '__main__':
    import sys, os, getopt, subprocess

    parser = argparse.ArgumentParser(description='Command line interface for thermal printers like those ones from Adafruit or Sparkfun.',
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=30,indent_increment = 2,width=None),
                                     version='v0.9')
    parser.add_argument("-p", "--port",
                        action="store",
                        default=ThermalPrinter.SERIALPORT,
                        help="Serial port (by default : /dev/ttyUSB0)")
    parser.add_argument("-l", "--line",
                        action="store",
                        dest="text",
                        help="Line to print")
    parser.add_argument("-t", "--terminal",
                        action="store_true",
                        help="Open a terminal")
    parser.add_argument("-m", "--memo",
                        action="store_true",
                        help="Print a memo")
    parser.add_argument("-o", "--open",
                        action="store_true",
                        help="Open ticket with header")
    parser.add_argument("-c", "--close",
                        action="store_true",
                        help="Close ticket with footer")
    parser.add_argument("-B", "--bold",
                        action="store_true",
                        help="Print bold text")
    parser.add_argument("-W", "--wide",
                        action="store_true",
                        help="Print wide text")
    parser.add_argument("-F", "--fontb",
                        action="store_true",
                        help="Use the second font")
    parser.add_argument("-U", "--underline",
                        action="store_true",
                        help="Print underlined line")
    parser.add_argument("-D", "--down",
                        action="store_true",
                        help="Print the line upside down")
    parser.add_argument("-I", "--inverse",
                        action="store_true",
                        help="Reverse black/white")
    parser.add_argument("-L", "--left",
                        action="store_true",
                        help="Align the text left")
    parser.add_argument("-C", "--center",
                        action="store_true",
                        help="Align the text in the middle")
    parser.add_argument("-R", "--right",
                        action="store_true",
                        help="Align the text right")
    parser.add_argument("-s", "--separation",
                        action="store_true",
                        help="Print separation")
    parser.add_argument("-f", "--feed",
                        action="store_true",
                        help="Feed 4 lines to align the paper for cutting")
    parser.add_argument("-8", "--code128",
                        action="store",
                        dest="code",
                        help="CODE 128")
    parser.add_argument("-u", "--url",
                        action="store",
                        dest="file",
                        help="Print a picture from an url address")
    parser.add_argument("-d", "--test",
                        action="store_true",
                        help="Print test page")
    parser.add_argument("-i", "--initialize",
                        action="store_true",
                        help="Initialize the printer (needed after power up and before the first print)")
    parser.add_argument("-z", "--debug",
                        action="store_true",
                        help="For debugging only")
    args = parser.parse_args()

    serialport = args.port
    p = ThermalPrinter(serialport=serialport)

    p.main()
