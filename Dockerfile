FROM ubuntu:24.04 AS build

WORKDIR /workspace

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mscgen \
    texlive-font-utils \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-plain-generic \
    latexmk \
    netpbm \
    poppler-utils \
    python3-enchant \
    python3-sphinxcontrib.spelling \
    inkscape \
    fonts-dejavu-core \
    python3-venv \
    git

RUN git clone https://github.com/obonaventure/mscgen.git
RUN git clone https://github.com/sphinx-contrib/tikz

RUN python3 -m venv .

SHELL ["/bin/bash", "-c"]

RUN . ./bin/activate && pip3 install -r <(echo -e '\
    setuptools\n\
    sphinx>=2.0.0\n\
    PyEnchant>=1.6.5\n\
    sphinxcontrib-spelling\n\
    sphinx-book-theme\n\
    sphinx-intl')

RUN . ./bin/activate && pip3 install -e mscgen
RUN . ./bin/activate && pip3 install -U -e tikz

COPY ./ /repo/

# Don't run with --fail-on-warning here to only check for spelling mistakes first
# Grep exit with 0 if it finds anything, here we don't want to find any spelling mistake, this why we have the !
RUN . ./bin/activate && cd /repo && ! sphinx-build --keep-going -b spelling . /out | grep "Spell check:"
RUN . ./bin/activate && cd /repo && sphinx-build --keep-going -b html . /out
RUN . ./bin/activate && cd /repo && sphinx-build --keep-going -b epub . /out
RUN . ./bin/activate && cd /repo && sphinx-build -M latexpdf . /out

FROM scratch AS export
COPY --from=build /out .
