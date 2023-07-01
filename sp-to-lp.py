#!/usr/bin/env python3
from argparse import ArgumentParser
from utilities import generate_header

def main():
    parser = ArgumentParser(description='Decapsulate MDLP padded ATRAC3 to raw ATRAC3.')
    parser.add_argument('--in', dest='input_file', action='store',
                        help='Input File (AEA only)', required=True)
    parser.add_argument('--out', dest='output_file', action='store',
                        help='Output Filename (WAV encapsulated)', required=True)
    parser.add_argument('--mode', dest='mode', action='store', choices=['LP2', 'LP4'],
                        help='Expected codec mode', required=True)
    args = parser.parse_args()
    output_data = bytearray()
    with open(args.input_file, 'rb') as input:
        input.seek(2048) # Throw out the AEA header
        while (frame := input.read(212)):
            output_data += frame[12:204]

    with open(args.output_file, mode='wb') as output:
        output.write(generate_header(args.mode, len(output_data)))
        output.write(output_data)
    print("Done!")
    


if __name__ == "__main__":
    main()