"""
NER機能のテスト・デバッグスクリプト
"""

import pickle
from ner_extractor import PatentLawNER

def debug_pickle_structure():
    """Pickleファイルの構造を確認"""
    pickle_file = '334AC0000000121_20230703_505AC0000000051.pickle'
    
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    
    print("=== Pickleファイル構造 ===")
    print(f"データ型: {type(data)}")
    print(f"長さ: {len(data) if hasattr(data, '__len__') else 'N/A'}")
    
    if isinstance(data, list) and len(data) > 0:
        print(f"\n最初の要素:")
        first_item = data[0]
        print(f"  型: {type(first_item)}")
        
        if isinstance(first_item, dict):
            print(f"  キー: {list(first_item.keys())}")
            for key, value in first_item.items():
                if isinstance(value, str):
                    print(f"    {key}: '{value[:100]}...' ({len(value)} 文字)")
                else:
                    print(f"    {key}: {type(value)}")
        
        print(f"\n2番目の要素:")
        if len(data) > 1:
            second_item = data[1]
            print(f"  型: {type(second_item)}")
            if isinstance(second_item, dict):
                print(f"  キー: {list(second_item.keys())}")
                for key, value in second_item.items():
                    if isinstance(value, str):
                        print(f"    {key}: '{value[:100]}...' ({len(value)} 文字)")
                    else:
                        print(f"    {key}: {type(value)}")
    
    elif isinstance(data, dict):
        print(f"キー: {list(data.keys())}")
        for key, value in data.items():
            print(f"\n{key}:")
            if isinstance(value, list):
                print(f"  リスト長: {len(value)}")
                if len(value) > 0:
                    print(f"  最初の要素: {type(value[0])}")
                    if isinstance(value[0], dict):
                        print(f"  要素のキー: {list(value[0].keys())}")
            else:
                print(f"  型: {type(value)}")

def test_ner_on_sample():
    """サンプルテキストでNER機能をテスト"""
    ner = PatentLawNER()
    
    # テストサンプル
    sample_text = """
    第三十六条　特許出願人は、次に掲げる事項を記載した明細書を特許庁に提出しなければならない。
    一　発明の名称
    二　図面の簡単な説明
    前項の明細書には、政令で定めるところにより、請求項に記載した発明が発明者によってされたものであることを証明する書面を添付しなければならない。
    """
    
    print("\n=== NERテスト ===")
    print(f"テストテキスト: {sample_text[:100]}...")
    
    entities = ner.extract_entities(sample_text)
    
    for category, entity_list in entities.items():
        if entity_list:
            print(f"\n{category}: {len(entity_list)}個")
            for entity in entity_list[:3]:  # 最初の3個を表示
                print(f"  - {entity['text']} (位置: {entity['start']}-{entity['end']})")

if __name__ == "__main__":
    debug_pickle_structure()
    test_ner_on_sample()
