#!/bin/bash
pico2wave -l en-US -w temp.wav "$1"
aplay temp.wav
rm temp.wav
