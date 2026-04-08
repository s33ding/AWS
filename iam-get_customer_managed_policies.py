import sys
from shared_func.iam_func import *

pd.set_option('display.max_colwidth', None)

# Call the function
df = get_customer_managed_policies()
df = df.sort_values(by="UpdateDate",ascending=False)


# Display the DataFrame
print(df)

