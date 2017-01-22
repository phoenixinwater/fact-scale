import json
import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag.perceptron import PerceptronTagger

class Evaluator:
    def __init__(self):
        with open('lexicon.json') as data_file:
            self.lexicon = json.load(data_file)

    def Eval(self, input_string, topics):
        topics = self.nltkTopicSplit(topics)
        score = 0
        if type(topics) is list:
            for topic in topics:
                score += self.EvalOverall(input_string, topic)
                score += self.EvalPerSentence(input_string, topic)
        elif type(topics) is type("string"):
            score += self.EvalOverall(input_string, topics)
            score += self.EvalPerSentence(input_string, topics)
        return score

    def EvalOverall(self, input_string, topic):
        score = 0
        for affirmWord in self.lexicon["affirmative"]:
            key = str(list(affirmWord.keys())[0])
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(key), input_string))
            val = int(list(affirmWord.values())[0])
            score += count * val

        for negWord in self.lexicon["negative"]:
            key = str(list(negWord.keys())[0])
            count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(key), input_string))
            val = int(list(negWord.values())[0])
            score += count * val
        return score

    def IncludesDigit(self, input_string):
        return any(char.isdigit() for char in input_string)

    def EvalPerSentence(self, input_string, topic):
        score = 0
        sentenceList = sent_tokenize(input_string)
        for sentence in sentenceList:
            tmpScore = 0
            containsTopic = False
            flipConclusion = False
            words = word_tokenize(sentence)
            for word in words:
                if word.isalpha():
                    if word == topic:
                        containsTopic = True
                    else:
                        tmpScore = self.EvalOverall(word, topic)
                        if tmpScore < 0:
                            flipConclusion = True
                        if containsTopic and flipConclusion:
                            score -= tmpScore
                        elif containsTopic:
                            score += tmpScore
        return score

    def TopicSplit(self, topicInput):
        topics = []
        words = word_tokenize(topicInput)
        for word in words:
            if not word.isalpha():
                cleanWord = ""
                gotData = False
                for c in word:
                    if c.isalpha():
                        cleanWord += c
                        gotData = True
                if gotData:
                    word = cleanWord
                else:
                    continue
            skipWord = False
            for linkWord in self.lexicon["linking"]:
                if word.lower() == linkWord:
                    skipWord = True
            if not skipWord:
                topics.append(word)
        return topics

    # http://www.nltk.org/_modules/nltk/tag.html
    # http://www.nltk.org/book/ch05.html
    def nltkTopicSplit(self, topicInput):
        topics = []
        tagWords = []
        words = word_tokenize(topicInput)
        for word in words:
            if word.isalpha():
                tagWords.append(word)
        tagger = PerceptronTagger()
        for word in tagger.tag(tagWords):
            if word[1] == 'NN' or word[1] == 'NNS' or word[1] == 'VB':
                topics.append(word[0])
        return topics


if __name__ == '__main__':
    evaluator = Evaluator()
    print(evaluator.EvalOverall("true false true confirmed",""))
    print(sent_tokenize("Hello SF Python. This is NLTK."))
    print(evaluator.EvalPerSentence("The result comparing students to gorillas was found to be significant at p=.05. However, further study is still required.","gorillas"))
    print(evaluator.Eval("The result comparing students to gorillas was found to be not significant at p=.05. However, further study is still required.", "gorillas"))
    topics = evaluator.TopicSplit("Are students gorillas?")
    print(evaluator.Eval("The result comparing students to gorillas was found to be not significant at p=.05. However, further study is still required.", topics))
    print(evaluator.nltkTopicSplit("Are students gorillas?"))
