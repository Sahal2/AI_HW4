#P(vj) = the number of times the class/category appeared in the training data



import sys
dict = {}
Pvj = {}
listy = []
list_of_categories_and_their_P = {}
list_of_categories_appearing_in_training_data = []
def learn(traindat):
    '''Load data for training; adding to
    dictionary of classes and counting words.'''
    with open(traindat,'r') as fd:
        for line in fd.readlines():
            id, *word = line.split()
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