# tweetmh
Tweetmh's purpose is to show hourly-updated sentiment analysis for the search terms:

- mental health
- mental illness
- brain disease
- brain health

...on [twitter](http://twitter.com/).

## Running the app
In order to run the app locally, you'll need to install [Plotly Dash](https://dash.plot.ly/) and its dependencies. Once you've installed Dash and it's dependencies, you'll need to set up a database to run the dashboard from. I've used and linked to [Heroku's Postgres Database](https://elements.heroku.com/addons/heroku-postgresql) using the ''DATABASE_URL'' environment variables you can set up in the Settings pane for your Heroku app.

Run the script and wait for it to finish! Make sure to double check there's 2,000 rows in your database on Heroku by going to the addon page for your app.

```
python mh_tweets.py
```

Next, set the environment variables locally using the following line (in the terminal window that'll run the app):

```
export DATABASE_URL=URL_GOES_HERE
```

Finally, run the following line of code in your terminal:

```
python app.py
```

You should see the app running, if you don't feel free to file an issue and I'll look into it.

## Deploying the app

To deploy, you can run it locally (with the steps noted above) or on Heroku via the [instructions linked here](https://dash.plot.ly/deployment).

## Files
```
tweetmh
|   app.py
|   mh_tweets.py
|   requirements.txt
|   stop_words.txt
|   Procfile (for Heroku)
│
└───assets
│   │   main.css
│   │   gtag.js
```

## Packages Used

- `pandas`: A python package used for all things data analysis.
- `tweepy`: A python package used for querying Twitter.
- `textblob`: A python package used for determining the subjectivity and polarity of tweets
- `textstat`: A python package used for various forms of text analysis


