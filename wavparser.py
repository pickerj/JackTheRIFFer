#/usr/bin/python

import struct

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

            self.bytes_per_sample = self.bits_per_sample / 8
            self.length_in_seconds = len(self.samples) / (self.sample_rate * self.num_channels)


    def write_to_file(self):
        print("Writing file to {}.jack".format(self.filename))

        # Reverse polarity
        #for i in range(0,len(self.samples)):
        #    if (self.samples[i] > 0):
        #        self.samples[i] = (self.samples[i] - 10) * -1
        #    else:
        #        self.samples[i] = (self.samples[i] + 10) * -1

        # Reverse audio
        #self.samples = self.samples[::-1]

        with open(self.filename + '.jack','wb') as wav:
            # write first 44 bytes of header info
            for i in range(0,44):
                wav.write(self.binary[i])
            
            # write sample_count (* 2) bytes to file
            for i in range(0,self.sample_count):
                wav.write(struct.pack('<h',self.samples[i]))

            binoffset = 44 + (self.sample_count * 2)

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

