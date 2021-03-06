# BBB-Bot on Twitter v1.1 (22/03/2022)

## Overview

BBBot on Twitter is a personal project created just for study purpouses. The bot tweets informations about the participants from the biggest reallity show in Brazil: Big Brother Brazil (BBB).

Follow the bot on Twitter: @bbbot_bot

All the project is automated and running in AWS

## Structure
### Files

- *config.py* -> get credentials and authenticate user with Twitter API using Tweepy;  
- *app.py* -> generate WordCloud and post on Twitter;
- *gather_data.py* -> Every hour the code will scrap tweets about BBB and save the new data to a S3 bucket in AWS;
- *plot_paredao.py* -> From Sunday through Tuesday, on specific times, this code will get tweets created in the last 6 hours and generate a plot indicating who the public wants to eliminate from the tv show;
- *social_data_participantes.py* -> Every day, at 4h00 AM (America/São Paulo timezone), the code will collect data about engagement on participants' official Twitter and Instagram profiles and generate a "Social Engagement Score"
- *social_plot* -> Every day at 21h (America/São Paulo timezone) creates a plot with "Social Score" for each participant;
    - Social Score calculation is specified in the code
- *Test_files folder* -> contains codes that are currently not ready to run

## Install requirements

To get all dependencies, run:
```
 pip install -r requirements.txt
```

## Improvments for future verions
- [ ] Add sentiment analysis to social score
- [ ] Automate participants eliminations
- [ ] Predict elimination result based on recent tweets

## Changelogs
### V1.1
- Added Instagram data on social plot
- Removed wordcloud post from 16h30
- Changed social engagement calculus
- Improved hashtag treatment for rejection on Twitter
