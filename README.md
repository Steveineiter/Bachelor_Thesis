# Bachelor-thesis
Crawlers and ML for my Bachelor-thesis.

## How to run it
Install scrapy, selenium, chromedriver.
You maybe need to adapt the chromedriver path in the ```__init__``` function in the InstagramSpider.

To run it in Pycharm get configurations like this: 
![image](https://user-images.githubusercontent.com/53307237/129472345-02f5f040-1ee5-4eef-af74-6181e8f059bf.png)

To run it in Pycharm with arguments:
![image](https://user-images.githubusercontent.com/53307237/129472352-99c67a38-3634-46cd-bbb8-0287847615c1.png)

Arguments can be:
- username => The Username we want to scrape.
- is_a_company => True if the user we scrape is a company, where we want to get data, like Marry or Makava. False otherwise.
- is_a_deep_crawl => True if we want to crawl data from posts, not only the profile. Needs MUCH longer if set on True.
- path_to_useres_to_crawl_csv => If we use a CSV and the bash script for automatically scarping users, you need to pass the absolute path as argument so that the csv gets updatet after each scrape.

## Reasoning for algorithms:
### All:
Cluster size of 8: Because the mean of marry personas was 7.8 => ~8.

### MST cluster:
Weight threshold of 3: Tried other values, 3 archived best results.  

### K mean cluster:
K of 1000: More would be better but too slow  
MAX_ITER of 5: More would be better but too slow  

### Community cluster:
Threshold of 2: Tried other values, 2 archived best results.  

### New clusters interpretation:
NUMBER_OF_HASHTAGS_BASELINE of 8: Because the mena of marry personas was 7.8 => ~8 hashtags.  
NUMBER_OF_HASHTAGS_FACTOR of 1 / NUMBER_OF_HASHTAGS_BASELINE: Because it should get more reward the fewer hashtags it used. This approach is nice because of mean.  
MAXIMUM_SCORE_PER_HASHTAG of inf: "Bruteforce".  
NUMBER_OF_BEST_CLUSTERS of 6: Because Marry also uses 6 personas.  
HASHTAGS_WITH_TOO_HIGH_USAGE with ("graz", "austira", "summer"): Because other wise those values would appear in each of the best clusters.  


## Ideas
# For scaling
We can look at posts even if we are NOT logged in!! That means we could 1. get all the post urls and 2. get stuff like desciption etc. -> on the other side we dont get the name of likes.

## TODO
- Ponder: eig gibt es nur begreznte anzahl and hashtags, wir haben schon nur von insta 8000... macht es sinn mit twitter auch die personas einteilen oder waere es nid eig besser die hashtags von twitter her nehmen und shcuane ob wir jetzt mit neu gemachten personas mehr uebereinstimmungen haben?


## To clarify
- On list of followers / following we do not get all -> is it even usefull then? eg our followers since sometimes the user can be on the list sometimes not?
- We dont crawl for hashtags inside of descrption of posts, should we do that?
- Do i need liked by from our customers?
- was tun bei bildserie (zB 3 bilder?), eig brauchen wir die bilder nicht sooo dringend oder?
- Bis 25.8.2021 will ich mit Sachen von Firma fertig sein -> Moeglich? Bzw Plan machen

## Clarifyed
- Videos download / what to do with them? => einfach lassen passt schon so
- Description crawling is wrong, calrify what we need/don't need. => It is okey the way we do it atm.
- Mehrere Kleiner oder ein grosses Projekt (zb eine spider fuer marry, eine fuer menschen) => JA
- Wie wichtig ist das schoen / robust ist (wird es reused?) => Depends, wir wissen noch nid ob gebraucht wird, derweil schoen aber dynamische sachen einfach hardcoden
- Reicht alles in CSV und "normale" bilder zu speichern? Ab wievielen Daten brauchen wie DB? => JA
- Was tun mit hashtags? Nur die woerter oder wollen wir link zu jeweiligen hashtag (wie jetzt) => #WORT reicht
- Was ist der hauptfokus? Crawlen? Worauf soll ich mich fokusieren/am schoensten machen -> was ist fuer die Firma am wichtigsten => Crawling, benutzer kennen lernen, Neukundnegwinnung

## Things to improve:
