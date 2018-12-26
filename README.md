# getkey-to-img

Short python3 script used for randomly pick up keys from CSV file and save it to image. I used this for offering keys on Twitter during christmas.

### Requirements

* Python 3.x
* Pillow ([pip](https://pypi.org/project/Pillow/))

### Usage

Put your keys in a CSV file with row structure : platorm - game - key - used (use comma separator)

Run `python ./getkey-to-img.py -i <csv_file> [-s <destination>] [-n <number of keys>]`

```
usage: getkey-to-img.py [-h] -i INPUT [-s SAVEDIR] [-n NUMBER]

Pick random keys in csv file and convert to an image

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        CSV file
  -s SAVEDIR, --savedir SAVEDIR
                        Directory where generated images are saved
  -n NUMBER, --number NUMBER
                        Number of key to pick
```

### License

MIT License