# README #
This is a web-app that is designed to skim-read abstracts and score the conclusiveness of their findings.
For example, it should give a high positive score if there are significant results for the inputted hypothesis.

However, Google Scholar is tough on robot-traffic so development is difficult.  
  
Currently, there is a lot to do on the scoring system, dealing with Google Scholar (I would like to search here since the wording used in scholarly articles follow more of a pattern than in general), 
language analysis is very simple at this point
## Dependencies ##
python3  
pip install web.py==0.40.dev0  
pip install BeautifulSoup  
pip install requests  
pip install numpy  
pip install nltk  
 -> Then go to python console:  
    -> import nltk  
    -> nltk.download()  

## How to use ##
Please be warned that Google doesn't like Google Scholar traffic so after maybe 5-10 search attempts, they will start checking for robot activity  
python server.py  
visit: http://localhost:8080/ in browser of choice  
