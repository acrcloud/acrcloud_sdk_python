FROM alpine:latest

MAINTAINER ACRCloud

RUN apk update \
        && apk upgrade \
        && apk add --no-cache bash \
        bash-doc \
        bash-completion \
        libstdc++ \
        libstdc++.so.6 \
        python2 \
        python3 \
        && rm -rf /var/cache/apk/* \
        && /bin/bash
