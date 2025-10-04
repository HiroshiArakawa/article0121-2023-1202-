"""
「一年六月」の抽出確認
"""

import pandas as pd

# 改善されたCSVファイルを読み込み
csv_file = "patent_law_ner_results_improved.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

print("=== 「一年六月」の抽出確認 ===")

# 「一年六月」を検索
target = "一年六月"
matches = df[df['text'] == target]

if len(matches) > 0:
    print(f"✅ 「{target}」が抽出されています！")
    for _, row in matches.iterrows():
        print(f"  - 第{row['article_number']}条 ({row['category']})")
        print(f"    位置: {row['start']}-{row['end']}")
else:
    print(f"❌ 「{target}」は抽出されていません")

# TIME_PERIODカテゴリの複合期間表現を確認
print("\n=== TIME_PERIOD の複合期間表現 ===")
time_periods = df[df['category'] == 'TIME_PERIOD']
compound_periods = time_periods[time_periods['text'].str.contains('年.*月', regex=True)]

print(f"複合期間表現: {len(compound_periods)}個")
for _, row in compound_periods.head(10).iterrows():
    print(f"  - '{row['text']}' (第{row['article_number']}条)")

# 「年六月」パターンの表現を特別に確認
year_month_pattern = time_periods[time_periods['text'].str.contains('年六月', regex=True)]
print(f"\n「年六月」パターン: {len(year_month_pattern)}個")
for _, row in year_month_pattern.iterrows():
    print(f"  - '{row['text']}' (第{row['article_number']}条)")
