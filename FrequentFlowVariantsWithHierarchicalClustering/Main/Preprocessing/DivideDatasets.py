## This will return a random subset of an event log by extracting a given portion of items
import random
from pm4py.objects.log.obj import EventLog

def get_subset(log_all, portion_of):

    # Create a subset by dividing the full dataset into a given portion 
    # & take 1 trace from consecutive records 
    event_log_subset = EventLog()

    for i in range(0, len(log_all), portion_of):
        if i + 2 < len(log_all):
            event_log_subset.append(log_all[i])

    return event_log_subset