import struct


class PacketDecoder:
    _numeric_packet_unpacker = struct.Struct('q H 9s 3B 2H 3h H 2h')
    _event_packet_unpacker = None
    _instance = None

    def __init__(self):
        if PacketDecoder._instance:
            raise Exception('This class is a singleton.')
        else:
            PacketDecoder._instance = self

    @staticmethod
    def getInstance():
        if not PacketDecoder._instance:
            PacketDecoder()
        return PacketDecoder._instance

    def decode(self, header, data):
        (PS, PL, DID, VER, PN, CH, PT) = header
        if PT == 1:
            return self.buildWaveObject(header, data)
        elif PT == 2:
            return self.buildNumericObject(header, data)
        elif PT == 3:
            return self.buildEventObject(header, data)
        else:
            return self.buildErrorObject()

    def buildWaveObject(self, header, data):
        # TODO: Implement wave object processing
        return {}

    def buildNumericObject(self, header, data):
        (PS, PL, DID, VER, PN, CH, PT) = header

        (timeStamp, SR, vessel, depth, power, sample, flags, emboliCount,
         peakV, diasV, meanV, emboliRate, x,
         x) = self._numeric_packet_unpacker.unpack(data)

        formatted_packet = {'Time': timeStamp, 'Channel': CH,
                            'VesselLabel': str(vessel), 'Depth': depth,
                            'Power': power, 'SampleRate': sample,
                            'EmboliCount': emboliCount, 'PeakVelocity': peakV,
                            'DiastolicVelocity': diasV, 'MeanVelocity': meanV,
                            'EmboliRate': emboliRate}

        return formatted_packet

    def buildEventObject(self, header, data):
        self._event_packet_unpacker = struct.Struct(str(len(data)) + 'c')
        return {
            'EventMessage:': ''.join(self._event_packet_unpacker.unpack(data))}

    def buildErrorObject(self):
        return {'error': 'Something went wrong in the TCD machine.'}
