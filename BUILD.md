
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

## Requirements

### Ubuntu

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
```
 
### CentOS 7

`mscgen` is not packaged by default on CentOS 7, but you can find statically-linked binaries for `mscgen` [here](http://www.mcternan.me.uk/mscgen/software/mscgen-static-0.20.tar.gz).

The other required packages can be installed on a CentOS 7 distribution using the following commands.

```
sudo yum install netpbm-progs
sudo yum install inkscape
sudo yum install poppler-utils
sudo yum install python-enchant
sudo yum install netpbm
sudo yum install ImageMagick
sudo yum install texlive texlive-latex
sudo yum install texlive-base texlive-pgf
sudo yum install texlive-collection-latex texlive-collection-latexrecommended
```

You will then also need to manually install the `pgfplots` and `standalone` texlive packages available on [CTAN](https://www.ctan.org).

* The `pgfplots` package is available [here](http://mirrors.ctan.org/install/graphics/pgf/contrib/pgfplots.tds.zip).
* The `standalone` package is available [here](http://mirrors.ctan.org/install/macros/latex/contrib/standalone.tds.zip).

### Fedora 28+

The required packages can be installed on Fedora 28+ using the following command:

```
sudo dnf install mscgen netpbm-progs inkscape poppler-utils netpbm ImageMagick texlive texlive-latex texlive-base texlive-pgf texlive-collection-latex texlive-collection-latexrecommended texlive-pgfplots textlive-standalone
```

### Python dependencies
 
 Finally, you need to install python packages using `pip3`. This can be done by running the following command :
 
```
 sudo pip3 install -q requirements.txt

```
Here is the requirements.txt file

```
 setuptools
 sphinx>=2.0.0
 PyEnchant>=1.6.5
 sphinxcontrib-spelling

```

## Building the e-book

Once the required packages are installed, you should be able to recompile the HTML version of the e-book with the following command:

```
sphinx-build --keep-going -b html . <output_dir>
```

where ``<output_dir>`` is the output directory where the e-book should be built.

### Building a localized version

If you want to build a localized version of the e-book, change the ``language`` parameter in ``conf.py`` using the ISO-639-1 code corresponding to the target language.

### Updating the localization strings

To update the localization strings, you will need to install the Python ``sphinx-intl`` package.

- First generate the ``.pot`` files by typing:
  ```
  sphinx-build -b gettext . locale/pot
  ```
- Then update the ``.po`` files by typing:
   ```
   sphinx-intl update
   ```
