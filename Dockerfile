FROM minimum/markdown-web

EXPOSE 80

COPY README.md /home/python/markdown/index.md
RUN sed -Ei 's/docs\/(.*).md/\/\1/g' /home/python/markdown/index.md
COPY docs/*.md /home/python/markdown/
COPY stylesheet.css /home/python/static/
