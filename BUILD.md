
How to build the interactive e-book 
===================================

This interactive e-book is written using [sphinx](https://www.sphinx-doc.org/en/master/) in [restructured text](https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html). The interactive exercises are hosted on the [inginious](https://www.inginious.org) code grading platform developed at [UCLouvain](https://www.uclouvain.be).

To build the HTML version of the e-book, you need to install several software packages :

 - sphinx itself, we assume version 2.0
 - the python3 setuptools
 - mscgen to produce some figures
 - tikz to produce other figures
 - inkscape to convert some figures
 
We use the sphinxcontrib-spelling sphinx extension to check the spelling of the text on a regular basis. This extension use PyEnchant and the enchant library.

The required packages can be installed on a Ubuntu Linux using the following commands.

```
 sudo apt-get install mscgen
 sudo apt-get install texlive-font-utils
 sudo apt-get install texlive-latex-extra
 sudo apt-get install netpbm 
 sudo apt-get install poppler-utils
 sudo apt-get install python3-enchant
 sudo apt-get install python3-sphinxcontrib.spelling
 sudo apt-get install inkscape
 sudo pip3 install -q requirements.txt

```
Here is the requirements.txt file

```
 setuptools
 sphinx>=2.0.0
 PyEnchant>=1.6.5
 sphinxcontrib-spelling

```

Once these packages are installed, you should be able to recompile the HTML version of the e-book with:

```
sphinx-build  --keep-going -b html . /tmp
```

