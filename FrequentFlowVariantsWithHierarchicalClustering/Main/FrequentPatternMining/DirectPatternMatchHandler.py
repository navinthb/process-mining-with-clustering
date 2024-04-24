import pandas as pd
from collections import defaultdict

# Mine frequent variants based on direct text match
def mine_frequent_variants(log, sort_order):
    # Define a dictionary to store the frequency of event flows
    event_flows_with_counts = defaultdict(int)

    # Loop taces in the event log
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
    if sort_order == "DESC":
        reverse_order = True  
    else: 
        reverse_order = False
    
    event_flows_with_counts = sorted(event_flows_with_counts.items(), key=lambda x: x[1], reverse=reverse_order)

    # Create a Pandas dataFrame from the event flows
    event_flows_with_counts_df = pd.DataFrame(event_flows_with_counts, columns=['Event Flow', 'Count'])

    return event_flows_with_counts_df


# Get variants for each trace id
def get_trace_variants(log):
    # Define a list to store the tuples of Case ID and event flow
    trace_event_flows = []

    # loop traces in the event log
    for trace in log:
        events_list = []
        case_id = str(trace.attributes['concept:name'])

        # loop all events in the trace
        for event in trace:
            # concept:name is the key for event in a transaction
            concept_name = event['concept:name']
            if concept_name:
                events_list.append(concept_name)
                
        # Apppend the Case ID and event flow tuple to the list
        trace_event_flows.append((case_id, tuple(events_list)))

    # Create a Pandas DataFrame from the list of Case ID and Event Flow tuples
    trace_event_flows_df = pd.DataFrame(trace_event_flows, columns=['Case ID', 'Event Flow'])

    return trace_event_flows_df