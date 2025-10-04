"""
第64条のNERエンティティ詳細確認
"""

import pickle

# 改善されたPickleファイルを読み込み
with open('334AC0000000121_20230703_505AC0000000051_with_ner_improved.pickle', 'rb') as f:
    data = pickle.load(f)

# 第64条を取得
chapter_3_2 = data[3]  # 第三章の二　出願公開
article_64 = chapter_3_2['articles'][0]  # 第64条

print("=== 第64条の詳細 ===")
print(f"Title: {article_64.get('title', 'N/A')}")
print(f"Keys: {list(article_64.keys())}")

if 'clean_text' in article_64:
    clean_text = article_64['clean_text']
    print(f"Clean text preview: {clean_text[:100]}...")
    if '一年六月' in clean_text:
        print("✅ Clean textに「一年六月」が含まれています")
    else:
        print("❌ Clean textに「一年六月」が含まれていません")

if 'ner_entities' in article_64:
    entities = article_64['ner_entities']
    print(f"\n=== NER Entities ===")
    
    for category, items in entities.items():
        if items:
            print(f"\n【{category}】({len(items)}個)")
            for item in items:
                print(f"  - '{item['text']}' (位置: {item['start']}-{item['end']})")
                if '一年六月' in item['text']:
                    print(f"    🎯 「一年六月」を含む！")
    
    # TIME_PERIODを特別にチェック
    if 'TIME_PERIOD' in entities:
        time_entities = entities['TIME_PERIOD']
        has_target = any('一年六月' in entity['text'] for entity in time_entities)
        if has_target:
            print(f"\n🎉 「一年六月」がTIME_PERIODとして抽出されています！")
        else:
            print(f"\n⚠️ 「一年六月」はTIME_PERIODに含まれていません")
else:
    print("❌ ner_entitiesが存在しません")

# 元のbodyも確認
if 'body' in article_64:
    body = article_64['body']
    if '一年六月' in body:
        print(f"\n📝 元のbodyに「一年六月」が含まれています")
        # 「一年六月」周辺のテキストを表示
        index = body.find('一年六月')
        start = max(0, index - 30)
        end = min(len(body), index + 50)
        context = body[start:end]
        print(f"Context: ...{context}...")
    else:
        print(f"\n❌ 元のbodyに「一年六月」が含まれていません")
