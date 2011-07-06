'''
Transmogrify CMU ARCTIC prompts into versions usable in the Sphinx 4 model adaptation process:
http://cmusphinx.sourceforge.net/wiki/tutorialadapt

Copyright 2011 Brian Romanowski. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY BRIAN ROMANOWSKI ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BRIAN ROMANOWSKI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors.

Created on Jul 5, 2011
@author: romanows
'''
import re
from collections import defaultdict

arcticPromptFilename = '/home/romanows/Desktop/cmuarctic.data'  # http://festvox.org/cmu_arctic/cmuarctic.data
cmuSphinxDictFilename = '/home/romanows/Desktop/cmudict.0.7a_SPHINX_40'  # https://cmusphinx.svn.sourceforge.net/svnroot/cmusphinx/trunk/cmudict/sphinxdict/cmudict.0.7a_SPHINX_40

promptsOutFilename = '/home/romanows/Desktop/arcticAll.prompts'
transcriptionOutFilename = '/home/romanows/Desktop/arcticAll.transcription'
transcriptionPronunciationAltsOutFilename = '/home/romanows/Desktop/arcticAll.transcription.withPronunciationAlts'
dictionaryOutFilename = '/home/romanows/Desktop/arcticAll.dict'
fileidsOutFilename = '/home/romanows/Desktop/arcticAll.fileids'

# Read prompts; in the same format as the arctic prompts found at: http://festvox.org/cmu_arctic/cmuarctic.data
# Does some preliminary filtering
filenameToPrompts = {}
promptWords = set()
hyphenatedWords = set()
interestingChars = set()
with open(arcticPromptFilename,'r') as f:
    for line in f:
        m = re.search(r'(arctic_[^\s]+)\s"(.*)"',line)
        filename, utterance = m.group(1), m.group(2)
        
        # Don't allow utterances with numerals (too few to bother with correctly )
        if re.match(r'.*[0-9].*', utterance) is not None:
            print 'skipping utterance with numbers:', utterance
            continue
        
        if utterance.strip() == '':
            print 'skipping empty utterance:', utterance
            continue
                    
        filenameToPrompts[filename] = utterance
        utterance = utterance.lower()
        
        for s in re.split(r"[\sA-Za-z'-]+", utterance):
            if s != '':
                interestingChars.add(s)
        
        for w in re.split(r"[^A-Za-z'-]+", utterance):
            if w == '':
                continue
            if '-' in w:
                hyphenatedWords.add(w)
                for v in re.split(r'[-]+',w):
                    if v != '':
                        promptWords.add(v)
            promptWords.add(w)

print "%d utterances, %d unique words" % (len(filenameToPrompts), len(promptWords))
print "Interesting characters:", interestingChars
print "Hyphenated words:", hyphenatedWords 


# Added after observing the output of this program before 
hypenSubs = {}
hypenSubs['re-entered'] = 'reentered'

for k,v in hypenSubs.items():
    promptWords.add(v)
        
# Read cmu dictionary: https://cmusphinx.svn.sourceforge.net/svnroot/cmusphinx/trunk/cmudict/sphinxdict/cmudict.0.7a_SPHINX_40
cmuSphinxDict = defaultdict(list)
dictPromptWords = set()
with open(cmuSphinxDictFilename,'r') as f:
    for line in f:
        word,phones = line.strip().split('\t')
        basicWord = word.split('(')[0]
        if basicWord.lower() in promptWords:
            cmuSphinxDict[basicWord].append(phones)
            if word not in cmuSphinxDict:
                 cmuSphinxDict[word].append(phones)
            dictPromptWords.add(word.lower())
            
nonDictPromptWords = set(promptWords).difference(dictPromptWords)
multiplePronunciationWords = set()
for w in [k for k,v in cmuSphinxDict.items() if len(v) > 1]:
    multiplePronunciationWords.add(w)
    
print "%d dictionary words, %d prompts words missing" % (len(cmuSphinxDict),len(nonDictPromptWords))
print "%d dictionary words have more than one pronunciation" % (len(multiplePronunciationWords))
print "non-dict prompt words:",nonDictPromptWords


