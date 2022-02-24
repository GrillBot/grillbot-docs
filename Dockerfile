FROM alpine:3.5 as graph-rendering

RUN mkdir /graphviz
RUN apk update && apk add graphviz ttf-dejavu
RUN rm -rf /var/cache/apk/*
COPY docs/*.dot /graphviz/
RUN for file in $(find /graphviz -name "*.dot"); do \
    dot -Tsvg $file -o $(echo $file | cut -d'.' -f1).svg; \
    done

FROM minimum/markdown-web as docs
EXPOSE 80
ENV TZ=Europe/Prague

# Configure timezones
RUN apk update && apk add tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy content to docs
COPY README.md /home/python/markdown/index.md
COPY docs/*.md /home/python/markdown/
COPY --from=graph-rendering /graphviz/*.svg /home/python/static/

# Configure pages (Menu, Footer, Variables)
COPY footer.md /tmp/
RUN for file in $(find markdown -name "*.md"); do \
    cat /tmp/footer.md >> $file; \
    sed -Ei "s/\{\{Today\}\}/$(date +'%d. %m. %Y %H:%M:%S')/g" $file; \
    sed -Ei "s/\{\{User\}\}/$(whoami)/g" $file; \
    done
RUN sed -i --regexp-extended 's/\[(.*)\]\(docs\/(.*).md\)/[\1](\/\2)/g' /home/python/markdown/index.md

# Set CSS and JS content
COPY stylesheet.css script.js /home/python/static/
# Remove temporary files
RUN rm -f /tmp/footer.md markdown/about.md
