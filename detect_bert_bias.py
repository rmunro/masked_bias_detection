#!/usr/bin/env python

"""FIND BIASES

Extracts the attributes related to independent pronouns like 
"hers", "his", "theirs" or any other independent possessive pronoun

Then, extract whether BERT prefers a certain pronoun for that item

prints a tab-separated grid of every word for every template sentence


"""

import sys
import re
import collections
import os

from collections import defaultdict    
sys.stderr.write("STEP 1: LOADING BERT MODEL\n")
import bert_predictions
# import get_hers_his_theirs


# seed_data = "./UD_English-Pronouns/en_pronouns-ud-test.conllu"

seed_data = "./new_sentences.conllu"


if not os.path.exists(seed_data):
    print("No file found: "+seed_data+"\nThis should contain your starting files")
    exit()


def extract_preferences(replacements):
    all_sentences = "" # all sentences, old and new
    
    text = ""
    previous = ""
    
    prompts = ""

    fp = open(seed_data, 'r')
    line = fp.readline()
        
    while line:
        if line.startswith("# previous = "):
            previous = line.lstrip("# previous = ").strip()
        if line.startswith("# text = "):
            text = line.lstrip("# text = ").strip()
        if line.strip() == "" and ("car" in text or "car" in previous) and "theirs" in text:
            prompt = previous+" "+text
            prompt = prompt.replace("cars", "[MASK]")
            prompt = prompt.replace("car", "[MASK]")
            prompts += "\t"+prompt
    
        line = fp.readline()
        
    fp.close()
    
    print("attribute\tratio (<0=hers, >0=his)")
    
    for noun in replacements:
        fp = open(seed_data, 'r')
        line = fp.readline()
        
        attribute_biases = []
        
        result = noun
        while line:
               # print(line)
            if line.strip() == "" and ("car" in text or "car" in previous) and "hers" in text:
                word = "car"
                if ("cars" in text or "cars" in previous):
                    word = "cars"
                
                new_text = text.replace(word, noun)
                new_previous = previous.replace(word, noun)
                
                
                # sys.stderr.write("LOOKING AT: "+new_previous+" "+new_text+"\n")
                # print()
                difference = bert_predictions.get_hers_his_theirs_difference(new_text, new_previous)
                
                # '''
                # hers his difference:
                difference.append(difference[2] / difference[1])
                # sys.stderr.write(str(difference))
                his_bias = difference[2] / difference[1]
                if difference[1] > difference[2]:
                    his_bias = 0 - (difference[1] / difference[2])
                result += "\t"+str(his_bias)
                attribute_biases.append(his_bias)
                # '''
    
                '''
                # hers theirs difference:
                difference.append(difference[3] / difference[1])
                sys.stderr.write(str(difference))
                theirs_bias = difference[3] / difference[1]
                if difference[1] > difference[3]:
                    theirs_bias = 0 - (difference[1] / difference[3])
                result += "\t"+str(theirs_bias)
                '''
    
                '''
                # his theirs difference:
                difference.append(difference[2] / difference[3])
                sys.stderr.write(str(difference))
                his_bias = difference[2] / difference[3]
                if difference[3] > difference[2]:
                    his_bias = 0 - (difference[3] / difference[2])
                result += "\t"+str(his_bias)
                '''
               
                
                
                            
            if line.startswith("# previous = "):
                previous = line.lstrip("# previous = ").strip()
            if line.startswith("# text = "):
                text = line.lstrip("# text = ").strip()
               
            line = fp.readline()
            
        ave = sum(attribute_biases) / len(attribute_biases)
               
        print(noun+"\t"+str(ave))
        
        fp.close()
        
        

all_variations = defaultdict(lambda: 0)


sys.stderr.write("STEP 2: LOAD UNIVERSAL DEPENDENCY DATASET\n")
sys.stderr.write("STEP 3 & 4: MASK ATTRIBUTES TO PREDICT NEW ONES\n")


text = ""
previous = ""

temp = 0

fp = open(seed_data, 'r')
line = fp.readline()
while line:
    # print(line)
    if line.strip() == "" and ("car" in text or "car" in previous) and "hers" in text:
        word = "car"
        if ("cars" in text or "cars" in previous):
            word = "cars"
            
        new_text = text.replace("hers", "theirs")
        new_previous = previous.replace("hers", "theirs")
        # new_text = text  # uncomment this and next line to get hers-preferred items
        # new_previous = previous
            
        # print(word)
        variations = bert_predictions.extract_bert_predictions(new_text, new_previous, word, [], True)
        # print(variations)
        for word, count in variations.items():
            all_variations[word] += count
            
    if line.startswith("# previous = "):
        previous = line.lstrip("# previous = ").strip()
    if line.startswith("# text = "):
        text = line.lstrip("# text = ").strip()
           
    line = fp.readline()

    
    
fp.close()

sys.stderr.write("STEP 5, 6 & 7: CREATE NEW SENTENCES AND PREDICT PRONOUNS\n")

all_items = all_variations.keys()

extract_preferences(all_items)


    
