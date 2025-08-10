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

    return dp_table


if __name__ == "__main__":
    adj, id_to_idx, idx_to_id, num_nodes = data_reading()

    print(adj)
    print(id_to_idx)
    print(idx_to_id)
    print(num_nodes)    if __name__ == "__main__":
        # 1. データの読み込み
        compliant_input = data_reading()
    
        # 2. ノードの情報を整理し、IDとインデックスの対応を作成
        idx_to_station = linkage_idx_station(compliant_input)
        station_to_idx = linkage_station_idx(idx_to_station)
        num_nodes = len(idx_to_station)
    
        # 3. 隣接行列を作成
        #    注意: 現在のcreate_adjacent_matrixは内部で再度data_readingを呼び出します。
        #    また、引数num_nodesを正しく使用していません。
        #    ここでは、既存の関数の動作を前提として呼び出します。
        adj_matrix = create_adjacent_matrix(num_nodes)
    
        # 4. 動的計画法でDPテーブルを計算
        #    注意: dynamic_programmingは引数adjを受け取りますが、内部で未使用です。
        dp_table = dynamic_programming(adj_matrix, num_nodes)
    
        # 5. DPテーブルの中から最大値（最長経路長）を探す
        max_dist = 0.0
        for row in dp_table:
            for dist in row:
                if dist > max_dist:
                    max_dist = dist
        
        # 6. 結果の出力
        print(max_dist)