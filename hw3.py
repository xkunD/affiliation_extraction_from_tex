import numpy as np
import networkx as nx

# Define the adjacency matrix based on the railway network in the image
adj_matrix = np.array([
    [ 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 1  (Berlin)
    [ 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # 2  (Frankfurt)
    [ 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],  # 3  (Cologne)
    [ 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],  # 4  (Amsterdam)
    [ 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],  # 5  (brussels)
    [ 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],  # 6  (London)
    [ 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],  # 7  (Paris)
    [ 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],  # 8  (Madrid)
    [ 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],  # 9  (Barcelona)
    [ 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],  # 10 (Lyon)
    [ 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],  # 11 (Milan)
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]   # 12 (Rome)
])

# Create a graph from the adjacency matrix
G = nx.from_numpy_array(adj_matrix)

# 1. Check if the graph is acyclic and periodic
is_acyclic = nx.is_directed_acyclic_graph(G)  # Works only for directed graphs (False here)

# 2. Find the shortest path between Lyon (10) and Amsterdam (4)
shortest_path_length = nx.shortest_path_length(G, source=9, target=3)  # Adjusted for 0-based index

# 3. Count paths from Madrid (8) to Milan (11) within 4 and 8 links
paths_madrid_milan_4 = list(nx.all_simple_paths(G, source=7, target=10, cutoff=4))
paths_madrid_milan_8 = list(nx.all_simple_paths(G, source=7, target=10, cutoff=8))

# Count routes from London (6) to Frankfurt (2) with strictly less than 7 links
A_power_2 = np.linalg.matrix_power(adj_matrix, 2) 
print('2: ', A_power_2[1,5])
A_power_3 = np.linalg.matrix_power(adj_matrix, 3) 
print('3: ', A_power_3[1,5])
A_power_4 = np.linalg.matrix_power(adj_matrix, 4)   
print('4: ', A_power_4[1,5])
A_power_5 = np.linalg.matrix_power(adj_matrix, 5)  
print('5: ', A_power_5[1,5])
A_power_6 = np.linalg.matrix_power(adj_matrix, 6) 
print('6: ', A_power_6[1,5])

routes_london_frankfurt = A_power_2[1,5]+A_power_3[1,5]+A_power_4[1,5]+A_power_5[1,5]+A_power_6[1,5]
print("Routes from London to Frankfurt with strictly less than 7 links:", routes_london_frankfurt)


# Print results
print("1. Is the graph acyclic?", is_acyclic)
print("2. Shortest path from Lyon to Amsterdam:", shortest_path_length, "links")
print("3. Paths from Madrid to Milan:")
print("   - In 4 links:", len(paths_madrid_milan_4))
print("   - In 8 links:", len(paths_madrid_milan_8))
print("4. Routes from London to Frankfurt with strictly less than 7 links:", routes_london_frankfurt)
