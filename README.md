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


## Ideas

## TODO
- Ist es zu auffaellig das ich mich jedes mal neu einlogge nach einem crawl?
- Crawler schwerer zu entdecken machen

## To clarify
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
