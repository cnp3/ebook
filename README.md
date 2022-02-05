
Computer Networking : Principles, Protocols and Practice, 3rd Edition
=====================================================================

[![Build Status](https://travis-ci.org/cnp3/ebook.svg?branch=master)](https://travis-ci.org/cnp3/ebook)
[![Translation Status](https://weblate.info.ucl.ac.be/widgets/cnp3-ebook/-/svg-badge.svg)](https://weblate.info.ucl.ac.be/engage/cnp3-ebook/?utm_source=widget)

This is the current version of the third edition of the [Computer Networking : Principles, Protocols and Practice](https://www.computer-networking.info) open-source ebook. 

(c) Olivier Bonaventure, UCLouvain, Belgium
    https://perso.uclouvain.be/olivier.bonaventure

All the files in this subversion repository are licensed under a Creative Commons Attribution-Share Alike 3.0 Unported License.

You can find the source files for the two previous editions and their history on https://github.com/obonaventure/cnp3

You can access a build of the interactive e-book through http://beta.computer-networking.info


See [BUILD.md](BUILD.md) if you want to build the e-book yourself.

 
How to contribute
-----------------

Contributions to the e-book are more than welcome. We welcome contributions with new or improved text, new or improved figures, new open exercises, new multiple choice questions, ... Here are a few guidelines to help you prepare your contributions to the e-book.

### Updating existing sections

This is the simplest way to contribute. If you spot a small error, a typo or would like to clarify a few sentences, feel free to update the text directly on github and create a pull request. When doing so, remember that there are a few guidelines that we try to follow:

 - We use American English spelling. There are automated travis tests that will automatically verify that your pull-request passes the spell check. If not, update your pull request. If you introduce a new word that is not recognized by the standard directory, you can either add it as a spelling directive in the file where is appears (see e.g. the bottom of the `bibliography.rst` file) or include it in the `wordlist.dict` file which contains the new words that are used in different files.
 - When citing references, please update the file `bibliography.rst`. Please use the same style as the one used in the file and add an hyperlink to the paper title that points to a stable URL, e.g. a DOI
 - Make sure that your update builds correctly using sphinx. There are now github actions that check the spelling and then build the pdf, epub and HTML versions of the ebook automatically. 

### Proposing new sections

If you would like to add several sections or chapters to recover some topics that are important and are missing from the e-book, please start a discussion on the [cnp3 mailing list](https://sympa-2.sipr.ucl.ac.be/sympa/info/cnp3). The e-book evolves over time and we sometime remove sections/chapters as the networking technology evolves. We do not attempt at covering all possible networking technologies.

### Updating figures

There is unfortunately some diversity among the figures of the e-book. Some have been drawn using powerpoint, other were drawn using inkscape. If you plan to draw new figures, please try to use tikz or mscgen if possible. Thanks to [sphinxcontrib-tikz](https://sphinxcontrib-tikz.readthedocs.io/en/latest/) and [sphinxcontrib-mscgen](https://github.com/sphinx-contrib/mscgen), these figures are written directly in the text, which makes it easier to update them than using graphical drawing tools. 

### Proposing new translations

If you would like to make the e-book available in a language you are fluent in, please first introduce you by starting a discussion on the [cnp3 mailing list](https://sympa-2.sipr.ucl.ac.be/sympa/info/cnp3). Then, register on [Weblate](https://weblate.info.ucl.ac.be/engage/cnp3-ebook/) to start translating. The translations are made paragraph per paragraph and can be done collaboratively. They are periodically pushed into the repository via a pull-request.
