import argparse

import sounddevice as sd
import numpy
assert numpy
import time
import threading


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-c', '--channels', type=int, default=2,
    help='number of channels')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', type=float, help='sampling rate')
parser.add_argument('--blocksize', type=int, help='block size')
parser.add_argument('--latency', type=float, help='latency in seconds')
args = parser.parse_args(remaining)


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata
class listen(threading.Thread):
    def __init__(self,input,output):
        super().__init__()
        self.running=True
        self.inputdevice=input
        self.outputdevice=output
    def run(self):
        try:
            with sd.Stream(device=(int(self.inputdevice), int(self.outputdevice)),
                           samplerate=args.samplerate, blocksize=args.blocksize,
                           dtype=args.dtype, latency=args.latency,
                           channels=args.channels, callback=callback):
                while self.running:
                    time.sleep(0.1)
        except Exception as e:
            parser.exit(type(e).__name__ + ': ' + str(e))