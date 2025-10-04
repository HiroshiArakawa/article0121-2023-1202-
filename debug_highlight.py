"""
ハイライト表示のテストとデバッグ
"""

from app_with_ner import highlight_entities
import pickle

# テスト用のサンプルテキストとエンティティ
test_text = "第六十四条 特許庁長官は、特許出願の日から一年六月を経過したときは、特許掲載公報の発行をしたものを除き、その特許出願について出願公開をしなければならない。"

test_entities = {
    'TIME_PERIOD': [
        {'text': '一年六月', 'start': 21, 'end': 25}
    ],
    'ORGANIZATION': [
        {'text': '特許庁長官', 'start': 6, 'end': 11}
    ],
    'PROCEDURE': [
        {'text': '出願', 'start': 15, 'end': 17}
    ]
}

print("=== ハイライト表示テスト ===")
print(f"元テキスト: {test_text}")
print()

highlighted = highlight_entities(test_text, test_entities)
print("ハイライト結果:")
print(highlighted)
print()

# 実際のPickleデータからテスト
print("=== 実際のデータでのテスト ===")
try:
    with open('334AC0000000121_20230703_505AC0000000051_with_ner_hierarchical.pickle', 'rb') as f:
        data = pickle.load(f)
    
    # 第64条を取得
    chapter_3_2 = data[3]  # 第三章の二　出願公開
    article_64 = chapter_3_2['articles'][0]  # 第64条
    
    from app_with_ner import get_article_text
    
    # クリーンテキストを取得
    clean_text = get_article_text(article_64)
    print(f"クリーンテキスト: {clean_text[:100]}...")
    
    if 'ner_entities' in article_64:
        # ハイライト処理
        highlighted_real = highlight_entities(clean_text, article_64['ner_entities'])
        print(f"\nハイライト結果（最初の200文字）:")
        print(highlighted_real[:200])
        
        # 「一年六月」が含まれているかチェック
        if '一年六月' in highlighted_real:
            print("\n✅ 「一年六月」が含まれています")
            # 「一年六月」周辺を表示
            start_idx = highlighted_real.find('一年六月')
            if start_idx != -1:
                context_start = max(0, start_idx - 30)
                context_end = min(len(highlighted_real), start_idx + 100)
                context = highlighted_real[context_start:context_end]
                print(f"コンテキスト: ...{context}...")
        else:
            print("\n❌ 「一年六月」が見つかりません")
    else:
        print("❌ NERエンティティが存在しません")
        
except Exception as e:
    print(f"エラー: {e}")

# HTMLエスケープの問題をチェック
print("\n=== HTMLエスケープチェック ===")
sample_html = '<span style="color: red;">テスト</span>'
print(f"HTMLサンプル: {sample_html}")

# Streamlitでの表示方法のテスト
print("\n=== Streamlit表示方法の違い ===")
print("st.markdown(text) - HTMLタグがエスケープされる")
print("st.markdown(text, unsafe_allow_html=True) - HTMLタグが解釈される")
