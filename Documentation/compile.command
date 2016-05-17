#!/bin/bash
DIR=$( cd "$( dirname "$0" )" && pwd )
cd "$DIR"
/Library/TeX/Distributions/.DefaultTeX/Contents/Programs/texbin/pdflatex ReferenceGuide.tex
open ReferenceGuide.pdf
