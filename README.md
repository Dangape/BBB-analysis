# BBB-analysis
## Install requirements

```
 pip install -r requirements.txt
```

## Authenticate the Docker CLI to your Amazon ECR registry
````angular2html
aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 439043003643.dkr.ecr.sa-east-1.amazonaws.com
````

## Build image
````angular2html
docker build -t tweet-bot .
docker run -p 9000:8080 tweet-bot
````

## Create a repository in Amazon ECR using the create-repository command.
````angular2html
aws ecr create-repository --repository-name tweet-bot --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
````

## Tag your image to match your repository name, and deploy the image to Amazon ECR using the docker push command.

````angular2html
docker tag  tweet-bot:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest
docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest
````

