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
  font-size: 14px;
  margin-left:auto;
  margin-right:auto;
  border: 1px solid #CCC;
  width: auto;
}
.tableizer-table td {
  text-align:center;
  padding: 5px;
  border: 1px solid #CCC;
}
.tableizer-table th {
  text-align:center;
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

<!-- The final output of our combined efforts yielded a search engine built using `react.js`, and can be seen in the screenshots below.

* * *

<p class="caption">Search results of Tweets using the query "the kids basketball".</p>
![Search Engine Output](../assets/code/mr/Example1.png "Search Engine Output")

* * *

<p class="caption">Search results for query "superbowl sport" shown across a map (this only works for Tweets with associated geolocation enabled).</p>
![Map of Results](../assets/code/mr/Example2.png "Map of Results")

* * *

<p class="caption">Timeline of search results for query "hollywood california".</p>
![Timeline of Results](../assets/code/mr/Example3.png "Timeline of Results")

* * * -->

# <a name="part1"></a> Part 1: Getting the data

For the dataset we chose Twitter as it offers a large and diverse corpus.  Though in retrospect, this may have been a poor choice as I ended up spending an _inordinate_ amount of time just cleaning up the tweets themselves.  Every time I thought I had finally gotten the perfect set of RegEx to catch everything, a new edge case would pop up to ruin my day.  

```python
                    # Usernames
tweet_text = re.sub('(@[A-Za-z0-9_]+)|'
                    # Hashtags/topics
                    '(#[0-9A-Za-z]+)|'
                    # Emojis
                    '[^\x00-\x7F]|'
                    # URLs
                    'http[s]?\:\/\/.[a-zA-Z0-9\.\/\-]+'
                    , ' ', raw_tweet_text)
                    # Non-alpha-numeric
tweet_text = re.sub('([^0-9A-Za-z \t])', '', tweet_text)
tweet_text = tweet_text.strip()
```

This issue would crop up again later when it came time to actually index the tweets (though in a different way).  I'll go into that in the next section.

The diagram below shows the basic architecture of my crawler.  For the sake of efficiency, we had two crawlers running with mutually exclusive geographic bounding boxes--i.e. neither crawler would capture the other's tweets.  The tweets were fed into a SQLite3 database as I was still fairly paranoid about missing some CSV breaking characters with my aforementioned RegEx.

![Twitter Crawler](../assets/code/mr/Crawler-Architecture.jpg "Twitter Crawler")

The end result was that we managed to grab over 10 million tweets for our dataset.  A sample subset is shown below.

<table class="tableizer-table">
   <thead>
      <tr class="tableizer-firstrow">
         <th>id_str</th>
         <th>text</th>
         <th>rawtext</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td style="word-break:normal;">1094835700699222016</td>
         <td>Yeehaw Welcome home Elder Coulson Harris Salt Lake City International Airport SLC</td>
         <td>Yee-haw!!! Welcome home Elder Coulson Harris #Texas #sanantonio #returnwithhonor @ Salt Lake City International Airport (SLC) https://t.co/UW0adG331S</td>
      </tr>
      <tr>
         <td style="word-break:normal;">1094809801878470656</td>
         <td>Thanking my Kenyan friends for keeping me warm in Seattle Seattle Washington</td>
         <td>Thanking my Kenyan friends for keeping me warm in Seattle! @OngwenMartin @ Seattle Washington https://t.co/Z0opfjxdwT</td>
      </tr>
      <tr>
         <td style="word-break:normal;">1094809820375396352</td>
         <td>I ll be o your radio tonight 10Midnight Turn the dial to Donut Bar Las Vegas</td>
         <td>I'll be o your radio tonight 10-Midnight. Turn the dial to @hot975vegas #billiondollarbeard #zeshbian @ Donut Bar Las Vegas https://t.co/6qrBcdsmHC</td>
      </tr>
   </tbody>
</table>

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
tf_k=\frac{f_k}{\sum_{j=1}^{t}{f_j}}
$$

Where $$f_k$$ is the frequency of term $$k$$ in a tweet and the summation in the denominator is simply the total number of words in said tweet.

Additionally, if we have $$N$$ tweets in our collection, the inverse document frequency $$(idf_k)$$ is:

$$
i d f_k = \log_2{\left(\frac{N}{n_k}\right)}
$$

Where $$n_k$$ is the number of tweets containing term $$k$$.

The final $$\text{TF-iDF}$$ score is computed as a product of the two:

$$
\text{TF-iDF} = tf_k \times idf_k
$$

## Nitty-Gritty (coding)

The goal of this portion of the project was to convert the Twitter dataset into an index of the form:

<table class="tableizer-table"  >
   <thead>
      <!-- <tr class="tableizer-firstrow" style="border-bottom: 2px solid #F5F5F5">
         <th> Term </th>
         <th> Tweet </th>
         <th> Doc Frequency </th>
         <th> Term Frequency </th>
         <th> Score </th>
      </tr> -->
      <tr class="tableizer-firstrow">
         <th> Term $k$ </th>
         <th> Unique ID </th>
         <th> Doc Freq. $df_k$ </th>
         <th> Term Freq. $f_k$ </th>
         <th> Score $\text{TF-iDF}$ </th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td>facebook</td>
         <td>10949481939162</td>
         <td> 7/10000</td>
         <td> 1/24</td>
         <td>0.131454248</td>
      </tr>
      <tr>
         <td>facial  </td>
         <td>109425482036444</td>
         <td>  1/10000</td>
         <td> 1/18</td>
         <td>0.222222222</td>
      </tr>
   </tbody>
</table>
An outline of the MapReduce job is shown below:
![MapReduce job for TFiDF](../assets/code/mr/mapreduce.png "MapReduce job for TFiDF")