# Added after observing the output of this program, earlier
newWords = {}
newWords['springy'] = 'S P R IH NG IY' # like "stringy" or "thingy"
newWords['provocateurs'] = 'P R OW V AA K AH T ER Z' # like "restauranteurs"  
newWords['nightglow'] = 'N AY T G L OW' # just concatenated
newWords['roadmate'] = 'R OW D M EY T' # just concatenated
newWords['unquenchable'] = 'AH N K W EH N CH AH B AH L'
newWords['tomfoolery'] = 'T AA M F UW L ER IY'
newWords["promoter's"] = 'P R AH M OW T ER Z'
newWords["daylight's"] = 'D EY L AY T S'
newWords["factor's"] = 'F AE K T ER Z'
newWords["eileen's"] = 'AY L IY N Z'
newWords["selden's"] = 'S EH L D AH N Z'
newWords["jeanne's"] = 'JH IY N Z'
newWords["thorpe's"] = 'TH AO R P S'
newWords["steward's"] = 'S T UW ER D Z'
newWords["pascal's"] = 'P AE S K AE L Z'
newWords["pearce's"] = 'P IH R S IH Z' # same as "pierce's"
newWords["hanrahan's"] = 'HH AE N R AH HH AE N Z'
newWords["seafaring"] = 'S IY F EH R IY NG'
newWords["kerfoot's"] = 'K ER F UH T S'
newWords["mcfee's"] = 'M AH K F IY Z'
newWords["dennin's"] = 'D EH N IH N Z'
newWords["daughtry's"] = 'D AO T R IY Z'
newWords["companion's"] = 'K AH M P AE N Y AH N Z'
newWords["brodie's"] = 'B R OW T IY Z'
newWords["nakata's"] = 'N AA K AA T AH Z'
newWords["doane's"] = 'D OW N Z'

for k,v in newWords.items():
    cmuSphinxDict[k.upper()] = v

filenames = filenameToPrompts.keys()
filenames.sort()

# Write custom prompts, dictionary, transcriptions, fileids
fileidsFile = open(fileidsOutFilename,'w')
promptsFile = open(promptsOutFilename,'w')
transcriptionFile = open(transcriptionOutFilename,'w')
transcriptionPronunciationAltsFile = open(transcriptionPronunciationAltsOutFilename,'w')

class WordNotFoundInDictionary(Exception):
    pass

failedUtterances = []
for filename in filenames:
    # substitute utterance with dictionary words, splitting on [^A-Za-z'-]
    # if we can't find pronunciations for all words, try splitting hyphens
    # otherwise, continue with the next utterance and store failed utterance conversion attempt
    
    origUtterance = filenameToPrompts[filename]
    utterance = origUtterance.lower()
    try:
        utt = []
        uttAlt = []
        for w in re.split(r"[^A-Za-z'-]+", utterance):
            if w == '':
                continue

            # TODO: Refactor the complex special-casing below
            
            writing = True
            if len(cmuSphinxDict[w.upper()]) > 0:
                utt.append(w.upper())

                if len(cmuSphinxDict[w.upper()]) > 1:
                    uttAlt.append('%s[%s]' % (w.upper(), cmuSphinxDict[w.upper()][0]))
                    i = 2
                    while len(cmuSphinxDict['%s(%d)' % (w.upper(),i)]) > 0:
                        uttAlt.append('%s(%d)[%s]' % (w.upper(), i, cmuSphinxDict['%s(%d)' % (w.upper(),i)][0]))
                        i += 1
                else:
                    uttAlt.append(w.upper())
                        
            else:
                if w in hypenSubs.keys():
                    utt.append(hypenSubs[w].upper())  # No alternate pronunciations in hyphen subs at the moment
                    uttAlt.append(hypenSubs[w].upper())
                elif '-' in w:
                    for v in re.split(r'[-]+',w):
                        if v == '':
                            continue
                        elif len(cmuSphinxDict[v.upper()]) > 0:
                            utt.append(v.upper())
                            
                            if len(cmuSphinxDict[v.upper()]) > 1:
                                uttAlt.append('%s[%s]' % (v.upper(), cmuSphinxDict[v.upper()][0]))
                                i = 2
                                while len(cmuSphinxDict['%s(%d)' % (v.upper(),i)]) > 0:
                                    uttAlt.append('%s(%d)[%s]' % (v.upper(), i, cmuSphinxDict['%s(%d)' % (v.upper(),i)][0]))
                                    i += 1
                            else:
                                uttAlt.append(v.upper())                     

                        else:
                            failedUtterances.append(utterance)
                            raise WordNotFoundInDictionary()
                else:
                    failedUtterances.append(utterance)
                    raise WordNotFoundInDictionary()                        
                        
        fileidsFile.write(filename + '\n')
        promptsFile.write('%s:\t%s\n' % (filename,origUtterance))
        transcriptionFile.write('<s> %s </s> (%s)\n' % (' '.join(utt),filename))
        transcriptionPronunciationAltsFile.write('<s> %s </s> (%s)\n' % (' '.join(uttAlt),filename))
    except WordNotFoundInDictionary:
        pass # ok, this just means we go onto the next utterance
    
transcriptionPronunciationAltsFile.close()
transcriptionFile.close()
promptsFile.close()
fileidsFile.close()

dictWordsSorted = cmuSphinxDict.keys()
dictWordsSorted.sort()

dictionaryFile = open(dictionaryOutFilename,'w')
for k in dictWordsSorted:
    if len(cmuSphinxDict[k]) > 0:
        dictionaryFile.write('%s\t%s\n' % (k,cmuSphinxDict[k][0]))
dictionaryFile.close()

print "%d utterances couldn't be transcribed" % (len(failedUtterances))
print "left out:", failedUtterances  

print 'done.'