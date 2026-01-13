import sys
import pandas as pd 

day = int(sys.argv[1])
print(f"running pipeline for day {day}")

df = pd.DataFrame({"Unit": [1,2], "Quantity": [3,4]})
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")

