import pandas as pd
import csv

def assign_weights(event_flows_df):
    
    # Assign  weigh to each record in  data frame, based on the counts
    event_flows_df['Weight'] = event_flows_df['Count'] / event_flows_df['Count'].sum()
    
    return event_flows_df


def assign_unique_variant_ids(event_flows_df, col_name):

    # Assign a unique variant number to each record in the data frame
    variant_numbers = {flow: f"Variant{i+1}" for i, flow in enumerate(event_flows_df['Event Flow'])}

    # A new column to store the generated variant numbers
    event_flows_df[col_name] = [variant_numbers[flow] for flow in event_flows_df['Event Flow']]

    return event_flows_df


# write values in a given cluster by
# generating a CaseID & assigning event names as activities
def write_cluster_to_csv(cluster, file_name):
    
    # Write to file
    with open(file_name, 'w', newline='') as csv_file:
        
        # Define fields for CSV
        field_names = ['CaseID', 'Activity']

        # Create a CSV writer object
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write the header row to the CSV file
        csv_writer.writeheader()

        # Looping through each trace 
        for trace_idx, trace in enumerate(cluster, start=1):
            
            # Looping through each event in the trace
            for event_idx, event_name in enumerate(trace, start=1):
                # Write each event to the CSV file
                csv_writer.writerow({'CaseID': f'Trace{trace_idx}', 'Activity': event_name})