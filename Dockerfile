FROM minimum/markdown-web

ENV TZ=Europe/Prague

EXPOSE 80

RUN apk update && apk add tzdata
COPY README.md /home/python/markdown/index.md
RUN sed -i --regexp-extended 's/\[(.*)\]\(docs\/(.*).md\)/[\1](\/\2)/g' /home/python/markdown/index.md
COPY footer.md /tmp/
COPY docs/*.md /home/python/markdown/
RUN for file in $(find markdown -name "*.md"); do cat /tmp/footer.md >> $file; done
RUN for file in $(find markdown -name "*.md"); do sed -Ei "s/\{\{Today\}\}/$(date +'%d. %m. %Y %H:%M:%S')/g" $file; done
RUN for file in $(find markdown -name "*.md"); do sed -Ei "s/\{\{User\}\}/$(whoami)/g" $file; done
COPY stylesheet.css /home/python/static/
RUN rm -f /tmp/footer.md markdown/about.md
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
