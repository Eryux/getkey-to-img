# coding: utf-8
"""
MIT License

Copyright (c) 2018 Nicolas Candia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import csv
import random
import argparse

from PIL import Image, ImageDraw, ImageFont
from hashlib import md5
from os import path


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Pick random keys in csv file and convert to an image")
    argparser.add_argument('-i', '--input', type=str, help="CSV file", required=True)
    argparser.add_argument('-s', '--savedir', type=str, help="Directory where generated images are saved", default="./")
    argparser.add_argument('-n', '--number', type=int, help="Number of key to pick", default=1)
    args = argparser.parse_args()

    # -------------------------------------------

    # Get all keys
    keys = []

    try:
        with open(args.input, 'r') as f:
            reader = csv.DictReader(f)
            keys = [row for row in reader]
    except csv.Error as e:
        print("{0} isn't correct CSV file".format(args.input))
        print("({0}): {1}".format(e.errno, e.strerror))
        exit(1)
    except IOError as e:
        print("Can't read file", args.input)
        print("({0}): {1}".format(e.errno, e.strerror))
        exit(1)
        
    # Get n random key from keys that are not already used
    available_keys = [k for k in keys if k['used'] == '0']
    if len(available_keys) < args.number:
        print("Not enough keys.")
        exit(1)

    pickup_keys = []
    for _ in range(args.number):
        pickup_keys.append(random.choice(available_keys))
        available_keys.remove(pickup_keys[len(pickup_keys)-1])

    # Mark key(s) as used
    try:
        with open(args.input, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['platform', 'game', 'key', 'used'])
            writer.writeheader()
            for row in keys:
                writer.writerow({
                    'platform':row['platform'],
                    'game':row['game'],
                    'key':row['key'],
                    'used':'1' if row in pickup_keys else row['used']
                })
    except IOError as e:
        print("Can't write file", args.input)
        print("({0}): {1}".format(e.errno, e.strerror))
        exit(1)

    # Save key(s) as image
    for key in pickup_keys:
        img = Image.new('RGB', (300,75), (255,255,255))

        draw = ImageDraw.Draw(img)
        draw.text((10,10), "{0} KEY".format(key['platform'].upper()), fill=(0,0,0), font=ImageFont.truetype(font='./fonts/oswald.ttf', size=14))
        draw.text((10,30), key['key'], fill=(0,0,0), font=ImageFont.truetype(font='./fonts/oswald.ttf', size=16))

        filename = path.join(args.savedir, "{0}.png".format(md5(key['key'].encode('utf-8')).hexdigest()))

        try:
            img.save(filename, 'PNG')
        except IOError as e:
            print("Can't save key in", filename)
            print("({0}): {1}".format(e.errno, e.strerror))
            exit(1)

        print(filename, "saved.")