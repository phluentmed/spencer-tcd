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
    def get_instance():
        if not PacketDecoder._instance:
            PacketDecoder()
        return PacketDecoder._instance

    def decode(self, header, data):
        (PS, PL, DID, VER, PN, CH, PT) = header
        if PT == 1:
            return self.build_wave_object(header, data)
        elif PT == 2:
            return self.build_numeric_object(header, data)
        elif PT == 3:
            return self.build_event_object(header, data)
        else:
            return self.build_error_object()

    def build_wave_object(self, header, data):
        # TODO: Implement wave object processing
        return {}

    def build_numeric_object(self, header, data):
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

    def build_event_object(self, header, data):
        self._event_packet_unpacker = struct.Struct(str(len(data)) + 'c')
        return {
            'EventMessage:': ''.join(self._event_packet_unpacker.unpack(data))}

    def build_error_object(self):
        return {'error': 'Something went wrong in the TCD machine.'}
