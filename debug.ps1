docker kill grillbot-docs;
docker rm grillbot-docs;
docker build -t registry.gitlab.com/grillbot/grillbot-docs .;
docker run --name grillbot-docs -d -p 80:80 registry.gitlab.com/grillbot/grillbot-docs;
