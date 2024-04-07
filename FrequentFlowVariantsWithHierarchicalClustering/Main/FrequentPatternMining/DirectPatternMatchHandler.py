import pandas as pd
from collections import defaultdict

# Mine frequent variants based on direct text match
def mine_frequent_variants(log, sort_order):
    # Define a dictionary to store the frequency of event flows
    event_flows_with_counts = defaultdict(int)

    # loop taces in the event log
    for trace in log:
        events_list = [] 
        # loop all events in the tace
        for event in trace:
            # concept:name is the key for event in a transaction
            concept_name = event['concept:name']
            if concept_name:
                events_list.append(concept_name)
        # Convert the event list into a tuple for hashing
        events_tuple = tuple(events_list)
        
        event_flows_with_counts[events_tuple] += 1

    # Sort the event variants by their frequency in the given order
    reverse_order = True if sort_order == "DESC" else False
    event_flows_with_counts = sorted(event_flows_with_counts.items(), key=lambda x: x[1], reverse=reverse_order)

    # Create a Pandas dataFrame from the event flows
    event_flows_with_counts_df = pd.DataFrame(event_flows_with_counts, columns=['Event Flow', 'Count'])

    return event_flows_with_counts_df