
# Create a list of transactions based on
# the order of events present in each trace
# use concept:name as the key
def create_transactions(hospi_log):
    transactions_list = []

    # loop taces in the event log
    for trace in hospi_log:
        transaction = set()
        # loop all events in the tace
        for event in trace:
            # concept:name is the key for event in a transaction
            concept_name = event['concept:name']
            transaction.add(concept_name)
        transactions_list.append(transaction)

    return transactions_list