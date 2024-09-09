# import re
# from collections import defaultdict

# def parse_goal_file(file_path):
#     graphs = defaultdict(lambda: {'nodes': set(), 'edges': []})
#     task_infos = defaultdict(lambda: defaultdict(dict))
#     current_rank = None
#     current_channel = None  ## tag

#     with open(file_path, 'r') as file:
#         for line in file:
#             line = line.strip()

#             if line.startswith("rank"):
#                 current_rank = re.match(r"rank (\d+)", line).group(1)

#             elif line.startswith("l"):
#                 match = re.match(r"(l\d+):(.*)", line)
#                 if match:
#                     node = match.group(1)
#                     task_infos[current_rank][node] = match.group(2).strip()
#                     if "send" in line or "recv" in line:
#                         current_channel = re.search(r"tag (\d+)", line).group(1)
#                         if current_rank is not None and current_channel is not None:
#                             graphs[(current_rank, current_channel)]['nodes'].add(node)
#                     elif "calc" in line:
#                         if current_rank is not None and current_channel is not None:
#                             graphs[(current_rank, current_channel)]['nodes'].add(node)

#                 else:        
#                     if "requires" in line or "irequires" in line:
#                         match = re.match(r"(l\d+) (i?requires) (l\d+)", line)
#                         if match:
#                             src, edge_type, dst = match.groups()
#                             if current_rank is not None and current_channel is not None:
#                                 graphs[(current_rank, current_channel)]['edges'].append((src, dst, edge_type))
    
#     for (rank, channel), graph_data in graphs.items():
#         print(f"(rank {rank}, channel {channel}):")
#         for key, value in graph_data.items():
#             print(f"    {key}:")
#             for data in value:
#                 print(f"        {data}")

#     return graphs, task_infos

# def generate_graphviz(graphs, task_infos):
#     graphviz_input = "digraph G {\n"
#     graphviz_input += "    rankdir=LR;\n"

#     for (rank, channel), graph_data in graphs.items():
#         subgraph_name = f"cluster_rank_{rank}_channel_{channel}"
#         graphviz_input += f'    subgraph "{subgraph_name}" {{\n'
#         graphviz_input += f'        label = "Rank {rank} Channel {channel}";\n'

#         for node in graph_data['nodes']:
#             unique_node = f"{node}_rank{rank}: {task_infos[rank][node]}"
#             graphviz_input += f'        "{unique_node}";\n'

#         for src, dst, edge_type in graph_data['edges']:
#             unique_src = f"{src}_rank{rank}: {task_infos[rank][src]}"
#             unique_dst = f"{dst}_rank{rank}: {task_infos[rank][dst]}"
#             color = "black" if edge_type == "requires" else "red"
#             graphviz_input += f'        "{unique_dst}" -> "{unique_src}" [label="{edge_type}", color="{color}"];\n'

#         graphviz_input += "    }\n"

#     graphviz_input += "}\n"
#     return graphviz_input

# def main():
#     input_file = "example_2.goal" 
#     output_file = "example_2.dot"

#     graphs, task_infos = parse_goal_file(input_file)
#     graphviz_input = generate_graphviz(graphs, task_infos)

#     with open(output_file, 'w') as file:
#         file.write(graphviz_input)

#     print(f"Graphviz output written to {output_file}")

# if __name__ == "__main__":
#     main()

import re
from collections import defaultdict

def parse_goal_file(file_path):
    # 将 graphs 修改为每个 rank 一个子图
    graphs = defaultdict(lambda: {'nodes': set(), 'edges': []})
    task_infos = defaultdict(lambda: defaultdict(dict))
    current_rank = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # 处理 rank 信息
            if line.startswith("rank"):
                current_rank = re.match(r"rank (\d+)", line).group(1)

            elif line.startswith("l"):
                match = re.match(r"(l\d+):(.*)", line)
                if match:
                    node = match.group(1)
                    task_infos[current_rank][node] = match.group(2).strip()
                    # 将所有任务的节点添加到当前 rank 的子图中
                    graphs[current_rank]['nodes'].add(node)

                else:        
                    # 处理边的依赖关系
                    if "requires" in line or "irequires" in line:
                        match = re.match(r"(l\d+) (i?requires) (l\d+)", line)
                        if match:
                            src, edge_type, dst = match.groups()
                            graphs[current_rank]['edges'].append((src, dst, edge_type))

    # 输出结果
    for rank, graph_data in graphs.items():
        print(f"(rank {rank}):")
        for key, value in graph_data.items():
            print(f"    {key}:")
            for data in value:
                print(f"        {data}")

    return graphs, task_infos

def generate_graphviz(graphs, task_infos):
    graphviz_input = "digraph G {\n"
    graphviz_input += "    rankdir=LR;\n"

    for rank, graph_data in graphs.items():
        subgraph_name = f"cluster_rank_{rank}"
        graphviz_input += f'    subgraph "{subgraph_name}" {{\n'
        graphviz_input += f'        label = "Rank {rank}";\n'

        for node in graph_data['nodes']:
            unique_node = f"{node}_rank{rank}: {task_infos[rank][node]}"
            graphviz_input += f'        "{unique_node}";\n'

        for src, dst, edge_type in graph_data['edges']:
            unique_src = f"{src}_rank{rank}: {task_infos[rank][src]}"
            unique_dst = f"{dst}_rank{rank}: {task_infos[rank][dst]}"
            color = "black" if edge_type == "requires" else "red"
            graphviz_input += f'        "{unique_dst}" -> "{unique_src}" [label="{edge_type}", color="{color}"];\n'

        graphviz_input += "    }\n"

    graphviz_input += "}\n"
    return graphviz_input

def main():
    input_file = "example_2.goal" 
    output_file = "example_2.dot"

    graphs, task_infos = parse_goal_file(input_file)
    graphviz_input = generate_graphviz(graphs, task_infos)

    with open(output_file, 'w') as file:
        file.write(graphviz_input)

    print(f"Graphviz output written to {output_file}")

if __name__ == "__main__":
    main()