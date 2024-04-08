import pandas as pd

def assign_weights(event_flows_df):
    
    # Assign a weight to each record in the data frame, based on the counts
    event_flows_df['Weight'] = event_flows_df['Count'] / event_flows_df['Count'].sum()
    
    return event_flows_df


def assign_unique_variant_ids(event_flows_df, col_name):

    # Assign a unique variant number to each record in the data frame
    variant_numbers = {flow: f"Variant{i+1}" for i, flow in enumerate(event_flows_df['Event Flow'])}

    # A new column to store the generated variant numbers
    event_flows_df[col_name] = [variant_numbers[flow] for flow in event_flows_df['Event Flow']]

    return event_flows_df