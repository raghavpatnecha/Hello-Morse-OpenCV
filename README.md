# Morse Code Computer Vision

## What is Morse Code
Morse Code encodes the ISO basic Latin alphabet, some extra Latin letters, the Arabic numerals and a small set of punctuation and procedural signals (prosigns) as standardized sequences of short and long signals called "dots" and "dashes", or "dits" and "dahs", as in amateur radio practice.

## Inspiration

Inspired from Google's Experiment about how they used morse code to help differently abled people to communicate efficiently. We decided to implement morse code translator using computer vision which isn't that better but a cheaper option. 

## Working

This project translates morse code in plain english. We used webcam to read blinking of the eyes as dots and dashes which then with the use of a dictionary converts morse to english.

File `morse_converter.py` contains the python dictionary. For reference we have also included the Poster Cards to learn Morse better.

`Short Blink : Dot ' . '`

`Long Blink : Dash ' - '`

`Long Long Blink : Removes the last dot or dash`

# Requirements

[OpenCv](https://pypi.org/project/opencv-python/)

[imutils](https://github.com/jrosebr1/imutils)

[dlib](https://pypi.org/project/dlib/)

[Scipy](https://www.scipy.org/)

