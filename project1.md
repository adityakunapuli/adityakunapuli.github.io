---
layout: page
title: Information Retrieval
subtitle: Creating a custom search engine from scratch to search through archived Tweets.
---

<style>
.myquote {
    text-align: justify;
    font-style: italic;
    padding: 5px;
    padding-left: 15px;
    padding-right: 15px;
    margin:0 auto;
    width: auto;
    display: table;
    font-size: 15px;
    background-color: #F5F5F5;
}
.tg  {border-collapse: collapse; margin-left: auto; margin-right: auto; font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;   width: 100%;}
.tg .col1{text-align: left; border: 0px white;}
.tg .col2{text-align: right; border: 0px white}
.bld{font-family: 'Arial Black', Gadget, sans-serif; font-size: 20px;}
</style>

<p class="myquote">
The culmination of the Information Retrieval class was a group project in which we were required to construct a working search engine on a sample dataset of our choice (we used Twitter).  My portion of this project involved gathering the dataset from Twitter, and generating an TF-iDF scored word index using Hadoop MapReduce. <br>
</p>

The table below contains links to the respective sections as well as the corresponding piece of code I authored.

<table class="tg">
<tr style="border-bottom: 1px solid black; border-top: 0px solid white">
  <th class="col1 bld">Section</th>
  <th class="col2 bld">Code</th>
</tr>
  <tr style="background-color: white;">
    <th class="col1"><a href="#part1">Gathering the data</a></th>
    <th class="col2"><a href="https://github.com/adik0861/adik0861.github.io/blob/master/assets/code/mr/twcrawler.py">Twitter Crawler Code (GitHub)</a></th>
  </tr>
  <tr style="background-color: white;">
  <th class="col1"><a href="#part2">Creating the index</a></th>
  <th class="col2"><a href="https://github.com/adik0861/adik0861.github.io/blob/master/assets/code/mr/mrPhase_Final.java">TF-IDF MapReduce Code (GitHub)</a></th>
  </tr>
</table>

The final output of our combined efforts yielded a search engine built using ```react.js```, and can be seen in the screenshots below.
![Search Engine Output](../assets/code/mr/Example1.png "Search Engine Output")
![Map of Results](../assets/code/mr/Example2.png "Map of Results")



# <a name="part1"></a> Part 1: Getting the data

For the dataset we chose Twitter as it offers a large and diverse corpus.  Though in retrospect, this may have been a poor choice as I ended up spending an _inordinate_ amount of time just cleaning up the tweets themselves.  Every time I thought I had finally gotten the perfect set of RegEx to catch everything, a new edge case would pop up to ruin my day.  

```python
tweet_text = re.sub('(@[A-Za-z0-9_]+)|'#......................Usernames
                    '(#[0-9A-Za-z]+)|'#.......................Hashtags/topics
                    '[^\x00-\x7F]|'#..........................Emojis
                    'http[s]?\:\/\/.[a-zA-Z0-9\.\/\-]+'#......URLs
                    , ' ', raw_tweet_text)
tweet_text = re.sub('([^0-9A-Za-z \t])', '', tweet_text)#.....Non-alphabet characters
tweet_text = tweet_text.strip()
```

This issue would crop up again later when it came time to actually index the tweets (though in a different way).  I'll go into that in the next section.

The diagram below shows the basic architecture of my crawler.  For the sake of efficiency, we had two crawlers running with mutually exclusive geographic bounding boxes--i.e. neither crawler would capture the other's tweets.  The tweets were fed into a SQLite3 database as I was still fairly paranoid about missing some CSV breaking characters with my aforementioned RegEx.

![Twitter Crawler](../assets/code/mr/Crawler-Architecture.jpg "Twitter Crawler")

The end result was that we managed to grab over 10 million tweets for our dataset.  

# <a name="part2"></a> Part 2: Creating the index

<p class="myquote">
This section proved to be one of the toughest, and most enjoyable/rewarding coding endeavors I had undertaken during my studies.  Up to this point in my career, I had used Java on a number of occasions, though I was far from proficient with it.
</p>

The foundation of any search engine is the index on which it operates, or stated another way: a search engine is only as good as its index (disregarding more advanced topics like query parsing).


<!-- Now before I launch into a description of the MapReduce job itself, I think it'd be worthwhile to cover what -->
