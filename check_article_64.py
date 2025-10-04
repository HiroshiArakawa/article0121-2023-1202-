"""
第64条が含まれているかデータ構造を確認
"""

import pickle
from ner_extractor import PatentLawNER

# 元のPickleファイルを読み込み
pickle_file = "334AC0000000121_20230703_505AC0000000051.pickle"

with open(pickle_file, 'rb') as f:
    data = pickle.load(f)

print(f"=== データ構造確認 ===")
print(f"総データ数: {len(data)}")

# 第64条を探す
found_64 = None
for i, article in enumerate(data):
    # article_numberが64または「六十四」を含むものを探す
    article_num = str(article.get('article_number', ''))
    title = str(article.get('title', ''))
    body = str(article.get('body', ''))
    
    if ('64' in article_num or '六十四' in article_num or 
        '六十四条' in title or '六十四条' in body):
        found_64 = article
        print(f"\n✅ 第64条を発見！ (インデックス: {i})")
        print(f"Article Number: {article.get('article_number', 'N/A')}")
        print(f"Title: {article.get('title', 'N/A')}")
        
        # bodyから「一年六月」を含む部分を抽出
        if 'body' in article and '一年六月' in article['body']:
            print(f"✅ 'body'に「一年六月」が含まれています")
            # 前後50文字を表示
            body_text = article['body']
            index = body_text.find('一年六月')
            if index != -1:
                start = max(0, index - 50)
                end = min(len(body_text), index + 50)
                context = body_text[start:end]
                print(f"コンテキスト: ...{context}...")
        break

if found_64:
    print(f"\n=== 第64条でNER解析テスト ===")
    ner = PatentLawNER()
    entities = ner.analyze_article_text(found_64)
    
    if 'ner_entities' in entities and 'TIME_PERIOD' in entities['ner_entities']:
        time_entities = entities['ner_entities']['TIME_PERIOD']
        print(f"TIME_PERIOD抽出数: {len(time_entities)}")
        for entity in time_entities:
            print(f"  - '{entity['text']}'")
            if '一年六月' in entity['text']:
                print(f"    ✅ 「一年六月」を含む表現が抽出されました！")
    else:
        print("❌ TIME_PERIOD が抽出されませんでした")
else:
    print("❌ 第64条が見つかりませんでした")
    
    # データサンプルを表示
    print("\n=== データサンプル ===")
    for i, article in enumerate(data[:5]):
        print(f"[{i}] Article Number: {article.get('article_number', 'N/A')}")
        print(f"    Title: {article.get('title', 'N/A')}")
        print(f"    Keys: {list(article.keys())}")
        print()
