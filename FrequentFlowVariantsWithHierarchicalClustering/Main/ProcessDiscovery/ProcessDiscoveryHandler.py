import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer


def create_cluster_full_event_log(cluster, trace_event_flows_df, full_log):

    cluster_strings = [str(tup) for tup in cluster]
    cluster_df = pd.DataFrame(cluster_strings, columns=['Event Flow'])

    # Join cluster_df with trace_event_flows_df to get the corresponding actual concept:name of the trace
    # as it is in the full event log
    cluster_event_log_actual_df = pd.merge(cluster_df, trace_event_flows_df, on='Event Flow', how='inner')
    #cluster_event_log_actual_df
    # Covert full log (in pm4py.objects.log.obj.EventLog type) into a dataframe
    full_log = log_converter.apply(full_log, variant=log_converter.Variants.TO_DATA_FRAME)

    # Join cluster_event_log_actual_df with the full event log based on case concept:name
    # to find the corresponding actual trace records for the cluster
    cluster_event_log_actual_df = pd.merge(cluster_event_log_actual_df, full_log, left_on='Case ID', right_on='case:concept:name', how='inner')

    # Drop the additional supportive columns from the cluster event log 
    cluster_event_log_actual_df = cluster_event_log_actual_df.drop(columns=['Event Flow', 'Case ID'])

    return cluster_event_log_actual_df


# discover the process for a given event log
# using Heuristic Miner algorithm
def discover_process(event_log, is_event_log):

    # Convert the Data Frame into an EventLog if not
    if not is_event_log:
        event_log = log_converter.apply(event_log, variant = log_converter.Variants.TO_EVENT_LOG)

    # Discover the process using Heuristic miner
    process_model = heuristics_miner.apply_heu(event_log, parameters={heuristics_miner.Variants.CLASSIC.value.Parameters.DEPENDENCY_THRESH: 0.5})

    return process_model


# visualize a discovered process model
def visualize_process(process_model, save_file):

    # Visualize the process
    gviz = hn_visualizer.apply(process_model)
    hn_visualizer.view(gviz)

    # Save file to disk
    if save_file is not None:
        hn_visualizer.save(gviz, save_file)