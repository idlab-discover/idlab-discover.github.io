import pandas as pd

# Read the CSV file with newline ('\n') as the delimiter
# Replace 'your_csv_file.csv' with the actual path to your CSV file
df = pd.read_csv('members.csv', delimiter=',', header=None)

# Define a function to create the CQL query
def create_cql_query(author_name):
    return f'author exact "{author_name}"'

# Apply the function to each row in the DataFrame and join the results with " or "
cql_queries = df[0].apply(create_cql_query)
full_query = ' or '.join(cql_queries)

# Print the final CQL query
print(full_query)
