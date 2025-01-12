import pandas as pd 
from shared_func.ec2_func import *

df = list_ec2_instances()

if df is not None:
    # Save the DataFrame to a CSV file (optional)
    output_file = "ec2_instances.csv"
    df.to_csv(output_file, index=False)
    print(f"Instance details saved to {output_file}")
