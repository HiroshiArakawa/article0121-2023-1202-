"""
第64条の期間表現テスト
"""

from ner_extractor import PatentLawNER

# 第64条のテキスト
text = "第六十四条 特許庁長官は、特許出願の日から一年六月を経過したときは、特許掲載公報の発行をしたものを除き、その特許出願について出願公開をしなければならない。次条第一項に規定する出願公開の請求があつたときも、同様とする。"

ner = PatentLawNER()
entities = ner.extract_entities(text)

print("=== 第64条のNER解析結果 ===")
for category, items in entities.items():
    if items:
        print(f"\n【{category}】")
        for item in items:
            print(f"  - '{item['text']}' (位置: {item['start']}-{item['end']})")

print("\n=== TIME_PERIOD の詳細確認 ===")
if 'TIME_PERIOD' in entities:
    time_entities = entities['TIME_PERIOD']
    print(f"抽出された時間表現数: {len(time_entities)}")
    for item in time_entities:
        print(f"  - '{item['text']}'")
else:
    print("TIME_PERIOD が見つかりませんでした")

# 「一年六月」が含まれているかチェック
target = "一年六月"
if target in text:
    print(f"\n「{target}」はテキスト内に存在します")
    found = False
    for category, items in entities.items():
        for item in items:
            if target in item['text']:
                print(f"「{target}」は {category} として抽出されました: '{item['text']}'")
                found = True
    if not found:
        print(f"「{target}」は固有表現として抽出されていません ❌")
else:
    print(f"「{target}」はテキスト内に見つかりません")
