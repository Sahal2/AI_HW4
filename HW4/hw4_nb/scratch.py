#P(vj) = the number of times the class/category appeared in the training data



import sys
<<<<<<< HEAD
dict = {}
Pvj = {}
listy = []
list_of_categories_and_their_P = {}
list_of_categories_appearing_in_training_data = []
=======
from copy import deepcopy
word_and_their_instances = {}
wrd_instance_by_category = {}
categories_and_their_instances = {}
wrd_and_their_probailities_by_category = {}
>>>>>>> function to calculate global instance and category instance
def learn(traindat):
    '''Load data for training; adding to
    dictionary of classes and counting words.'''
    with open(traindat,'r') as fd:
        for line in fd.readlines():
            id, *word = line.split()
<<<<<<< HEAD
            calc_Pvj(id)
            calc_wj
    print(Pvj)
        #print(list_of_categories_and_their_P)
            # calc_prob(count_wrds(word))

def calc_Pvj(category):
    list_of_categories_appearing_in_training_data.append(category)
    total_number_of_category_instances = len(list_of_categories_appearing_in_training_data)
    list_of_categories_and_their_P[category] = list_of_categories_appearing_in_training_data.count(category)
    for category in list_of_categories_and_their_P:
        Pvj[category] = list_of_categories_and_their_P[category] / total_number_of_category_instances
    return Pvj


# def count_wrds(self,wrd):
#     total_instances_of_each_word = []
#     total_word_count = list.count(wrd)
#     list_of_every_unique_word_in_the_list = list(set(wrd))
#     for one_word in list_of_every_unique_word_in_the_list:
#         total_instances_of_each_word.append(one_word)
#         total_instances_of_that_word = [one_word, wrd.count(one_word)]
#         total_instances_of_each_word.append(total_instances_of_that_word)
#
#     return total_instances_of_each_word,total_word_count
#
# def calc_prob(x,y):
#     prob=x/y
#     return prob





    #
    #
    # def add_prb(dictionary,item,id):
    #     try:
    #         dictionary[id].append(item)
    #     except KeyError:
    #         dictionary[id] = item


learn("testy.txt")
=======
            calculate_probability_of_each_word(add_word_inst(word),add_wrd_by_category(id,word))
    print(word_and_their_instances)

def add_word_inst(wrds):
    for wrd in wrds:
        try:
            word_and_their_instances[wrd] +=1
        except KeyError:
            word_and_their_instances[wrd] = 1
    return word_and_their_instances

def add_wrd_by_category(category,wrds):
    for wrd in wrds:
        try: 
            wrd_instance_by_category[wrd][category] += 1
        except KeyError:
            try:
                wrd_instance_by_category[wrd].update({category:1})
            except KeyError:
                wrd_instance_by_category[wrd] = {category:1}
    return wrd_instance_by_category

def give_second_dectionary(dictionary,key):
    return dictionary[key]
    

def calculate_probability_of_each_word(total_instance_of_wrd_in_document,total_instance_in_category):
    for word_instance_in_doc in total_instance_of_wrd_in_document:
        
    
    
    
    
    return wrd_and_their_probailities_by_category

learn("/Users/sahalfhussain/Desktop/AI_HW4/HW4/hw4_nb/testy.txt")
>>>>>>> function to calculate global instance and category instance
