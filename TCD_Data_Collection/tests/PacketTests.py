import unittest
from PacketDecoder import PacketDecoder

class TestPackets(unittest.TestCase):
    numeric_packet_header = (42435,48,209,3,229,1,2)
    numeric_packet_data = b'\xd7\xfa\xcf4i\x01\x00\x00\x01\x00       \x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    numeric_packet_output = {'Time':1551369239255, 'Channel':1, 'VesselLabel': str(b'       \x00\x00'),'Depth':50,'Power':10, 'SampleRate':6, 'EmboliCount':0, 'PeakVelocity':0, 'DiastolicVelocity':0, 'MeanVelocity':0,'EmboliRate':0}
    
    def test_numeric_packet(self):
        packet_decoder = PacketDecoder.getInstance()
        self.assertEqual(packet_decoder.decode(self.numeric_packet_header, self.numeric_packet_data), self.numeric_packet_output)
        
