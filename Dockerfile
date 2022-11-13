FROM alpine:3.5 as graph-rendering

LABEL org.opencontainers.image.source https://github.com/grillbot/grillbot-docs

RUN mkdir /graphviz
RUN apk update && apk add graphviz ttf-dejavu
RUN rm -rf /var/cache/apk/*
COPY data/*.dot /graphviz/
RUN for file in $(find /graphviz -name "*.dot"); do \
    dot -Tsvg $file -o $(echo $file | cut -d'.' -f1).svg; \
    done

FROM python:3.9-alpine as flask_docs

EXPOSE 80
ENV TZ=Europe/Prague

# Configure timezones
RUN apk update && apk add tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy content
COPY . .
COPY --from=graph-rendering /graphviz/*.svg /static/

CMD [ "python3", "app.py" ]
