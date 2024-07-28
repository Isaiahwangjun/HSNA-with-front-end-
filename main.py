import pandas as pd
import response
import prompt
import json
from dotenv import load_dotenv
import os
from openai import OpenAI
import relation
import relatest
import time


def main():
    start_time = time.time()

    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    file = 'diary_lxt_.csv'
    df = pd.read_csv(file, usecols=['content'])

    json_path = 'output/capture.json'  # 在迴圈之外打開檔案

    with open(json_path, 'w', encoding='utf-8') as output:
        output.write('[')

        for i, content_value in enumerate(df['content'].head(5)):
            user_message = """將下列文章填入格式中，並以json輸出: """ + content_value
            system_message, rule = prompt.get_prompt()

            response_ = response.create_completion(client, system_message,
                                                   user_message, rule)

            result = json.loads(response_.choices[0].message.content)
            json.dump(result, output, ensure_ascii=False)

            if i < len(df['content'].head(5)) - 1:
                output.write(',\n')

        output.write(']')
    end_time = time.time()
    print("執行時間:", end_time - start_time, "秒")
    # for content_value in df['content']:
    #     user_message = """將下列文章填入格式中，並以json輸出: """ + content_value
    #     system_message, rule = prompt.get_prompt()

    #     response_ = response.create_completion(client, system_message,
    #                                            user_message, rule)

    #     result = json.loads(response_.choices[0].message.content)

    #     json_path = f'test.json'
    #     with open(json_path, 'w', encoding='utf-8') as output:
    #         json.dump(result, output, ensure_ascii=False)


def api_main(ocr_result):
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    user_message = """將下列文章填入格式中，並以json輸出: """ + ocr_result
    system_message, rule = prompt.get_prompt()

    response_ = response.create_completion(client, system_message,
                                           user_message, rule)

    result = response_.choices[0].message.content
    result_write = json.loads(response_.choices[0].message.content)
    json_path = 'api_test.json'
    print(ocr_result)
    print(result)
    with open(json_path, 'w', encoding='utf-8') as output:
        output.write('[')
        json.dump(result_write, output, ensure_ascii=False)
        output.write(']')

    relatest.relationMatrix(json_path, '蔡培火')
    relatest.change()

    return result


if __name__ == "__main__":
    main()
    relation.generate()
