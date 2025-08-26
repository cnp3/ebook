FROM ubuntu:24.04 AS build

WORKDIR /workspace

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    mscgen \
    texlive-font-utils \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-science \
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

# Install imagemagick (https://stackoverflow.com/questions/74951619/how-to-install-imagemagick-7-on-ubuntu-image)
RUN apt-get install -y wget autoconf pkg-config build-essential curl libpng-dev
RUN wget https://github.com/ImageMagick/ImageMagick/archive/refs/tags/7.1.0-31.tar.gz && \
    tar xzf 7.1.0-31.tar.gz && \
    rm 7.1.0-31.tar.gz && \
    apt-get clean && \
    apt-get autoremove
RUN sh ./ImageMagick-7.1.0-31/configure --prefix=/usr/local --with-bzlib=yes --with-fontconfig=yes --with-freetype=yes --with-gslib=yes --with-gvc=yes --with-jpeg=yes --with-jp2=yes --with-png=yes --with-tiff=yes --with-xml=yes --with-gs-font-dir=yes && \
    make -j && make install && ldconfig /usr/local/lib/

RUN git clone https://github.com/obonaventure/mscgen.git
RUN git clone https://github.com/sphinx-contrib/tikz

RUN python3 -m venv .

SHELL ["/bin/bash", "-c"]

COPY requirements.txt .

RUN . ./bin/activate && pip install -r requirements.txt

COPY ./ /repo/

# Regenerate imgs
RUN cd /repo/pkt && rm *.pdf && rm *.png
RUN cd /repo/pkt && make

ARG CHECK_SPELLING="Y"

# Don't run with --fail-on-warning here to only check for spelling mistakes first
# Grep exit with 0 if it finds anything, here we don't want to find any spelling mistake, this why we have the !
RUN . ./bin/activate && cd /repo && \
    bash -c "if [ $CHECK_SPELLING == Y ]; then \
        ! sphinx-build --keep-going -b spelling . /out | grep 'Spell check:'; \
    fi"
    
RUN . ./bin/activate && cd /repo && sphinx-build --keep-going -b html . /out
RUN . ./bin/activate && cd /repo && sphinx-build --keep-going -b epub . /out
RUN . ./bin/activate && cd /repo && sphinx-build -M latexpdf . /out

FROM scratch AS export
COPY --from=build /out .
