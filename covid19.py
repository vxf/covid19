#!/usr/bin/env python3

import argparse
import os

from fetch import (
    get_attributes,
    get_attribute_header,
    get_attribute_data
)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Get Portugal covid-19 stats')
    parser.add_argument('command', metavar='command', type=str, help='Commands (list|csv|plot)')
    parser.add_argument('--attribute', help='--attribute casosnovos')
    parser.add_argument('--plot_file', help='--plot_file mychart.png')

    return parser.parse_args()

if __name__== "__main__":
    args = parse_arguments()

    if args.command == 'list':
        for alias, name in get_attributes():
            print('{}: {}'.format(alias, name))

    elif args.command == 'csv':
        header = get_attribute_header(args.attribute)
        print('{},{}'.format(*header))

        for timestamp, value in get_attribute_data(args.attribute):
            print('{},{}'.format(timestamp, value))

    elif args.command == 'plot':
        from forecast import plot

        data = list(get_attribute_data('casosconfirmados'))

        plot('Casos confirmados', 'casosconfirmados', data, args.plot_file)
