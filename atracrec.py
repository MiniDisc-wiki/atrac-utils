#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import timedelta
from utilities import generate_header, aea_header

def main():
    parser = ArgumentParser(description='Recover different formatted tracks from an AEA MD rip')
    parser.add_argument('--in', dest='input_file', action='store',
                        help='Input File (AEA only)', required=True)
    parser.add_argument('--prefix', dest='prefix', action='store',
                        help='Output prefix for recovered files', required=True)
    args = parser.parse_args()
    output_data = {}
    with open(args.input_file, 'rb') as input:
        track_counter = 0
        frame = 0
        current_mode = ""
        framenumber = 0
        input.seek(2048)
        while (frame := input.read(212)):
            print(f'Processing SP time {timedelta(seconds=framenumber*256/44100)}', end='\r')
            framenumber += 1
            if all(byte == 0 or byte == 0xff for byte in frame[1:211]): #Empty frame
                current_mode = ""
                continue
            if all(byte == 0 for byte in frame[1:11]): #LP mode frame
                if frame[12] >> 2 == 0x28:
                    if current_mode != "LP4":
                        print("\nNew LP4 Track detected")
                        current_mode = "LP4"
                        track_counter += 1
                        output_data[str(track_counter)] = {}
                        output_data[str(track_counter)]['type'] = 'LP4'
                        output_data[str(track_counter)]['data'] = bytearray()
                elif current_mode != "LP2":
                    print("\nNew LP2 Track detected")
                    current_mode = "LP2"
                    track_counter += 1
                    output_data[str(track_counter)] = {}
                    output_data[str(track_counter)]['type'] = 'LP2'
                    output_data[str(track_counter)]['data'] = bytearray()
                output_data[str(track_counter)]['data'] += frame[12:204]
            else: #SP Mode
                if current_mode != "SP":
                    print("\nNew SP track detected")
                    current_mode = "SP"
                    track_counter += 1
                    output_data[str(track_counter)] = {}
                    output_data[str(track_counter)]['type'] = 'SP'
                    output_data[str(track_counter)]['data'] = bytearray()
                output_data[str(track_counter)]['data'] += frame

    print('\n')
    for track, data in output_data.items():
        print(f'Writing track {track}')
        if data['type'] == 'SP': 
            extension = '.aea'
        else:
            extension = '.wav'
        with open(f'{args.prefix}{track}{extension}', mode='wb') as output:
            if data['type'] == 'SP': 
                output.write(aea_header())
            else:
                output.write(generate_header(data['type'], len(data['data'])))
            output.write(data['data'])
    print("Done!")
    


if __name__ == "__main__":
    main()