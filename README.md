# Simple Steganography Tool


## Overview

This simple Python-based Steganography Tool was developed as a student project for a Computer Security Fundamentals course. It allows you to hide and extract text messages within images using steganography techniques. 

Steganography is the practice of concealing one message within another in such a way that it's difficult to detect. In this tool, we hide text messages within the least significant bits (LSBs) of the color channels (RGB) of image pixels.


## Features
- **Hiding Messages**: You can hide a text message of your choice within an image. The tool will encode the message, and create a steganographic version of the image.
- **Extracting Messages**: You can extract hidden messages from steganographic images. The tool will decode and reconstruct the original message.


## Usage
1. Clone this repository to your local machine:
```
git clone https://github.com/biscof/steganography-tool.git
```
2. Navigate to the project directory:
```
cd steganography-tool
```
3. Run the Python script to execute the steganography tool:
```
python steganography.py
```
4. Follow the provided instructions on the screen to hide or extract messages from images.

## Dependencies
- Python 3
- Pillow (PIL) library for image processing