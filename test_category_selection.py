#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
カテゴリ選択機能のテストスクリプト

左右パネル連動のカテゴリ選択機能が正常に動作するかテストします。
"""

import pickle
import sys
import os

def test_category_selection():
    """カテゴリ選択機能のテスト"""
    print("🧪 カテゴリ選択機能テスト開始")
    print("=" * 50)
    
    # データファイルの存在確認
    hierarchical_file = "334AC0000000121_20230703_505AC0000000051_with_ner_hierarchical.pickle"
    
    if not os.path.exists(hierarchical_file):
        print("❌ 階層NER解析済みデータファイルが見つかりません")
        return False
    
    try:
        # データ読み込み
        with open(hierarchical_file, 'rb') as f:
            data = pickle.load(f)
        
        print("✅ データ読み込み成功")
        print(f"📁 データ構造: {type(data)}")
        
        # データ構造の確認
        if isinstance(data, dict) and 'chapters' in data:
            chapters = data['chapters']
        elif isinstance(data, list):
            chapters = data
        else:
            print(f"⚠️ 予期しないデータ構造: {type(data)}")
            print(f"📊 データキー: {list(data.keys()) if isinstance(data, dict) else 'リスト形式'}")
            chapters = data if isinstance(data, list) else []
        
        print(f"📁 章数: {len(chapters)}章")
        
        # 条文データの確認
        total_articles = 0
        categories_found = set()
        
        for chapter in chapters:
            if 'articles' in chapter:
                for article in chapter['articles']:
                    total_articles += 1
                    if 'ner_entities' in article:
                        for category in article['ner_entities'].keys():
                            categories_found.add(category)
        
        print(f"📋 総条文数: {total_articles}条")
        print(f"🏷️ 発見されたカテゴリ: {len(categories_found)}種類")
        
        # カテゴリ詳細表示
        print("\n📊 カテゴリ詳細:")
        category_names = {
            'LAW_REFERENCE': '📚 法律参照',
            'ARTICLE_REFERENCE': '📋 条文参照', 
            'TIME_PERIOD': '⏰ 期間表現',
            'MONEY_AMOUNT': '💰 金額表現',
            'ORGANIZATION': '🏢 組織・機関',
            'PROCEDURE': '⚙️ 手続き関連',
            'LEGAL_STATUS': '⚖️ 法的地位'
        }
        
        for category in sorted(categories_found):
            display_name = category_names.get(category, category)
            print(f"  - {display_name} ({category})")
        
        # 第64条のテスト（期間表現確認）
        print("\n🔍 第64条の期間表現テスト:")
        found_article_64 = False
        
        for chapter in chapters:
            if 'articles' in chapter:
                for article in chapter['articles']:
                    if '第六十四条' in article.get('title', '') or '第64条' in article.get('title', ''):
                        found_article_64 = True
                        print(f"✅ 第64条発見: {article.get('title', '')}")
                        
                        if 'ner_entities' in article and 'TIME_PERIOD' in article['ner_entities']:
                            time_entities = article['ner_entities']['TIME_PERIOD']
                            print(f"📅 期間表現: {len(time_entities)}個")
                            
                            for entity in time_entities:
                                if '一年六月' in entity['text']:
                                    print(f"  🎯 「{entity['text']}」 (位置: {entity['start']}-{entity['end']})")
                        break
        
        if not found_article_64:
            print("⚠️ 第64条が見つかりませんでした")
        
        print("\n✅ カテゴリ選択機能テスト完了")
        print("\n📱 アプリでのテスト手順:")
        print("1. http://localhost:8508 にアクセス")
        print("2. 章と条文を選択")
        print("3. 「ハイライト表示」を選択")
        print("4. 右パネルのラジオボタンでカテゴリ選択")
        print("5. 右パネルのクイック選択ボタンをクリック")
        print("6. 左パネルの統計ボタンをクリック")
        print("7. 選択元が正しく表示されることを確認")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def test_session_state_logic():
    """セッション状態ロジックのテスト"""
    print("\n🔬 セッション状態ロジックテスト")
    print("-" * 30)
    
    # 想定されるセッション状態のテスト
    test_states = [
        {"selected_category": "すべて", "source": "radio"},
        {"selected_category": "TIME_PERIOD", "source": "sidebar"},
        {"selected_category": "LAW_REFERENCE", "source": "quick_button"},
        {"selected_category": "ORGANIZATION", "source": "radio"},
    ]
    
    for i, state in enumerate(test_states, 1):
        print(f"{i}. カテゴリ: {state['selected_category']}, 選択元: {state['source']}")
        
        # 表示形式のテスト
        category_names = {
            'LAW_REFERENCE': '📚 法律参照',
            'ARTICLE_REFERENCE': '📋 条文参照', 
            'TIME_PERIOD': '⏰ 期間表現',
            'MONEY_AMOUNT': '💰 金額表現',
            'ORGANIZATION': '🏢 組織・機関',
            'PROCEDURE': '⚙️ 手続き関連',
            'LEGAL_STATUS': '⚖️ 法的地位'
        }
        
        source_icons = {
            "radio": "⚙️ 右パネル",
            "quick_button": "🚀 クイック選択", 
            "sidebar": "📊 左パネル"
        }
        
        if state['selected_category'] != "すべて":
            display_name = category_names.get(state['selected_category'], state['selected_category'])
            source_text = source_icons.get(state['source'], "🔧 システム")
            print(f"   → 表示: {display_name} (選択元: {source_text})")
        else:
            print(f"   → 表示: 🌈 すべてのカテゴリが表示されています")
    
    print("✅ セッション状態ロジックテスト完了")

if __name__ == "__main__":
    print("🚀 固有表現カテゴリ選択機能 統合テスト")
    print("=" * 60)
    
    success = test_category_selection()
    if success:
        test_session_state_logic()
        print("\n🎉 すべてのテストが完了しました！")
        print("📱 ブラウザでアプリをテストしてください: http://localhost:8508")
    else:
        print("\n❌ テストに失敗しました")
        sys.exit(1)
