#!/usr/bin/env python3
"""
修正されたNERで既存のPickleデータを再処理
"""

from ner_extractor import PatentLawNER
import pickle

def update_ner_data():
    """既存のPickleデータを修正されたNERで再処理"""
    
    # NERエクストラクター初期化
    ner = PatentLawNER()
    
    # 元のPickleファイルを読み込み
    input_file = '334AC0000000121_20230703_505AC0000000051.pickle'
    output_file = '334AC0000000121_20230703_505AC0000000051_with_ner_fixed.pickle'
    
    print(f"=== 修正されたNERでデータ再処理 ===")
    print(f"入力ファイル: {input_file}")
    print(f"出力ファイル: {output_file}")
    print()
    
    try:
        # 全条文の解析
        processed_data = ner.process_all_articles(input_file)
        
        # 解析結果をPickleファイルに保存
        with open(output_file, 'wb') as f:
            pickle.dump(processed_data, f)
        print(f"✅ 修正済み固有表現解析データを {output_file} に保存しました")
        
        # CSV出力
        csv_output = 'patent_law_ner_results_fixed.csv'
        df = ner.export_ner_results_to_csv(processed_data, csv_output)
        
        # 統計情報表示
        print("\n=== 修正後の固有表現抽出統計 ===")
        if len(df) > 0:
            category_counts = df['category'].value_counts()
            for category, count in category_counts.items():
                print(f"{category}: {count}個")
            print(f"\n合計: {len(df)}個の固有表現を抽出しました")
            
            # 第一条の「この法律」を確認
            first_article_law_refs = df[
                (df['category'] == 'LAW_REFERENCE') & 
                (df['entity_text'] == 'この法律')
            ]
            if len(first_article_law_refs) > 0:
                print(f"\n🎉 「この法律」が {len(first_article_law_refs)} 箇所で抽出されました！")
                for _, row in first_article_law_refs.iterrows():
                    print(f"  - 条文: {row['article_title']}")
            else:
                print("\n⚠️ 「この法律」が抽出されませんでした")
        else:
            print("固有表現が抽出されませんでした。")
            
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_ner_data()
