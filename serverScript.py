from searcher import *
from evaluator import *

class EvaluationResult:
    def __init__(self, googleNumResults, scholarNumResults, googleResultList, scholarResultList, totalScore, keyUrlsScholar, keyUrlsGoogle):
        self.googleNumResults = googleNumResults
        self.scholarNumResults = scholarNumResults
        self.googleResultList = googleResultList
        self.scholarResultList = scholarResultList
        self.totalScore = totalScore
        self.keyUrlsScholar = keyUrlsScholar
        self.keyUrlsGoogle = keyUrlsGoogle

def RunEvaluation(input_string):
    evaluator = Evaluator()
    results = ResultFinder()
    crawler = PageCrawler()
    googleNumResults = results.FindResultNumGoogle(input_string)
    # Focusing on language analysis more so than working on what to do about scholar
    scholarNumResults = None # results.FindResultNumScholar(input_string)
    googleResultList = results.FindResultURLsGoogle(input_string, 1)
    scholarResultList = None # results.FindResultURLsScholar(input_string, 10)
    totalScore = 0
    keyUrlsScholar = []
    keyUrlsGoogle = [] # = googleResultList
    # for result in scholarResultList:
    #     if is_valid_url(str(result)):
    #         try:
    #             score = evaluator.Eval(crawler.CrawlAbstract(str(result)), input_string)
    #             totalScore += score
    #             if abs(score) > 100:
    #                 keyUrls.append(result)
    #         except ValueError:
    #             continue

    for result in googleResultList:
        if is_valid_url(str(result)):
            try:
                score = evaluator.Eval(crawler.CrawlArticle(str(result)), input_string)
                totalScore += score
                if abs(score) > 100:
                    keyUrlsGoogle.append(result)
            except ValueError:
                continue

    print(googleNumResults)
    print(scholarNumResults)
    print(googleResultList)
    print(scholarResultList)
    print(totalScore)
    print(keyUrlsScholar)
    print(keyUrlsGoogle)

    evaluationReturn = EvaluationResult(googleNumResults, scholarNumResults, googleResultList, scholarResultList, totalScore, keyUrlsScholar, keyUrlsGoogle)
    html = MakeHtml(evaluationReturn)
    return html

def MakeHtml(evaluation):
    returnStr = ""
    returnStr += str(evaluation.totalScore)  + "@"
    if evaluation.googleNumResults:
        returnStr += "Google search number: " + str(evaluation.googleNumResults) + "<br>"
    else:
        returnStr += "Google search unavailable<br>"
    if evaluation.scholarNumResults:
        returnStr += "Scholar search number: " + str(evaluation.scholarNumResults) + "<br>"
    else:
        returnStr += "Google Scholar search unavailable<br>"

    if evaluation.totalScore != 0:
        if evaluation.totalScore > 0:
            returnStr += "The general result was found to be FOR, with a score of:" + str(evaluation.totalScore) + "<br>"
        else:
            returnStr += "The general result was found to be AGAINST, with a score of:" + str(evaluation.totalScore) + "<br>"
    else:
        returnStr += "Evaluation unsuccessful or inconclusive :( <br>"

    if evaluation.keyUrlsGoogle:
        returnStr += "Key Google search links: <br>"
        for link in evaluation.keyUrlsGoogle:
            returnStr += '<a href="' + str(link) + '">' + str(link) + '</a><br>'
    else:
        returnStr += "Google seach links not found<br>"

    if evaluation.keyUrlsScholar:
        returnStr += "Key Google Scholar search links: <br>"
        for link in evaluation.keyUrlsScholar:
            returnStr += '<a href="' + str(link) + '">' + str(link) + '</a><br>'
    else:
        returnStr += "Google Scholar seach links not found<br>"

    return returnStr


if __name__ == '__main__':
    RunEvaluation("item")
