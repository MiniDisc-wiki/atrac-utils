#!/usr/bin/env python3
from argparse import ArgumentParser
from utilities import generate_header, validate_header

def main():
    parser = ArgumentParser(description='Remove invalid ATRAC3 frames from a wav encapsulated LP fule')
    parser.add_argument('--in', dest='input_file', action='store',
                        help='Input File (ATRAC3 WAV only)', required=True)
    parser.add_argument('--out', dest='output_file', action='store',
                        help='Output Filename (ATRAC3 WAV only)', required=True)
    args = parser.parse_args()
    output_data = bytearray()
    with open(args.input_file, 'rb') as input:
        file_attributes = validate_header(input)
        frame_counter = 0
        while (frame := input.read(192)):
            if file_attributes['mode'] == 'LP4':
                print(f'soundunit id: {hex(frame[0] >> 2)} (byte {hex(frame[0])})')
                if frame[0] >> 2 == 0x28:
                    output_data += frame
                    print(f'Processed frame {frame_counter}')
                else:
                    print(f'Invalid frame {frame_counter}')
            frame_counter += 1
                 

    with open(args.output_file, mode='wb') as output:
        output.write(generate_header(file_attributes['mode'], len(output_data)))
        output.write(output_data)
    print("Done!")
    


if __name__ == "__main__":
    main()