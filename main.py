# 1) Load the data

# open txt file and read lines into a list
# Initialize an empty dictionary to store column-wise data
wiki_data = {
    "title": [],
    "time": [],
    "revert": [],
    "version": [],
    "user": [],
}

try:
    with open('./rowiki_2006.txt', 'r') as file:
        # Skip the header line if it exists
        next(file)

        for line in file:
            fields = line.strip().split('\t')

            # Validate the number of fields
            if len(fields) != 5:
                print(f"Malformed line: {line}")
                continue

            wiki_data["title"].append(fields[0])
            wiki_data["time"].append(fields[1])
            wiki_data["revert"].append(int(fields[2]))  # Convert to integer
            wiki_data["version"].append(int(fields[3]))  # Convert to integer
            wiki_data["user"].append(fields[4])


except IOError as e:
    print(f"Error reading file: {e}")

# Print the resulting dictionary
# print("The first 10 titles are:")
# print(wiki_data["title"][:10])
# print("The first 10 times are:")
# print(wiki_data["time"][:10])
# print("The first 10 revert values are:")
# print(wiki_data["revert"][:10])
# print("The first 10 versions are:")
# print(wiki_data["version"][:10])
# print("The first 10 users are:")
# print(wiki_data["user"][:10])

## Build the network
import math
from collections import defaultdict

network = []
edits_per_user = defaultdict(int)


for i in range(1, len(wiki_data["user"])):
    current_user = wiki_data["user"][i]
    previous_user = wiki_data["user"][i - 1]

    # Update edit counts (this should be done for every edit, revert or not)
    edits_per_user[current_user] += 1

    # Check if the current edit is a revert
    if wiki_data["revert"][i] == 1:
        # Skip self-reverts
        if current_user == previous_user:
            continue

        # Calculate seniority
        seniority_reverter = math.log10(max(1, edits_per_user[previous_user]))
        seniority_reverted = math.log10(max(1, edits_per_user[current_user]))

        # Add to network (reverter, reverted, time, seniority_reverter, seniority_reverted)
        network.append((previous_user, current_user, wiki_data["time"][i], seniority_reverter, seniority_reverted))


# Print first 5 data points
print("First 5 network edges:", network[:5])

# Print number of nodes and edges
nodes = set([edge[0] for edge in network] + [edge[1] for edge in network])
print("Number of nodes:", len(nodes))
print("Number of edges:", len(network))


import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add edges from your network data
# (For a large network, consider adding only a subset)
for edge in network[:100]:  # Example: Adding first 100 edges
    reverter, reverted, time, seniority_reverter, seniority_reverted = edge
    G.add_edge(reverter, reverted, time=time, seniority_diff=seniority_reverter - seniority_reverted)

# Plot the graph
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1500, font_size=8)
plt.title("Subset of Wikipedia Edit Reversion Network")
plt.show()
