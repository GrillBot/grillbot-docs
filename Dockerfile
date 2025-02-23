FROM alpine:3.21.3 AS d2-rendering

RUN mkdir /d2
RUN apk update && apk add ttf-dejavu curl make
RUN curl -fsSL https://d2lang.com/install.sh | sh -s --
RUN rm -rf /var/cache/apk/*
COPY data/*.d2 /d2/
RUN for file in $(find /d2 -name "*.d2"); do \
    d2 $file $(echo $file | cut -d'.' -f1).svg; \
    done

FROM python:3.14.0a5-alpine AS flask_docs

EXPOSE 80
ENV TZ=Europe/Prague
LABEL org.opencontainers.image.source=https://github.com/grillbot/grillbot-docs

# Configure timezones
RUN apk update && apk add tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy content
COPY . .
COPY --from=d2-rendering /d2/*.svg /static

CMD [ "python3", "app.py" ]
