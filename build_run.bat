cd "C:\Users\DANIEL BEMERGUY\OneDrive\BBB-analysis\dockerfiles"

aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 439043003643.dkr.ecr.sa-east-1.amazonaws.com

echo What would you like to install?
echo 1 - tweet-bot
echo 2 - tweet-bot-paredao
echo 3 - tweet-bot-gather-data
echo 4 - tweet-bot-engajamento
echo 5 - tweet-bot-engajamento-plot
echo 6 - all

set /p whatapp=

if %whatapp%==1 (
    docker build -t tweet-bot .
    docker tag  tweet-bot:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest
)

else if %whatapp%==2 (
    docker build -f dockerfile_paredao -t tweet-bot-paredao .
    docker tag tweet-bot-paredao:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-paredao:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-paredao:latest
)

else if %whatapp%==3 (
    docker build -f dockerfile_gather_data -t tweet-bot-gather-data .
    docker tag tweet-bot-gather-data:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-gather-data:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-gather-data:latest
)

else if %whatapp%==4 (
    docker build -f dockerfile_engagement -t tweet-bot-engajamento .
    docker tag tweet-bot-engajamento:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento:latest
)

else if %whatapp%==5 (
    docker build -f dockerfile_engagement_plot -t tweet-bot-engajamento-plot .
    docker tag tweet-bot-engajamento-plot:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento-plot:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento-plot:latest
)

else if %whatapp%==6 (
    docker build -t tweet-bot .
    docker tag  tweet-bot:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot:latest

    docker build -f dockerfile_paredao -t tweet-bot-paredao .
    docker tag tweet-bot-paredao:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-paredao:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-paredao:latest

    docker build -f dockerfile_gather_data -t tweet-bot-gather-data .
    docker tag tweet-bot-gather-data:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-gather-data:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-gather-data:latest

    docker build -f dockerfile_engagement -t tweet-bot-engajamento .
    docker tag tweet-bot-engajamento:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento:latest

    docker build -f dockerfile_engagement_plot -t tweet-bot-engajamento-plot .
    docker tag tweet-bot-engajamento-plot:latest 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento-plot:latest
    docker push 439043003643.dkr.ecr.sa-east-1.amazonaws.com/tweet-bot-engajamento-plot:latest
)




