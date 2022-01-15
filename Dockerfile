FROM minimum/markdown-web

EXPOSE 80
ENV TZ=Europe/Prague

# Configure timezones
RUN apk update && apk add tzdata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy content to docs
COPY README.md /home/python/markdown/index.md
COPY docs/*.md /home/python/markdown/

# Configure pages (Menu, Footer, Variables)
COPY footer.md /tmp/
RUN for file in $(find markdown -name "*.md"); do cat /tmp/footer.md >> $file; done
RUN for file in $(find markdown -name "*.md"); do sed -Ei "s/\{\{Today\}\}/$(date +'%d. %m. %Y %H:%M:%S')/g" $file; done
RUN for file in $(find markdown -name "*.md"); do sed -Ei "s/\{\{User\}\}/$(whoami)/g" $file; done
RUN sed -i --regexp-extended 's/\[(.*)\]\(docs\/(.*).md\)/[\1](\/\2)/g' /home/python/markdown/index.md

# Set CSS and JS content
COPY stylesheet.css script.js /home/python/static/
# Remove temporary files
RUN rm -f /tmp/footer.md markdown/about.md
