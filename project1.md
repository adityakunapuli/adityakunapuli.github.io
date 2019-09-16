---
layout: page
title: Indexing Tweets
subtitle: Utilizing MapReduce to construct a TF-IDF index
---

The culmination of the Search Engine's class was a group project in which we were required to construct a working search engine on a sample dataset.  My portion of this project involved generating the dataset as well as creating the search term index.  

## [Crawler Code (GitHub)](asd)

## [MapReduce Code (GitHub)](asd)

For the dataset we chose Twitter as it offers a large and diverse corpus.  Though in retrospect, this may have been a poor choice as I ended up spending an *inordinate* amount of time just cleaning up the tweets themselves.  Every time I thought I had finally gotten the perfect set of RegEx to catch everything, a new edge case would pop up to ruin my day.  
```python
tweet_text = re.sub('(@[A-Za-z0-9_]+)|'#......................Usernames
                    '(#[0-9A-Za-z]+)|'#.......................Hashtags/topics
                    '[^\x00-\x7F]|'#..........................Emojis
                    'http[s]?\:\/\/.[a-zA-Z0-9\.\/\-]+'#......URLs
                    , ' ', raw_tweet_text)
tweet_text = re.sub('([^0-9A-Za-z \t])', '', tweet_text)#.....Non-alphabet characters
tweet_text = tweet_text.strip()
```
This issue would crop up again later when it came time to actually index the tweets.

The diagram below shows the basic architecture of my crawler.  For the sake of efficiency, we had two crawlers running with mutually exclusive geographic bounding boxes--i.e. neither crawler would capture the other's tweets.  The tweets

![alt text](../assets/code/mr/Crawler-Architecture.jpg "Twitter Crawler")


The end result was that we managed to grab over 10 million tweets for our dataset.  
