# Bachelor-thesis documentation

## Table of contents

1. Overview
2. Instagram Scraper
    1. Important Files and Directories
    2. How to install and run it
3. Twitter Scraper
    1. Important Files and Directories
    2. How to install and run it
4. Learning From Data
    1. machine_learning
    2. new_clusters_interpretation
5. Done Data
    5. checklist
    6. personas_with_hashtags
    7. posts_data
    8. z_HTML Creator



## 1.) Overview

This documentation is focused on the Crawling part of the Bachelor-thesis as well as the representation of the data from
the first part of the bachelor thesis. Also it descibes more complicated parts for example the machine learning and
cluster interpretation. Other areas like the scripts that created the data for the first part are treated separately
with Jupyter notebooks.

There are two different crawlers:

- A instagram crawler using scrapy and selenium.
- A twitter crawler using scrapy and selenium as well for getting usernames and a scweet_crawler for getting details out
  of those profiles.

Data management has been archived via CSV files.



## 2.) Instagram Scraper

Folder instagram_scraper. This crawler is using scrapy and selenium. It is used for all purposes:

- Crawling a company.
- Crawling a user / consumer.
- Crawling for shallow data: Things we can get from the profile: Description, # Followers, # Following...
- Crawling for deep data: Things we can get from the profile (with more depth, eg. names of Followers / Following) and
  information we can get from posts: The image, descriptions, # of likes, who liked it...

This is set via the parameters ```is_a_company``` and ```is_a_deep_crawl```.

The parameter ```user_count_to_load_from_csv```is used to load x user which we would like to crawl from a given csv
file. As an example refer to the file instagram_scraper/users_to_crawl.csv.

The parameter ```is_raspberry_pi``` is used if we wish to crawl from a raspberry pi, since it needs a different version
of the chromium-browser chromedriver.

### 2.i) Important Files and Directories

In the directory instagram_scraper/instagram_scraper:

- spiders/instagram_crawler.py:
    - This file contains the crawler for Instagram. It handles the request and parsing part of the crawler.
- constants.py
    - This file is the most important to tune parameters: Eg. wait time between requests, scrolling distance, profiles
      to log in with.
- csv_handler.py
- file_manager.py
    - Handles everything in the file system except CSV files.

The other files, including items.py, middlewares.py, pipelines.py and settings.py, belong to the standard scrapy files.
Please refer to https://docs.scrapy.org/en/latest/ for further information.

The directory instagram_scraper/items contains all the crawled data. The **companies** directory contains all the
relevant data of the client and the **consumers** directory all the relevant data about the consumers.

The shell-scripts **crawl_users_from_csv.sh** and **crawl_users_from_csv_with_raspberry.sh** are a simple way to execute
the crawler.

### 2.ii) How to install and run it

Install scrapy, selenium and the chromedriver. You maybe need to adapt the chromedriver path in the ```__init__```
function in the InstagramSpider.

