'''

Author: Sahal Fayed Hussain
CMSC 251: Artificial Intelligence
Sven Anderson
Collaboration Statement: I collaborated with Bobby, RJ, Jack, Mubasil and Cole.
Date: 9.Nov.2017


'''
from __future__ import print_function
import sys
try:
    from pandas import *
except ModuleNotFoundError:
    None
from copy import deepcopy
import math
wrd_instance_by_category = {}
categories_and_their_instances = {"total_instances_of_categories":0}
wrd_and_their_probailities_by_category = {}
got_correct = {"total_categories":0}
total_categories = 0
percentage_correct = 0
number_right = 0
number_wrong = 0
class NaiveBayes():
    '''Naive Bayes classifier for text data. Assumes input text is one text sample per line. First word is classification, a string.
    Remainder of line is space-delimited text.
    '''

    def __init__(self,train):

        self.learn(train) # loads train data, fills prob. table

    def learn(self,traindat):
        
        def add_wrd_instances(category,wrds):
            '''adds words to the two dimensional global dictionary (wrd_instance_by_category) 
            where the jeys are words and the values'''    
            for wrd in wrds:
                '''are dictionaries which have keys that are the names 
                of the class that and values as the number of instances of the wrd in that category'''                    
                try:                            #checks if the word is in the dictionary associated with a dictionary of the given class 
                    wrd_instance_by_category[wrd][category] += 1 #and increments the value of the key associated with that class                          
                    wrd_instance_by_category[wrd]["total_instance_of_wrds_in_doc"] += 1 #as well as a key which counts the total number of words that word in the whole document
                except KeyError:
                    '''if the it gets a KeyError it means either the word is there but it 
                    is not been seen in that category before or the word is a new word 
                    and none exist in the dictionary containing words'''    
                    try:
                        '''it checks if the word is in the dictionary and if so creates a new dictionary with the key as the name of the class 
                        and the value becuase it is the first instanece of this class'''

                        wrd_instance_by_category[wrd]["total_instance_of_wrds_in_doc"] += 1  
                        wrd_instance_by_category[wrd].update({category:1}) #update is used so that the previous keys (class) and vlaues(thier instances) are not removed
                    except KeyError:  
                        """if it encounter another KeyErron it means the word has not been encountered so a 
                        key is created and made to hold the value of the associated category"""
                        wrd_instance_by_category[wrd] = {category:1,"total_instance_of_wrds_in_doc":1}  #the total_instnaces_of_wrds_in_doc is also created
            return wrd_instance_by_category, categories_and_their_instances


        def calc_Pvj(category,total_number_of_wrds_in_category):    
            """takes in the class name associated with the line(document) and stores it in global dictionary categories_and_their_instances 
            by incrementing the value to the key instances_of_category it does so by dividing the total number of instnaces the class 
            has been encountered by the total number of instances of all classes encountered it also increments the total number of instances of all 
            categories encountered (number of lines in the document) and stores it in categories_and_their_instances with the key total_instances_of_categories 
            this function also increments the value of the key total_number_of_wrds_in_category which stores the value of the total number of 
            positions a word can be in the class givent to it as argument"""


            categories_and_their_instances["total_instances_of_categories"] += 1 
            try:    #it checks if the key (class) is in the dictionary and if so it increments the value associated with it 
                categories_and_their_instances[category]["instances_of_category"] += 1
                categories_and_their_instances[category]["total_number_of_words_in_category"] += total_number_of_wrds_in_category 
            except KeyError: #if the category is not in the dictionary then a key is created with a dictionary with the necessary keys
                categories_and_their_instances[category] = {"instances_of_category":1,"total_number_of_words_in_category": total_number_of_wrds_in_category} 

            return categories_and_their_instances

        with open(traindat,'r') as fd:  
            for line in fd.readlines():
                id, *word = line.split()
                add_wrd_instances(id,word) #takes all the class names (ex:alt.atheism) and the words assoociated with it and feeds it to the add_wrd_instances function
                calc_Pvj(id,len(word)) #feeds the class names as well as the length of the list that contains all the words in the category 
        
    

    def runTestRaw(self,testdat):   
        """Use raw probabilities for training."""
        def calculate_prob_wrd(wrds,categories_and_their_instances):  
            """runs the test file and then looks it up in the global dictionary wrd_instance_by_category and uses the values to calculate the 
            probability of that word appearing associated with a class and then gives back the category that has the highest probability. It takes as arguments: 
            all the words in a line in test file and the global dictionary categories_and_their_instances. Then this is multiplied by the prior probability of the class
            which is calculated by the calculate_prior_probability function""" 
            probability_of_wrds_given_category = {} #this dictionary stores all the probabilities of the line belonging to a specific class 
            category_without_total_instance = deepcopy(categories_and_their_instances) #copy the global dictionary ategories_and_their_instances so a dictionary 
            del category_without_total_instance["total_instances_of_categories"] #withou total_instances_of_categories key value pair
            for categories in category_without_total_instance: #can be iterated over to go through every possible class
                probability_of_wrds = 1.0   #variable stores the product of the probability of each word
                probability_of_wrd = 0.0    #variable stores the probability of the word
                for wrd in wrds:
                    """Loops over every word in the given test class and then goes to the global dictionary wrd_instance_by_category and retrives the
                    value given by the key wrd_instance_by_category[wrd][categories] which is the probability of it occuring in a class (receives class from outter for loop) 
                    and divides that by the total number of words that have been encountered that were associated with the class by accessing the value stored within the 
                    key: categories_and_their_instances[categories]["total_number_of_words_in_category"]"""
                    try:
                        probability_of_wrd = (wrd_instance_by_category[wrd][categories]/categories_and_their_instances[categories]["total_number_of_words_in_category"])
                    except KeyError:
                        probability_of_wrd = 0.000000001
                    probability_of_wrds = probability_of_wrds * probability_of_wrd #multiplies the probability of the current word to the previous one
                probability_of_wrds_given_category[(probability_of_wrds*(calculate_prior_probability(categories_and_their_instances,categories) ))] =  categories 
                """stores the probabilities (product of prior probabilities and the aggregate word probability 
                as keys in the dictionary probability_of_wrds_given_category whose values are the class that is being passed by the outter loop"""
            return probability_of_wrds_given_category[max(probability_of_wrds_given_category.keys())] #returns the category with the largest probability


        def calculate_prior_probability(categories_and_their_instances,categories):
            """takes a class and the global dictionary categories_and_their_instances as arguments retrieves the value stored in key instances_of_category of the argument class
            then divides that by the value stored in the key total_instances_of_categories"""
            prior_probability = (categories_and_their_instances[categories]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"])
            return prior_probability
        
        
        def calculate_precentage_right(assumed_category,correct_category):
            """"This takes the category with the maximium probability from (argmax) calculate_prob_wrd  function and checks it with 
            the classes obtained from the test file to calculate the percentage the algorithm got correct"""
            global number_right
            got_correct["total_categories"] +=  1
            if assumed_category == correct_category:
                try:
                    number_right += 1
                    got_correct[correct_category]["correct"] += 1           #it increments the value of the key correct everytime it encounter a correct argmax
                    got_correct[correct_category]["total_instances"] += 1
                except KeyError:
                    None
                    got_correct[correct_category] = {"correct":1,"total_instances":1}
            else:
                try:
                    got_correct[correct_category]["total_instances"] += 1 
                except KeyError:
                    got_correct[correct_category] = ({"tota_instances":1})
            return got_correct
        


        def calculate_statistics_TEST(classy3):
            global percentage_correct
            print("################### TEST  OUTPUT #######################")
            stat = []
            classy4 = deepcopy(classy3)
            del classy4["total_categories"]
            stat.append(["Category", "NCorrect", "N","%corr"])
            for key in classy4:
                stat.append([key,classy4[key]['correct'],classy4[key]["total_instances"],classy4[key]['correct']/classy4[key]["total_instances"]])
                percentage_correct += classy4[key]['correct']/classy4[key]["total_instances"]
            percentage_correct = (percentage_correct/20)*100
            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
        
        def calculate_statistics_TRAIN(dictionary):
            print("################ TRAIN  OUTPUT ####################")
            stat = []
            stat.append(["Category", "NDoc", "NWords","P(cat)"])
            classy2 = deepcopy(dictionary)
            del classy2["total_instances_of_categories"]
            for key in classy2:
                stat.append([key,dictionary[key]["instances_of_category"],
                categories_and_their_instances[key]["total_number_of_words_in_category"],
                categories_and_their_instances[key]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"]],
                )

            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
            



        with open(testdat,'r') as fd:
            for line in fd.readlines():
                id, *word = line.split()
                calculate_precentage_right(calculate_prob_wrd(word,categories_and_their_instances),id)
        calculate_statistics_TRAIN(categories_and_their_instances)
        calculate_statistics_TEST(got_correct)
        
            

        
            

    def runTestMest(self,testdat):                                                                       #runs the test file and calculates the probability and prints the result

        def calculate_prob_wrd(wrds,categories_and_their_instances):
            probability_of_wrds_given_category = {}
            global distinct_words_in_line
            category_without_total_instance = deepcopy(categories_and_their_instances)
            del category_without_total_instance["total_instances_of_categories"]
            for categories in category_without_total_instance:
                """We add the number of distinct words in the category to the to the total number of words in the category and add 1 to the number of times the 
                word appeared in the category while calculating the probability of the word"""
                probability_of_wrds = 1.0
                probability_of_wrd = 0.0
                for wrd in wrds:
                    try:
                        probability_of_wrd = (   wrd_instance_by_category[wrd][categories]+1   ) / (   categories_and_their_instances[categories]["total_number_of_words_in_category"]  +   len(wrd_instance_by_category)  )
                    except KeyError:
                        probability_of_wrd = 1.0/(categories_and_their_instances[categories]["total_number_of_words_in_category"]  +   len(wrd_instance_by_category)  )
                    probability_of_wrds = probability_of_wrds * probability_of_wrd 
                probability_of_wrds_given_category[(probability_of_wrds * (calculate_prior_probability(categories_and_their_instances,categories)))] =  categories
            return probability_of_wrds_given_category[max(probability_of_wrds_given_category.keys())]


        def calculate_prior_probability(categories_and_their_instances,categories):
            prior_probability = categories_and_their_instances[categories]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"]
            
            return prior_probability

        def calculate_precentage_right(assumed_category,correct_category):
            """"This takes the category with the maximium probability from (argmax) calculate_prob_wrd  function and checks it with 
            the classes obtained from the test file to calculate the percentage the algorithm got correct"""
            global number_right
            got_correct["total_categories"] +=  1
            if assumed_category == correct_category:
                try:
                    number_right += 1
                    got_correct[correct_category]["correct"] += 1           #it increments the value of the key correct everytime it encounter a correct argmax
                    got_correct[correct_category]["total_instances"] += 1
                except KeyError:
                    None
                    got_correct[correct_category] = {"correct":1,"total_instances":1}
            else:
                try:
                    got_correct[correct_category]["total_instances"] += 1 
                except KeyError:
                    got_correct[correct_category] = ({"tota_instances":1})
            return got_correct


        def calculate_statistics_TEST(classy3):
            global percentage_correct
            print("################### TEST  OUTPUT #######################")
            stat = []
            classy4 = deepcopy(classy3)
            del classy4["total_categories"]
            stat.append(["Category", "NCorrect", "N","%corr"])
            for key in classy4:
                stat.append([key,classy4[key]['correct'],classy4[key]["total_instances"],classy4[key]['correct']/classy4[key]["total_instances"]])
                percentage_correct += classy4[key]['correct']/classy4[key]["total_instances"]
            percentage_correct = (percentage_correct/20)*100
            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
        
        def calculate_statistics_TRAIN(dictionary):
            print("################ TRAIN  OUTPUT ####################")
            stat = []
            stat.append(["Category", "NDoc", "NWords","P(cat)"])
            classy2 = deepcopy(dictionary)
            del classy2["total_instances_of_categories"]
            for key in classy2:
                stat.append([key,dictionary[key]["instances_of_category"],
                categories_and_their_instances[key]["total_number_of_words_in_category"],
                categories_and_their_instances[key]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"]],
                )

            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
            



        with open(testdat,'r') as fd:
            for line in fd.readlines():
                id, *word = line.split()
                calculate_precentage_right(calculate_prob_wrd(word,categories_and_their_instances),id)
        calculate_statistics_TRAIN(categories_and_their_instances)
        calculate_statistics_TEST(got_correct)
        
            

    def runTestTifdif(slef,testdat):                                                            #runs the test file and calculates the probability and prints the result
        """ This function weights (multiply) the mestimate values of the probabilities of the word with the inverse document frequency 
                    which is calculated by the function calculate_tf_df """
        def calculate_prob_wrd(wrds,categories_and_their_instances):
            probability_of_wrds_given_category = {}
            global distinct_words_in_line
            category_without_total_instance = deepcopy(categories_and_their_instances)
            del category_without_total_instance["total_instances_of_categories"]
            for categories in category_without_total_instance:
                probability_of_wrds = 0.0
                probability_of_wrd = 0.0
                for wrd in wrds:
                    """"It uses math.log of the probability of words and adds the probability of each word instead of taking products """
                    try:
                        probability_of_wrd =((( ( (   wrd_instance_by_category[wrd][categories]+1   ) / (   categories_and_their_instances[categories]["total_number_of_words_in_category"]  +   len(wrd_instance_by_category)  ) ) )) * (calculate_tf_df(wrd,categories_and_their_instances)))
                    except KeyError:
                        probability_of_wrd = (1.0/(categories_and_their_instances[categories]["total_number_of_words_in_category"]  +   len(wrd_instance_by_category)  ) )
                    probability_of_wrds = probability_of_wrds + math.log(probability_of_wrd) 
                probability_of_wrds_given_category[(probability_of_wrds + (calculate_prior_probability(categories_and_their_instances,categories)))] =  categories
            return probability_of_wrds_given_category[max(probability_of_wrds_given_category.keys())]


        def calculate_prior_probability(categories_and_their_instances,categories):
            prior_probability = math.log(categories_and_their_instances[categories]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"])
            
            return prior_probability

        
        
        
        def calculate_tf_df(word,categories_and_their_instances):
            """this takes as argument a word and the global dictionary categories_and_their_instances and returns logarithm of the total instances of all
            classes in the training document divided by the total amount of classes that word has appered in the training document"""
            return math.log(categories_and_their_instances["total_instances_of_categories"]/(len(wrd_instance_by_category[word])-1))
            

        def calculate_precentage_right(assumed_category,correct_category):
            """"This takes the category with the maximium probability from (argmax) calculate_prob_wrd  function and checks it with 
            the classes obtained from the test file to calculate the percentage the algorithm got correct"""
            global number_right
            got_correct["total_categories"] +=  1
            if assumed_category == correct_category:
                try:
                    number_right += 1
                    got_correct[correct_category]["correct"] += 1           #it increments the value of the key correct everytime it encounter a correct argmax
                    got_correct[correct_category]["total_instances"] += 1
                except KeyError:
                    None
                    got_correct[correct_category] = {"correct":1,"total_instances":1}
            else:
                try:
                    got_correct[correct_category]["total_instances"] += 1 
                except KeyError:
                    got_correct[correct_category] = ({"tota_instances":1})
            return got_correct
        
        def calculate_statistics_TEST(classy3):
            global percentage_correct
            print("################### TEST  OUTPUT #######################")
            stat = []
            classy4 = deepcopy(classy3)
            del classy4["total_categories"]
            stat.append(["Category", "NCorrect", "N","%corr"])
            for key in classy4:
                stat.append([key,classy4[key]['correct'],classy4[key]["total_instances"],classy4[key]['correct']/classy4[key]["total_instances"]])
                percentage_correct += classy4[key]['correct']/classy4[key]["total_instances"]
            percentage_correct = (percentage_correct/20)*100
            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
        
        def calculate_statistics_TRAIN(dictionary):
            print("################ TRAIN  OUTPUT ####################")
            stat = []
            stat.append(["Category", "NDoc", "NWords","P(cat)"])
            classy2 = deepcopy(dictionary)
            del classy2["total_instances_of_categories"]
            for key in classy2:
                stat.append([key,dictionary[key]["instances_of_category"],
                categories_and_their_instances[key]["total_number_of_words_in_category"],
                categories_and_their_instances[key]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"]],
                )

            try:
                print(DataFrame(stat))
                print(("Avg pct correct:",percentage_correct))
            except NameError:
                for row in stat:
                    print("\n")
                    for elem in row:
                        print(repr(elem).rjust(2), end=" ")
            return None
            



        with open(testdat,'r') as fd:
            for line in fd.readlines():
                id, *word = line.split()
                calculate_precentage_right(calculate_prob_wrd(word,categories_and_their_instances),id)
        calculate_statistics_TRAIN(categories_and_their_instances)
        calculate_statistics_TEST(got_correct)
        
            
        
        
                
                    


def main():
    # if len(sys.argv) != 3:
    #     print("Usage: %s trainfile testfile" % sys.argv[0])
    #     sys.exit(-1)

    version = sys.argv[3] 
    
    nbclassifier = NaiveBayes(sys.argv[1])
    # nbclassifier.printClasses()
    if version == "raw":
        nbclassifier.runTestRaw(sys.argv[2])
    elif version == "mest":
        nbclassifier.runTestMest(sys.argv[2])
    elif version == "tfdf":
        nbclassifier.runTestTifdif(sys.argv[2])
        

if __name__ == "__main__":
    main()
