#Import required library
import nltk

'''
import codecs
#Read the configure file
load_grammar = nltk.data.load('file:english_grammer.cfg')
file_input = codecs.open('english_input.txt', 'r')
for sent in file_input:
    wrong_syntax=1
    sent_split = sent.split()
    print("\n\n"+ sent)
    rd_parser = nltk.RecursiveDescentParser(load_grammar)
    for tree_struc in rd_parser.parse(sent_split):
        s = tree_struc
        wrong_syntax=0
        print("Correct Grammer !!!")
        print(str(s))
        f = open("demoEnglish.txt", "a")  
        f.write("Correct Grammer!!!")   
        f.write(str(s))
        f.close()
    if wrong_syntax==1:
        print("Wrong Grammer!!!!")
        f = open("demoEnglish.txt", "a")
        f.write("Wrong Grammer!!!")
        f.close()
'''

load_grammar = nltk.data.load('file:english_grammer.cfg')

rd = nltk.RecursiveDescentParser(load_grammar)

sentence = 'the cat chased the dog'.split()

for t in rd.parse(sentence1):
    print(t)
    