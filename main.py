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


# 3) Visualize the network

import networkx as nx
import matplotlib.pyplot as plt

# Assuming 'network' is your list of edges
first_5_edges = network[:5]  # Get the first 5 edges

# Create a new directed graph for the subgraph
G_sub = nx.DiGraph()

# Add only the first 5 edges to the subgraph
for edge in first_5_edges:
    reverter, reverted, time, seniority_reverter, seniority_reverted = edge
    G_sub.add_edge(reverter, reverted, time=time, seniority_diff=seniority_reverter - seniority_reverted)

# Use a layout algorithm to position the nodes. spring_layout is a good start
pos = nx.spring_layout(G_sub)

# Draw the nodes and edges with custom options
nx.draw(G_sub, pos, with_labels=True, node_color='skyblue', node_size=2500, font_size=10, edge_color='gray', width=2)

# Add edge labels to show time of revert
edge_labels = nx.get_edge_attributes(G_sub, 'time')
nx.draw_networkx_edge_labels(G_sub, pos, edge_labels=edge_labels, font_color='red')

plt.axis('off')  # Turn off the axis
plt.show()

