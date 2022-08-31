git pull --rebase;
git push;
docker build -t registry.gitlab.com/grillbot/grillbot-docs .
docker push registry.gitlab.com/grillbot/grillbot-docs
