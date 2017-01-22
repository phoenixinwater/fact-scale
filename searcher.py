import requests # HTTP library # Not currently used
from bs4 import BeautifulSoup# HTTP library for data search
import sys
import urllib.request # Read HTML
import re # Regex
import random
import hashlib
from html.entities import name2codepoint

#django: http://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
def is_valid_url(url):
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

class ResultFinder:
    def CreateTopicString(self, url, topic):
        topicList = re.sub("[^\w]", " ",  topic).split()
        for i in range(0, len(topicList)):
            url += topicList[i]
            if i + 1 < len(topicList):
                url += "+"
        return url

    def GetWebPage(self, url):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        return resp.read()

    def FindResultNumGoogle(self, topic):
        googleURL = self.CreateTopicString("https://www.google.com.au/search?q=", topic)
        page = self.GetWebPage(googleURL)
        soup = BeautifulSoup(page, "html.parser")
        results = soup.find('div',{'id':'resultStats'}).text
        resultVal = ""
        beginCapture = False # Only get first section, and incorporate the commas used
        for c in str(results):
            if c.isdigit():
                if not beginCapture:
                    beginCapture = True
                resultVal += c
            elif beginCapture and c!=',':
                break

        resultVal =  int(resultVal)
        return resultVal

    def FindResultNumScholar(self, topic):
        scholarURL = self.CreateTopicString("https://scholar.google.com.au/scholar?hl=en&q=", topic)
        page = self.GetWebPage(scholarURL)
        soup = BeautifulSoup(page, "html.parser")
        soupFind = soup.find('div', {'id':'gs_ab_md'})
        if soupFind:
            results = soupFind.text
            resultVal = "";
            for c in str(results):
                if c.isdigit():
                    resultVal += c
                elif c == 'r':
                    break
            resultVal =  int(resultVal)
            return resultVal

    def FindResultURLsGoogle(self, topic, numResults):
        baseURL = self.CreateTopicString("https://www.google.com.au/search?q=", topic)
        resultList = []
        for i in range(0, numResults):
            googleURL = baseURL + "&start=" + str(i * 10)
            page = self.GetWebPage(googleURL)
            soup = BeautifulSoup(page, "html.parser")
            for cite in soup.findAll('cite'):
                resultList.append(cite.text)
        return resultList

    def FindResultURLsScholar(self, topic, numResults):
        # fake google id : https://github.com/venthur/gscholar
        rand_str = str(random.random()).encode('utf8')
        google_id = hashlib.md5(rand_str).hexdigest()[:16]
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        headers['Cookie'] = "GSP=ID=" + str(google_id) + ":CF=" + str(3)
        baseURL = self.CreateTopicString("https://scholar.google.com.au/scholar?hl=en&q=", topic)
        returnLinks = []
        for i in range(0, numResults):
            scholarURL = baseURL + "&start=" + str(i * 10)
            req = urllib.request.Request(scholarURL, headers = headers)
            resp = urllib.request.urlopen(req)
            page = resp.read()
            page = page.decode('utf8')
            soup = BeautifulSoup(page, "html.parser")
            h3Element = soup.findAll('h3', {'class' : 'gs_rt'})
            for element in h3Element:
                link = element.find('a', href=True)
                if not link:
                    continue
                elif bool(re.search("#", link['href'])):
                    continue
                else:
                    returnLinks.append(link['href'])
        return returnLinks

