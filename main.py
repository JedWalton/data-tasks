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

# 2) Build the network
import math
from collections import defaultdict

# Initialize data structures
edits_per_user = defaultdict(int)
version_history = defaultdict(list)  # Stores tuples of (time, user, version before edit)
network = []

# Build version history and track all edits
for time, user, version in zip(wiki_data["time"], wiki_data["user"], wiki_data["version"]):
    edits_per_user[user] += 1
    # Store the current version and the version before the edit
    if len(version_history[version]) > 0:
        prev_version = version_history[version][-1][2]
    else:
        prev_version = None
    version_history[version].append((time, user, prev_version))

# Process for reverts
for time, user, revert, version in zip(wiki_data["time"], wiki_data["user"], wiki_data["revert"], wiki_data["version"]):
    if revert == 1:
        # Get the last time this version number occurred before the revert
        previous_versions = [entry for entry in version_history[version] if entry[0] < time]
        
        if previous_versions:
            _, prev_user, prev_version = previous_versions[-1]

            # Check for valid revert and exclude self-reverts
            if prev_version != version and user != prev_user:
                seniority_reverter = math.log10(max(1, edits_per_user[user]))
                seniority_reverted = math.log10(max(1, edits_per_user[prev_user]))

                # Add edge to the network
                network.append((user, prev_user, time, seniority_reverter, seniority_reverted))

# Output the network information
print("First 5 network edges:", network[:5])
print("Total number of edges:", len(network))
