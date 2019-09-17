---
layout: page
title: Information Retrieval
subtitle: Creating a custom search engine from scratch to search through archived Tweets.
---

<style>
.caption {
  text-align: justify;
  padding: 5px;
  padding-left: 15px;
  padding-right: 15px;
  margin:0 auto;
  width: auto;
  display: table;
  background-color: #F5F5F5;
}
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

table.tableizer-table {
  border: 1px solid #CCC;
  width: 100%
}
.tableizer-table td {
  padding: 5px;
  margin: auto;
  border: 1px solid #CCC;
}
.tableizer-table th {
  background-color: #F5F5F5;
  color: black;
  font-weight: bold;
}
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

The final output of our combined efforts yielded a search engine built using `react.js`, and can be seen in the screenshots below.

* * *

<p class="caption">Search results of Tweets using the query "the kids basketball".</p>
![Search Engine Output](../assets/code/mr/Example1.png "Search Engine Output")

* * *

<p class="caption">Search results for query "superbowl sport" shown across a map (this only works for Tweets with associated geolocation enabled).</p>
![Map of Results](../assets/code/mr/Example2.png "Map of Results")

* * *

<p class="caption">Timeline of search results for query "hollywood california".</p>
![Timeline of Results](../assets/code/mr/Example3.png "Timeline of Results")

* * *

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

The end result was that we managed to grab over 10 million tweets for our dataset.  A sample subset is shown below.
<span style="word-break:break-all;">

<table class="tableizer-table" style="font-size: 8px;">
   <thead>
      <tr class="tableizer-firstrow">
         <th>created_at</th>
         <th>user_screen_name</th>
         <th>geolocation</th>
         <th>id_str</th>
         <th>rawtext</th>
         <th>parsedtext</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>2/11/2019 6:34</td>
         <td>NipahcAdoroare</td>
         <td>39.1022, -94.5809</td>
         <td>1094847025227620000</td>
         <td>Doing some #deepdreaming here's #kansascity - KC_Paper @ Kansas City Missouri https://t.co/2RY7nPlm1g</td>
         <td>Doing some heres KCPaper Kansas City Missouri</td>
      </tr>
      <tr>
         <td>2/11/2019 3:40</td>
         <td>agspy</td>
         <td>13.7115, 100.5815</td>
         <td>1094803453673630000</td>
         <td>I'm at Bangkok University International College (BUIC) in Khlong Toei Bangkok https://t.co/97pzh8K74m</td>
         <td>Im at Bangkok University International College BUIC in Khlong Toei Bangkok</td>
      </tr>
      <tr>
         <td>2/11/2019 6:00</td>
         <td>jav85p</td>
         <td>30.2684, -97.7362</td>
         <td>1094838612238050000</td>
         <td>Music always makes it better. alisonwonderland and her cello @ Stubb's Austin https://t.co/0pwXVMIRe1</td>
         <td>Music always makes it better alisonwonderland and her cello Stubbs Austin</td>
      </tr>
      <tr>
         <td>2/11/2019 9:59</td>
         <td>weareteamtrump</td>
         <td>25.8433, -80.4326</td>
         <td>1094898788949380000</td>
         <td>Interested in a job in Miami FL? This could be a great fit: https://t.co/SIcIVo8FXz #Trump #TeamTrump</td>
         <td>Interested in a job in Miami FL This could be a great fit</td>
      </tr>
      <tr>
         <td>2/11/2019 9:32</td>
         <td>511NYC</td>
         <td>40.7605, -74.0033</td>
         <td>1094891853005150000</td>
         <td>Cleared: Closure on #LincolnTunnel WB from New York Side - North Tube to New Jersey Side - North Tube</td>
         <td>Cleared Closure on WB from New York Side North Tube to New Jersey Side North Tube</td>
      </tr>
   </tbody>
</table>
</span>

A proper subset of 500 rows (including all columns) can [viewed here (GitHub)](https://github.com/adik0861/adik0861.github.io/blob/master/assets/code/mr/tweets_10K_subset.csv).

# <a name="part2"></a> Part 2: Creating the index

<p class="myquote">
This section proved to be one of the toughest, and most enjoyable/rewarding coding endeavors I had undertaken during my studies.  Up to this point in my career, I had used Java on a number of occasions, though I was far from proficient with it.  
</p>
<!-- The foundation of any search engine is the index on which it operates, or stated another way: a search engine is only as good as its index (disregarding more advanced topics like query parsing). -->
Before launching into technical details of the MapReduce code, I think it's worthwhile to cover the concept of Term Frequency-inverse Document Frequency (TF-iDF).  TF-iDF is the basis for our index's scoring metric, and by extension the search engine's ranking system.  In absence of scoring/ranking a search engine will default to returning *any and all* results that contain the query terms (i.e. a boolean search).  Such a system is borderline worthless when user's queries include common words such as "and" or "the".

## TF-iDF

For a query $$k$$, the term-frequency $$(tf_k)$$ can be represented as:

$$
tf_k=\\frac{f_k}{\\sum_{j=1}^{t}{f_j}}
$$

Where $$f_k$$ is the frequency of term $$k$$ in a tweet and the summation in the denominator is simply the total number of words in said tweet.

Additionally, if we have $$N$$ tweets in our collection, the inverse document frequency $$(idf_k)$$ is:

$$
i d f_k = \\log_2{\\left(\\frac{N}{n_k}\\right)}
$$

Where $$n_k$$ is the number of tweets containing term $$k$$.

The final $$\\text{TF-iDF}$$ score is computed as a product of the two:

$$
\\text{TF-iDF} = tf_k \\times idf_k
$$

## Nitty-Gritty (coding)

The goal of this portion of the project was to convert the aforementioned tweets into an index of the form:
<span style="word-break:break-all; ">
<table class="tableizer-table" style="font-size: 12px;">
<thead><tr class="tableizer-firstrow"><th>term</th><th> tweet uID</th><th> document frequency</th><th> term frequency</th><th> TF-iDF score</th></tr></thead><tbody>
 <tr><td>facebook</td><td>1094948193916200000</td><td> 7/10000</td><td> 1/24</td><td>0.131454248</td></tr>
 <tr><td>facial  </td><td>1094254820364440000</td><td>  1/10000</td><td> 1/18</td><td>0.222222222</td></tr>
</tbody></table>
</span>
An outline of the MapReduce job is shown below:
![MapReduce job for TFiDF](../assets/code/mr/mapreduce.png "MapReduce job for TFiDF")
