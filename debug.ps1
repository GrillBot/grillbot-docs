docker kill grillbot-docs;
docker rm grillbot-docs;
docker build -t ghcr.io/grillbot/grillbot-docs .;
docker run --name grillbot-docs -d -p 80:80 ghcr.io/grillbot/grillbot-docs;
