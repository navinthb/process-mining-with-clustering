## This will return a random subset of a given event log by extracting a given ratio of items
import random

def get_subset(log_all, portion):

    # Final size of the subset
    subset_size = round(len(log_all) * portion)

    # Seleting data randomly for the subset
    log_subset = random.sample(log_all, subset_size)

    return log_subset