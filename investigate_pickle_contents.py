"""
pickleファイルの内容を調査するスクリプト
"""

import pickle

def main():
    # pickleファイルを読み込み
    pickle_file = "334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle"
    
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
        print(f"pickleファイル読み込み成功: {len(data)}件")
    except FileNotFoundError:
        print(f"エラー: {pickle_file} が見つかりません")
        return
    
    # 最初の10件を確認
    print("\n=== データ構造の確認（最初の10件） ===")
    for i, item in enumerate(data[:10]):
        print(f"\n{i+1}. タイプ: {type(item)}")
        if isinstance(item, dict):
            print(f"   キー: {list(item.keys())}")
            if 'article_number' in item:
                print(f"   条文番号: {item['article_number']}")
            if 'title' in item:
                print(f"   タイトル: {item['title']}")
            # 文字列に64が含まれているかチェック
            for key, value in item.items():
                if isinstance(value, str) and '64' in value:
                    print(f"   '64'を含むフィールド {key}: {value[:100]}...")
        
    # 第64条を検索（より広範囲）
    print(f"\n=== 64条関連の検索結果 ===")
    found_64_items = []
    for i, item in enumerate(data):
        if isinstance(item, dict):
            # 様々なフィールドで64を検索
            for key, value in item.items():
                if isinstance(value, str) and ('64' in value or '六十四' in value):
                    found_64_items.append((i, key, value))
                    print(f"位置{i}, フィールド'{key}': {value[:200]}...")
    
    print(f"\n見つかった64関連項目: {len(found_64_items)}件")

if __name__ == "__main__":
    main()
