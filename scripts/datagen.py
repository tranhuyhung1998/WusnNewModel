import os
import sys
sys.path.append('.')

from argparse import ArgumentParser


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-o', '--output', default='data/small_data')
    parser.add_argument('-W', type=int, default=200)
    parser.add_argument('-H', type=int, default=200)
    parser.add_argument('-n', '--count', type=int, default=5)
    parser.add_argument('--depth', type=float, default=1)
    parser.add_argument('--height', type=float, default=10)
    parser.add_argument('--ns', '--num-sensor', type=int, default=40)
    parser.add_argument('--nr', '--num-relay', type=int, default=40)
    parser.add_argument('--radius', default='25,30,35,40,45,50')
    parser.add_argument('--prefix', default='dem-')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)

    
