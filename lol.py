import pandas as pd

# Read the CSV file
input_file_path = 'G:/225 data.csv'
df = pd.read_csv(input_file_path)

# Aggregate data based on the 'emails' column
aggregated_df = df.groupby('email').agg('sum').reset_index()

# Save the aggregated data to a new CSV file
output_file_path = 'G:/aggregated_data_225.csv'
aggregated_df.to_csv(output_file_path, index=False)
