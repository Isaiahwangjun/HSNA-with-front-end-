import pandas as pd
import json


def relationMatrix(json_path, protagonist):
    # 讀取.json文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取所有的 person
    all_persons = []
    for diary_entry in data:
        diary_entries = diary_entry.get('日記', [])
        for entry in diary_entries:
            all_persons.extend(entry.get('person', []))

    # 去除重複的 person 並保持原始順序
    unique_persons = []
    for person in all_persons:
        if person not in unique_persons:
            unique_persons.append(person)

    # 创建空白的关系矩阵 DataFrame
    df_relationship = pd.DataFrame(index=[protagonist] + unique_persons,
                                   columns=[protagonist] + unique_persons)
    df_relationship = df_relationship.fillna(0)  # 将所有值初始化为0

    # 对每条记录中的人物进行关系填充
    for diary_entry in data:
        diary_entries = diary_entry.get('日記', [])
        for entry in diary_entries:
            persons_in_entry = entry.get('person', [])
            # 将主角与每个出现的人物之间的关系加1
            for person in persons_in_entry:
                df_relationship.at[protagonist, person] += 1
                df_relationship.at[person, protagonist] += 1

            for person1 in persons_in_entry:
                for person2 in persons_in_entry:
                    if person1 != person2:
                        # 將兩人之間的關係強度加1
                        df_relationship.at[person1, person2] += 1
    # 將 DataFrame 寫入 Excel 文件
    excel_output_path = 'output/relationship_matrix.xlsx'
    df_relationship.to_excel(excel_output_path)


def change():
    # 讀取關係矩陣 Excel 檔案
    rela_file = 'output/relationship_matrix.xlsx'
    df = pd.read_excel(rela_file, index_col=0)  # 將第一欄設為索引

    # 創建一個新的 DataFrame 來存儲轉換後的點線表示法資料
    lines_df = pd.DataFrame(columns=['srcId', 'srcLabel', 'dstId', 'dstLabel'])

    # 用集合來存儲已經處理過的關係
    processed_relations = set()

    # 對每一行進行處理，將關係轉換為線
    for source, row in df.iterrows():
        for target, value in row.items():
            if source != target and value > 0:  # 確保 source 和 target 不同，並且關係值大於0
                # 判斷這條關係是否已經處理過（如果 source 和 target 順序相反，則只處理一次）
                relation = frozenset([source, target])
                if relation not in processed_relations:
                    new_row = {'srcLabel': source, 'dstLabel': target}
                    lines_df = pd.concat(
                        [lines_df, pd.DataFrame(new_row, index=[0])],
                        ignore_index=True)
                    # 將這條關係添加到已處理的集合中
                    processed_relations.add(relation)

    # 將結果寫入新的 Excel 檔案
    output_file = 'output/draw.xlsx'
    lines_df.to_excel(output_file, index=False)
