import pandas as pd
from mlxtend.frequent_patterns import fpgrowth


## Mine frequent patterns using mlxtend fpgrowth
def mine_frequent_variants(transactions_chunk, min_support):
    # Covnert to a Pandas dataframe
    transactions_chunk_df = pd.DataFrame(transactions_chunk)
    # Encode to a boolen list for the ease of computation in FPGRowth
    transactions_chunk_df = pd.get_dummies(transactions_chunk_df.stack()).astype('bool').groupby(level=0).sum()
    # Mine frequent flow variants for the chunk
    frequent_variants_chunk = fpgrowth(transactions_chunk_df.astype('bool'), min_support=min_support, use_colnames=True)
    
    return frequent_variants_chunk
