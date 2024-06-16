import random

def combine_and_shuffle_lists(*lists):
    combined_list = [item for sublist in lists for item in sublist]
    random.shuffle(combined_list)
    return combined_list