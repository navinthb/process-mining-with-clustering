import pm4py
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter


# Perform conformance check by using token based replay method
def get_conformance(process_model, cluster_event_log, is_event_log):

    # Convert the Data Frame into an EventLog, if not
    if not is_event_log:
        cluster_event_log = log_converter.apply(cluster_event_log, variant = log_converter.Variants.TO_EVENT_LOG)
    # GEnerate a petrinet from the full proces model
    petri_net, initial_marking_, final_marking = pm4py.convert_to_petri_net(process_model)

    # CAlcualte finess & precision values of the cluster event log against full process model 
    # using the token based replay method 
    fitness = pm4py.fitness_token_based_replay(cluster_event_log, petri_net, initial_marking_, final_marking)
    precision = pm4py.precision_token_based_replay(cluster_event_log, petri_net, initial_marking_, final_marking)

    return fitness, precision

# Perform conformance check by using alignment-based
