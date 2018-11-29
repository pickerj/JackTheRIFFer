#/usr/bin/python

import struct
import math
import utilities as ut

class ParsedWave(object):
    """
    Class representing the Wave data structure as defined by:
        http://soundfile.sapp.org/doc/WaveFormat/
    """
    def __init__(self, filename = None):
        """
        Method Initialize
        :param filename:
        """
        self.binary = None
        self.filename = filename
        self.chunk_id = None
        self.chunk_size = None
        self.format = None
        self.sub_chunk_1_id = None
        self.sub_chunk_1_size = None
        self.audio_format = None
        self.num_channels = None
        self.sample_rate = None
        self.byte_rate = None
        self.block_align = None
        self.bits_per_sample = None
        self.sub_chunk_2_id = None
        self.sub_chunk_2_size = None
        self.samples = [] # This represents the data section
        self.bytes_per_sample = None # Derived data
        self.length_in_seconds = None # Derived data

        if filename:
            self.parse_file(filename)


    def parse_file(self, filename):
        with open(filename,'rb') as wav:
            self.binary = wav.read()
        with open(filename, 'rb') as wav:
            self.chunk_id = wav.read(4)
            self.chunk_size = struct.unpack('<I', wav.read(4))[0]
            self.format = wav.read(4)
            self.sub_chunk_1_id = wav.read(4)
            self.sub_chunk_1_size = struct.unpack('<I', wav.read(4))[0]
            self.audio_format = struct.unpack('<H', wav.read(2))[0]
            self.num_channels = struct.unpack('<H', wav.read(2))[0]
            self.sample_rate = struct.unpack('<I', wav.read(4))[0]
            self.byte_rate = struct.unpack('<I', wav.read(4))[0]
            self.block_align = struct.unpack('<H', wav.read(2))[0]
            self.bits_per_sample = struct.unpack('<H', wav.read(2))[0]
            self.sub_chunk_2_id = wav.read(4)
            self.sub_chunk_2_size = struct.unpack('<I', wav.read(4))[0]

            self.bytes_per_sample = self.bits_per_sample / 8
            self.sample_count = int(self.sub_chunk_2_size / self.bytes_per_sample)

            for _ in range(self.sample_count):
                self.samples.append(struct.unpack('<h', wav.read(2))[0])

            self.length_in_seconds = len(self.samples) / (self.sample_rate * self.num_channels)


    def encode_data(self,byte_array):
        if type(byte_array) is not bytearray:
            print("ERROR: encoded data must be a byte array")
            return

        bits = ''.join([bin(i)[2:].zfill(8) for i in byte_array])

        # Calculate Header size
        header_size = int(math.ceil(math.log(len(self.samples),2)))
        #header_residue = header_size % 8
        #if header_residue != 0:
        #    header_residue = 8 - header_residue
        #header_size += header_residue
        max_len = len(self.samples) - header_size
        bits_len = len(bits)

        if bits_len > max_len:
            print("ERROR: the data to be encoded is too large for the current sample space")
            return

        # Write len(bits) into header as binary string
        header_bstring = bin(bits_len)[2:].zfill(header_size)
        data_bstring = header_bstring + bits

        # Write each bit into parsed samples LSB
        for i in range(0,len(data_bstring)):
            if data_bstring[i] == '0':
                if self.samples[i] < 0:
                    tmp = ut.twos_comp(self.samples[i],self.bits_per_sample)
                    tmp &= 0xFFFE
                    self.samples[i] = ut.twos_comp(tmp,self.bits_per_sample)
                else:
                    self.samples[i] &= 0xFFFE
            else:
                if self.samples[i] < 0:
                    tmp = ut.twos_comp(self.samples[i],self.bits_per_sample)
                    tmp |= 0x1
                    self.samples[i] = ut.twos_comp(tmp,self.bits_per_sample)
                else:
                    self.samples[i] |= 1


    def decode_data(self):        
        # Calculate header size
        header_size = int(math.ceil(math.log(len(self.samples), 2)))
        header_value = 0x0000
        data_bstring = bytearray()
        
        # Read LSB from first header_size samples to get size parameter
        for i in range(0, header_size):
            tmp = self.samples[i]
            if tmp < 0:
                tmp = ut.twos_comp(self.samples[i], self.bits_per_sample)
            tmp = 0x0001 & self.samples[i]
            header_value |= tmp
            header_value = header_value << 1
        header_value = header_value >> 1

        max_len = len(self.samples) - header_size
        if header_value > max_len:
            return None, 1

        # Read LSB from data section of encoded wave to extract data_bstring
        bit_count = 0;
        tmp_byte  = 0x00;
        for i in range(header_size, header_size + header_value):
            tmp = self.samples[i]
            if tmp < 0:
                tmp = ut.twos_comp(self.samples[i], self.bits_per_sample)
            tmp &= 0x0001
            tmp_byte |= tmp
            bit_count += 1
            if bit_count == 8:
                bit_count = 0
                data_bstring.append(tmp_byte)
                tmp_byte = 0x00
            tmp_byte = tmp_byte << 1
        tmp_byte = tmp_byte >> 1 
        return data_bstring, 0


    def write_to_file(self,outfile_name = None):
        if not outfile_name:
            outfile_name = self.filename + '.jack'

        print("STATUS: Writing file to {}".format(outfile_name))

        # Invert polarity
        #for i in range(0,len(self.samples)):
        #    if (self.samples[i] > 0):
        #        self.samples[i] = (self.samples[i] - 10) * -1
        #    else:
        #        self.samples[i] = (self.samples[i] + 10) * -1

        # Reverse audio
        #self.samples = self.samples[::-1]

        with open(outfile_name,'wb') as wav:
            # write first 44 bytes of header info
            for i in range(0,44):
                wav.write(self.binary[i])
            
            # write sample_count (* 2) bytes to file
            for i in range(0,self.sample_count):
                wav.write(struct.pack('<h',self.samples[i]))

            binoffset = 44 + (self.sample_count * self.bytes_per_sample)

            for i in range(binoffset,len(self.binary)):
                wav.write(self.binary[i])


    def debug(self):

        print("""
ChunkID:\t{}
ChunkSize:\t{}
Format:\t\t{}
Subchunk1ID:\t{}
Subchunk1Size:\t{}
AudioFormat:\t{}
NumChannels:\t{}
SampleRate:\t{}
ByteRate:\t{}
BlockAlign:\t{}
BitsPerSample:\t{}
Subchunk2ID:\t{}
Subchunk2Size:\t{}
SampleCount:\t{}
BytesPerSample:\t{}
AudioLength:\t{} seconds
        """.format(
        self.chunk_id,
        self.chunk_size,
        self.format,
        self.sub_chunk_1_id,
        self.sub_chunk_1_size,
        self.audio_format,
        self.num_channels,
        self.sample_rate,
        self.byte_rate,
        self.block_align,
        self.bits_per_sample,
        self.sub_chunk_2_id,
        self.sub_chunk_2_size,
        len(self.samples),
        self.bytes_per_sample,
        self.length_in_seconds))

