# coding=utf-8
from collections import Counter
import sys

class PosTaggingBrills:
    currentTags = []
    correctTags = []
    Tags = set()
    countWordTag = {}
    PrevCurrTagCount = {}
    CountTags = {}
    def calculateError(self,sentTag1, sentTag2):
        errortags = 0
        i=0
        while i<(len(sentTag1) - 1):
            if sentTag1[i][1] != sentTag2[i][1]:
                errortags += 1
        return (float(errortags) / float(len(sentTag1)))

    def PosTagModel(self,corpusfile):
        
        cfile = open(corpusfile, 'r')
        data = cfile.read()
        word_tags = data.split()
        prev_Tag = None
        wrongTags = 0
        for word_tag in word_tags:
            word = word_tag.split("_")[0]
            tag = word_tag.split("_")[1]
            if len(self.Tags) < 50:
                self.Tags.add(tag)
            if word in self.countWordTag:
                self.countWordTag[word][tag] = self.countWordTag[word].get(tag, 0) + 1
            else:
                self.countWordTag[word] = {}
                self.countWordTag[word][tag] = 1
            if prev_Tag != None:
                self.PrevCurrTagCount[(prev_Tag, tag)] = self.PrevCurrTagCount.get((prev_Tag, tag), 0) + 1
            prev_Tag = tag
            self.CountTags[tag] = self.CountTags.get(tag, 0) + 1

        
        TotalTags = len(word_tags)
        for word_tag in word_tags:
            
            word = word_tag.split('_')[0]
            tag = word_tag.split('_')[1]
            maxWordTag = max(self.countWordTag[word].values())
            if maxWordTag == 0:
                currentTag = "NN"
            else:
                for key in self.countWordTag[word]:
                    if self.countWordTag[word][key] == maxWordTag:
                        currentTag = key
            self.currentTags.append((word, currentTag))
            self.correctTags.append((word, tag))
            if tag != currentTag:
                wrongTags += 1
        error = float(wrongTags) * 100 / float(TotalTags)

        transformationRules = self.BestInstance().most_common()

        transformationRulesFile = open('transformationRules1.txt', 'w')
        transformationRulesFile.write(("FROM_TAG, TO_TAG, PREVIOUS_WORD_TAG\n"))
        for item in transformationRules:
            transformationRulesFile.write((item[0][0] + "," + item[0][1] + "," + item[0][2]  + "\n"))
        transformationRulesFile.close()

        


    def BestInstance(self):
        transformationRules = Counter()
        FromTo_PrevWordsTags = {}
        count = 0
        for fromTag in self.Tags:
            for toTag in self.Tags:
                if fromTag == toTag:
                    continue
                else:
                    FromTo_PrevWordsTags[(fromTag, toTag)] = {T: 0 for T in self.Tags}
                    pos=1
                    while(pos< len(self.currentTags)-1):
                        if self.correctTags[pos][1] == toTag and self.currentTags[pos][1] == fromTag:
                            FromTo_PrevWordsTags[(fromTag, toTag)][self.currentTags[pos - 1][1]] += 1
                        elif self.correctTags[pos][1] == fromTag and self.currentTags[pos][1] == fromTag:
                            FromTo_PrevWordsTags[(fromTag, toTag)][self.currentTags[pos - 1][1]] -= 1
                        pos+=1
                    for prevTag in FromTo_PrevWordsTags[(fromTag, toTag)]:
                        if FromTo_PrevWordsTags[(fromTag, toTag)][prevTag] > 0:
                            count += 1
                            transformationRules[(fromTag, toTag, prevTag)] = FromTo_PrevWordsTags[(fromTag, toTag)][prevTag]
        return transformationRules


if len(sys.argv)<2:
    print("Corpus file should be added as command line..")
    sys.exit()
else:
    
    b = PosTaggingBrills()

    b.PosTagModel(sys.argv[1])
    #b.NaiveBayesPOS(sys.argv[1])