import sys
from copy import deepcopy
wrd_instance_by_category = {}
categories_and_their_instances = {"total_instances_of_categories":0}
wrd_and_their_probailities_by_category = {}

total_categories = 0
number_right = 0
number_wrong = 0
i = 0
def learn(traindat):
    '''Load data for training; adding to
    dictionary of classes and counting words.'''
    with open(traindat,'r') as fd:
        for line in fd.readlines():
            id, *word = line.split()
            add_wrd_instances(id,word)
            calc_Pvj(id,len(word))      
        
def add_wrd_instances(category,wrds):                                               #adds the words to a dictionary that holds instances of a word that appear in the whole document
    for wrd in wrds:                                                                #also adds the word to a dictionary containing all the instances of the word according to the category
        try:
            wrd_instance_by_category[wrd][category] += 1
            wrd_instance_by_category[wrd]["total_instance_of_wrds_in_doc"] += 1
        except KeyError:
            try:
                wrd_instance_by_category[wrd]["total_instance_of_wrds_in_doc"] += 1
                wrd_instance_by_category[wrd].update({category:1})
            except KeyError:
                wrd_instance_by_category[wrd] = {category:1,"total_instance_of_wrds_in_doc":1}
    return wrd_instance_by_category, categories_and_their_instances

def calc_Pvj(category,total_number_of_wrds_in_category):
    try:
        categories_and_their_instances["total_instances_of_categories"] += 1
        categories_and_their_instances[category]["instances_of_category"] += 1
        categories_and_their_instances[category]["total_number_of_words_in_category"] += total_number_of_wrds_in_category
    except KeyError:
        categories_and_their_instances[category] = {"instances_of_category":1,"total_number_of_words_in_category": total_number_of_wrds_in_category}
        categories_and_their_instances.update({})
    return categories_and_their_instances

# def calculate_words_in_category(category,wrds):
#     for wrd in wrds
    

def runTest(testdat):                                                            #runs the test file and calculates the probability and prints the result

    def calculate_prob_wrd(wrds,categories_and_their_instances):
        probability_of_wrds_given_category = {}
        category_without_total_instance = deepcopy(categories_and_their_instances)
        del category_without_total_instance["total_instances_of_categories"]
        for categories in category_without_total_instance:
            probability_of_wrds = 1.0
            probability_of_wrd = 0.0
            for wrd in wrds:
                try:
                    # categories_and_their_instances[categories]["total_number_of_words_in_category"]
                    probability_of_wrd = (wrd_instance_by_category[wrd][categories]/categories_and_their_instances[categories]["total_number_of_words_in_category"])
                except KeyError:
                    probability_of_wrd = 0.000000001
                probability_of_wrds = probability_of_wrds * probability_of_wrd
                
            probability_of_wrds_given_category[(probability_of_wrds*(calculate_prior_probability(categories_and_their_instances,categories) ))] =  categories
        return probability_of_wrds_given_category[max(probability_of_wrds_given_category.keys())]


    def calculate_prior_probability(categories_and_their_instances,categories):
        prior_probability = (categories_and_their_instances[categories]["instances_of_category"]/categories_and_their_instances["total_instances_of_categories"])
        return prior_probability
        

    def calculate_precentage_right(assumed_category, correct_category):
        global total_categories
        global number_right
        total_categories +=  1
        if assumed_category == correct_category:
            number_right += 1
        # print(assumed_category,probability_of_wrds_given_category[max(probability_of_wrds_given_category.keys())])
        return print((number_right/total_categories)*100)

    with open(testdat,'r') as fd:
        for line in fd.readlines():
            id, *word = line.split()
            global i 
            # i += 1
            # print(id,i)
            # distinct_words_in_line = list(set(word))
            calculate_precentage_right(calculate_prob_wrd(word,categories_and_their_instances),id)
            # calculate_prob_wrd(word,categories_and_their_instances)
            # print(calculate_probability_of_words(distinct_words_in_line,categories_and_their_instances),id)

learn("/Users/sahalfhussain/Desktop/AI_HW4/HW4/hw4_nb/20ng-train-stemmed.txt")
runTest("/Users/sahalfhussain/Desktop/AI_HW4/HW4/hw4_nb/20ng-test-stemmed.txt")