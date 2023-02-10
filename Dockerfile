ARG VERSION=unspecified

FROM python:3.12.0a5-alpine

ARG VERSION

LABEL maintainer="swarvingprogrammer@gmail.com"
LABEL version=$VERSION

ENV PLANKA_HOME="/home/planka"
ENV PLANKA_UTILITY_SRC="/usr/src/planka-utility"

USER root

RUN addgroup --system planka \
  && adduser --system --ingroup planka planka

RUN apk --update --no-cache add \
  bash py-pip postgresql-dev gcc python3-dev musl-dev

VOLUME ${PLANKA_HOME}

WORKDIR ${PLANKA_UTILITY_SRC}
COPY . ${PLANKA_UTILITY_SRC}

RUN pip install --no-cache-dir .
RUN chmod +x ${PLANKA_UTILITY_SRC}/var/getenv
RUN ln -snf ${PLANKA_UTILITY_SRC}/var/getenv /usr/local/bin

USER planka
WORKDIR $PLANKA_HOME
CMD ["getenv"]