class PageCrawler:
    def CrawlAbstract(self, url):
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()) # http://stackoverflow.com/questions/4098702/python-urllib-urlopen-returning-302-error-even-though-page-exists. Need setting of cookies to avoid redirects sometimes
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
        try:
            page = opener.open(url)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                print("Crawler: Page not found!")
            elif err.code == 403:
                print("Crawler: Access denied!")
            else:
                print("Crawler: Something happened! Error code", err.code)
            return False
        except urllib.error.URLError as err:
            print("Crawler: Some other error happened:", err.reason)
            return False
        soup = BeautifulSoup(page, "html.parser")
        #print(soup.title)

        # Look for abstract
        results = soup.find('div', {'id':'abstract'})
        if not results:
            results = soup.find('div', {'class':'abstract'})
            if not results:
                search = soup.findAll(attrs={'class': re.compile(r".*(A|a)bstract.*")})
                if not search:
                    search = soup.findAll(attrs={'id': re.compile(r".*(A|a)bstract.*")})
                    if not search:
                        # Search for 'Abstract' - This process is incomplete and too slow atm
                        # for elem in soup(text=re.compile(r".*(A|a)bstract.*")):
                        #     print(elem.parent)

                        return None # Decoding html for text-only content not yet done

                        #print('string search')
                        # html = page.read()
                        # sHtmlArr = self.ExtractHTMLBodyText(html)
                        # save = False
                        # outStr = ""
                        # for sHtml in sHtmlArr:
                        #     start = sHtml.find('Abstract')
                        #     if start != -1:
                        #         save = True
                        #     elif len(sHtml) > 90:
                        #         save = True
                        #     if save:
                        #         outStr += sHtml
                        # if len(outStr) < 20:
                        #     return None
                        # else:
                        #     return outStr
                    else:
                        for element in search:
                            if len(str(element.text)) > 20:
                                return element.text
                else:
                    for element in search:
                        if len(str(element.text)) > 20:
                            return element.text
            else:
                return results.text
        else:
            return results.text
        return None

    def CrawlArticle(self, url):
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        page = resp.read()
        sHtmlArr = self.ExtractHTMLBodyText(page)
        outStr = ""
        for sHtml in sHtmlArr:
            if len(sHtml) > 90:
                outStr += sHtml
        return outStr

    def ExtractHTMLBodyText(self, html):
        sHtml = str(html)
        returnArr = []
        returnStr = ""
        bodyTag = False
        scriptTag = False
        inTag = False
        for i, c in enumerate(sHtml):
            if c == '<' and not bodyTag:
                if sHtml[i+1:i+5] == 'body':
                    bodyTag = True
            elif c == '<':
                if sHtml[i+1:i+6] == '/body':
                    bodyTag = False
                    if len(returnStr) > 20:
                        returnArr.append(returnStr)
                        returnStr = ""
            if bodyTag:
                if c == '<' and not scriptTag:
                    if sHtml[i+1:i+6] == 'script':
                        scriptTag = True
                elif c== '>':
                    if sHtml[i-7:i-1] == '/script':
                        scriptTag = False
                if not scriptTag:
                    if c == '<':
                        inTag = True
                        if len(returnStr) > 20:
                            returnArr.append(returnStr)
                            returnStr = ""
                    elif c == '>':
                        inTag = False
                    elif not inTag:
                        returnStr += c # Requires handling formating e.g. \n and for escape characters e.g. \'
        return returnArr


if __name__ == '__main__':
    results = ResultFinder()

    # Finding number of results and URLS
    print(results.FindResultNumGoogle("item"))
    print(results.FindResultNumScholar("item"))
    print(results.FindResultURLsGoogle("item", 1))
    # print(results.FindResultURLsScholar("social psychology", 2))

    # Looking at individual web pages for key data
    crawler = PageCrawler()
    # print(crawler.CrawlAbstract("http://www.jstor.org/stable/3765916?seq=1#page_scan_tab_contents"))
    # print(crawler.CrawlAbstract("http://psycnet.apa.org/journals/amp/40/3/266/"))
    resultList = results.FindResultURLsScholar("social psychology", 5)
    for result in resultList:
        if is_valid_url(str(result)):
            try:
                print(crawler.CrawlAbstract(str(result)))
            except ValueError:
                continue
        else:
            print("Not a valid URL")
            print(".")

    # Decoding strategies
    page = results.GetWebPage('http://randomest.blogspot.com.au/')
    print(crawler.ExtractHTMLBodyText(page))
