git pull --rebase;
git push -u origin;
docker build -t ghcr.io/grillbot/grillbot-docs .
docker push ghcr.io/grillbot/grillbot-docs
