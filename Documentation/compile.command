#!/bin/bash
DIR=$( cd "$( dirname "$0" )" && pwd )
cd "$DIR"
/Library/TeX/Distributions/.DefaultTeX/Contents/Programs/texbin/pdflatex 0_ReferenceManual.tex
open 0_ReferenceManual.pdf
