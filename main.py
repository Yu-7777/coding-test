import sys

# 入力の受付
def data_reading():
    compliant_input = []
    for line in sys.stdin:
        start, end, dist = map(float, line.strip().split(','))
        compliant_input.append((start, end, dist))

    return compliant_input

# idx key, station value
def linkage_idx_station(compliant_input):
    all_stations = set()
    linked_dict = {}
    for start, end, dist in compliant_input:
        all_stations.add(start)
        all_stations.add(end)

    for idx, station in enumerate(sorted(all_stations)):
        linked_dict[idx] = station

    return linked_dict

# station key, idx value
def linkage_station_idx(linked_dict):
    return {v: k for k, v in linked_dict.items()}

# インデックスと駅IDの対応した隣接行列の作成
def create_adjacent_matrix(num_nodes, compliant_input, station_key_linked_dict):
    node_map = [[-1 for _ in range(num_nodes)] for _ in range(num_nodes)]

    for start, end, dist in compliant_input:
        node_map[station_key_linked_dict[start]][station_key_linked_dict[end]] = dist

    return node_map

# テーブルの初期化
def init_array(num_nodes):
    return [[-1 for _ in range(num_nodes)] for _ in range(2**num_nodes)]

# 動的計画法の実施
def dynamic_programming(adj, num_nodes):
    dp_table = init_array(num_nodes)
    route_hist = init_array(num_nodes)

    for i in range(num_nodes):
        dp_table[1 << i][i] = 0.0

    for row in range(1, 1 << num_nodes):
        for col in range(num_nodes):
            if dp_table[row][col] == -1:
                continue
            for j in range(num_nodes):
                if not (row & (1 << j)) and adj[col][j] != -1:
                    new_row = row | (1 << j)
                    new_col = j

                    new_dist = dp_table[row][col] + adj[col][j]

                    if new_dist > dp_table[new_row][new_col]:
                        dp_table[new_row][new_col] = new_dist
                        route_hist[new_row][new_col] = col

    return dp_table, route_hist

if __name__ == "__main__":
    compliant_input = data_reading()
    idx_to_station = linkage_idx_station(compliant_input)
    station_to_idx = linkage_station_idx(idx_to_station)
    num_nodes = len(idx_to_station)
    adj_matrix = create_adjacent_matrix(num_nodes, compliant_input, station_to_idx)
    dp_table, parent = dynamic_programming(adj_matrix, num_nodes)

    # 最大取得
    final_mask, end_node_idx = max(
        ((mask, i) for mask in range(1, 1 << num_nodes) for i in range(num_nodes)),
        key=lambda item: dp_table[item[0]][item[1]]
    )

    # 復元
    path = []
    while end_node_idx != -1:
        path.append(str(int(idx_to_station[end_node_idx])))
        prev_node = parent[final_mask][end_node_idx]
        final_mask ^= (1 << end_node_idx)
        end_node_idx = prev_node

    print("\r\n".join(path[::-1]))