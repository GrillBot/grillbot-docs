FROM alpine AS d2-rendering

RUN mkdir /d2
RUN apk update && apk add ttf-dejavu curl make
RUN curl -fsSL https://d2lang.com/install.sh | sh -s --
RUN rm -rf /var/cache/apk/*
COPY data/*.d2 /d2/
RUN for file in $(find /d2 -name "*.d2"); do \
    d2 $file $(echo $file | cut -d'.' -f1).svg; \
    done

FROM python:alpine AS flask_docs

EXPOSE 80
ENV TZ=Europe/Prague
LABEL org.opencontainers.image.source=https://github.com/grillbot/grillbot-docs
LABEL org.opencontainers.image.licenses=MIT

# Configure timezones
RUN apk update && apk add tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy content
COPY . .
COPY --from=d2-rendering /d2/*.svg /static

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/health || exit 1

CMD [ "gunicorn", "-c", "gunicorn.conf.py", "app:app" ]
