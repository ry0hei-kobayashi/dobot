import openai
import numpy as np
import base64
import os


def ask_chatgpt_question():

    # OpenAI APIキーの設定
    openai.api_key = os.getenv('OPENAI_API_KEY')
        
    # 画像をbase64にエンコードする
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": [
                {"type": "text", "text": "3*3のグリッド上に数字付きのブロックが配置されています．各数字のブロックがグリッド上のどこに存在するのかを認識してください．またグリッド内に存在する数字を左上から順に\",\"区切りで出力してください．グリッド上にブロックが存在し無い箇所は0で表現してください．無駄な解説はなしで結果のみを出力してください．"},  # ここに質問を書く
                {"type": "image_url", "image_url":{"url": f"data:image/jpeg;base64,{base64_image}"}},  # 画像の指定の仕方がちょい複雑
            ]}
        ],
        max_tokens = 2000
    )
    # 回答のテキストを取得
    answer = response.choices[0].message.content
    return answer

def parse_response_to_grid(response):
    # レスポンスの文字列をカンマで分割し、数値に変換
    numbers = list(map(int, response.split(',')))
    # 3x3の三次元配列に変換
    grid = np.array(numbers).reshape((3, 3)).tolist()
    return grid


"""
input_image = "./IMG_5397.jpg"

# APIで質問を送信して回答を取得
response = ask_chatgpt_question(input_image)
print("ChatGPTの回答:", response)

# 回答を3x3の三次元配列に変換
grid = parse_response_to_grid(response)
print("3x3グリッド配列:\n", grid)
"""