You can either run the **crawl_users_from_csv.sh** script or to run it in Pycharm get configurations like this:
![image](https://user-images.githubusercontent.com/53307237/129472345-02f5f040-1ee5-4eef-af74-6181e8f059bf.png)

To run it in Pycharm with arguments:
![image](https://user-images.githubusercontent.com/53307237/129472352-99c67a38-3634-46cd-bbb8-0287847615c1.png)

Arguments can be:

- username: The Username we want to scrape.
- is_a_company: True if the user we scrape is a company, where we want to get data, like Marry or Makava. False
  otherwise.
- is_a_deep_crawl: True if we want to crawl data from posts, not only the profile. Needs MUCH longer if set on True.
- path_to_useres_to_crawl_csv: If we use a CSV and the bash script for automatically scarping users, you need to pass
  the absolute path as argument so that the csv gets updatet after each scrape.



## 3.) Twitter Scraper

Folder twitter_scraper. This crawler using scrapy and selenium to get usernames / profiles and a scweet_crawler for
getting details out of those profiles.

### 3.i) Important Files and Directories

In the directory twitter_scraper/twitter_scraper:

- spiders/twitter_followers_spider.py:
    - this file contains the crawler to get the usernames of Twitter users.
    - You have to set the target Twitter side as well as your Username and the Password in **constants.py**
    - This is required to log in to Twitter, so it can search for user names in the followers section.
- constants.py:
    - This file is the most important to tune parameters: Eg. change the company to crawl, change the username /
      password to log in.

The other files, including items.py, middlewares.py, pipelines.py and settings.py, belong to the standard scrapy files.
Please refer to https://docs.scrapy.org/en/latest/ for further information.

The file twitter_scraper/scweet_crawler/scweetCrawler.py includes a simple implementation that reads usernames from a
csv file and then crawls for them using scweet. Please refer to https://github.com/Altimis/Scweet for further
information.

### 3.ii) How to install and run it

Install scrapy, selenium, chromedriver and the scweet_crawler.

The process to use the twitter_followers_spider is analogue to that of the Instagram spider.

To run it in Pycharm with arguments:

![Screenshot from 2021-11-04 15-49-35](https://user-images.githubusercontent.com/53307237/140335992-1779b723-1d10-4286-9e3f-f4c108a7bd55.png)

To run the scweet_crawler just execute the **scweetCrawler.py** file as any other python program.



## 4.) Learning From Data

The learning_from_data folder contains everything to discover new knowledge from the data we crawled. This includes 
clustering algorithms, data extractors etc. Most scripts are part of notebooks and should be quiet intuitive. This 
documentation is for the more complicated parts like the cluster generation.

### 4.i) machine_learning

Here only the cluster_analysis folder is of interest. In it there are all the clustering algorithms which are used
for this thesis. 

cluster_categorization:With the clusterCategorizer.py program we find out the likelihood of a cluster to predefined 
personas. Those personas were defined from the marketing team of Marry Ice Tea. For that we are using hashtags the
user has used and hashtags which the personas should use. 
- Input: A csv file with format cluster name | hashtags. See 
/learning_from_data/machine_learning/cluster_analysis/cluster_categorization/levenshtein_clusters.csv as example.
- Output: A file stating how likely the cluster is to each predefined persona.

enrica_cluster: named after Enrica because she had the idea for this cluster. Basically a social network clustering 
approach, but with fine-tuning like max clusters. In a nutshell it is creating a graph if hashtags were used together.
After creating the graph edges with weight less than a threshold are getting dropped, resulting in clusters. 
This cluster performed best.
- Input: a csv file with the categorization of personas. See /learning_from_data/machine_learning/cluster_analysis/
enrica_cluster/persona_categorization.csv as example.
- Output: a csv file with different cluster with format cluster name | hashtags.

k_mean_clustering: a normal k mean clustering algorithm. As metric for the euclidean distance the levenshtein distance 
of the hashtags where used. This cluster performed poorly, since there were many clusters with too many hashtags and 
some with too little. 
- Input: A csv with hashtags. See /learning_from_data/machine_learning/cluster_analysis/k_mean_clustering/
used_hashtags_all.csv as example. 
- Output: a csv file with different cluster with format cluster name | centroid | hashtags.

levenshtein_cluster: in the end it is pretty similar to the enrica cluster, but with the difference that the weights
of the edges are the levenshtein distance to each word. Since this results in a fully connected graph the runtime 
was not possible on my machine if used with all hashtags. That's why only the most used 1500 hashtags are passed as
parameter. After that we build a kruskal mst and again remove edges which are higher than a given threshold.
- Input: A csv with hashtags. See learning_from_data/machine_learning/cluster_analysis/leveshtein_cluster/
used_hashtags.csv as example. 
- Output: a csv file with different cluster with format cluster name | hashtags.

networkx_community_cluster: an implementation with the networkx framework. Unfortunately it had a similar weakness as 
the k mean clustering which is that it created just a couple clusters with way too many hashtags.
- Input: A csv with hashtags. See learning_from_data/machine_learning/cluster_analysis/networkx_community_cluster/
persona_categorization.csv as example. 
- Output: a csv file with different cluster with format cluster name | hashtags | silhouette score. Where the silhouette
score is a metric to determine the quality of clusters. 

### 4.ii) new_clusters_interpretation

persona_interpreter.py: with this program we calculate the performance of all the clusters. There are couple constants
to tweak, here a reasoning why we choose them as they are right now:

NUMBER_OF_HASHTAGS_BASELINE of 8: Because the mena of marry personas was 7.8 => ~8 hashtags.  
NUMBER_OF_HASHTAGS_FACTOR of 1 / NUMBER_OF_HASHTAGS_BASELINE: Because it should get more reward the fewer hashtags it used. This approach is nice because of mean.  
MAXIMUM_SCORE_PER_HASHTAG of inf: "Bruteforce".  
NUMBER_OF_BEST_CLUSTERS of 6: Because Marry also uses 6 personas.  
HASHTAGS_WITH_TOO_HIGH_USAGE with ("graz", "austira", "summer"): Because other wise those values would appear in each of the best clusters.  

In the end this program calculates how well each cluster performs on the used hashtags given.
- Input: csv files of community_clustering, k_mean_clustering, mst_clustering (aka levenshtein clustering) and the used
hashtags. Please refer to the learning_from_data/new_clusters_interpretation/data folder.
- Output: 



## 5.) Done Data

The folder done_data contains the representation of the first part of the bachelor thesis which are mainly the posts of
Marry Icetea as well as user data. The most important files in those folders are the html files, which are the
representation of our data.

### 5.i) checklist

Shows all users with the amount of liked posts and an URL to each post they liked.

### 5.ii) personas_with_hashtags

- persona_categorization: Shows all users with the likelyhood that they are one of the personas Marry has defined
  together with the hashtags they have used.
- used_hashtags: Shows all hashtags that the users have used, together with the number how often it got used and an
  checkmark if it already is getting used in any of Marry's defined personas.

### 5.iii) posts_data

Shows all the data of an post we have collected.

### 5.iv) z_HTML Creator

- csv_with_images: Is used to create a HTML document out of a CSV file and images for each row in the CSV file.
- normal_csv: Is used to create a HTML document out of a CSV file.










