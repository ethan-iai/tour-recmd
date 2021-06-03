from graph import KnowledgeGraphHandler

if __name__ == '__main__':
    graph_handler = KnowledgeGraphHandler(
        province_path=r'C:\Users\18508\Desktop\111\province.txt',
        type_path=r'C:\Users\18508\Desktop\111\type.txt',
        name_path=r'C:\Users\18508\Desktop\111\name.txt'
    )

    line = input()
    if line and len(line) > 0:
        print(graph_handler(line))