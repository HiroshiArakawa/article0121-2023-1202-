# -*- coding: utf-8 -*-
"""
NER機能のテストコード
"""
import unittest
import os
import json
import tempfile
import sys
from unittest.mock import patch, MagicMock

# 自作モジュールをインポート
from ner_processor import ArticleNERProcessor


class TestArticleNERProcessor(unittest.TestCase):
    """ArticleNERProcessorのテストクラス"""
    
    def setUp(self):
        """テストセットアップ"""
        # モックのspaCyモデルを作成
        self.processor = ArticleNERProcessor()
        
        # テスト用データ
        self.test_article = {
            'title': '第1条',
            'caption': 'テスト条文',
            'body': '<section>この法律は、令和5年4月1日から施行する。田中太郎氏が東京都で100万円を支払った。</section>'
        }
        
        self.test_chapters = [
            {
                'title': '第1章 総則',
                'articles': [self.test_article]
            }
        ]
    
    def test_preprocess_article_text(self):
        """テキスト前処理のテスト"""
        # HTMLタグの除去テスト
        html_text = '<section><span>第1条</span> この法律は、令和5年4月1日から施行する。</section>'
        result = self.processor.preprocess_article_text(html_text)
        
        self.assertNotIn('<', result)
        self.assertNotIn('>', result)
        self.assertIn('第1条', result)
        self.assertIn('令和5年4月1日', result)
    
    def test_extract_custom_patterns(self):
        """カスタムパターン抽出のテスト"""
        text = "第1条、第2項、第3号について、令和5年4月1日に100万円を支払う。"
        patterns = self.processor.extract_custom_patterns(text)
        
        # 法律参照パターンの検出
        law_refs = [p for p in patterns if p['label'] == 'LAW_REFERENCE']
        self.assertGreater(len(law_refs), 0)
        
        # 日付パターンの検出
        dates = [p for p in patterns if p['label'] == 'DATE_JP']
        self.assertGreater(len(dates), 0)
        
        # 金額パターンの検出
        money = [p for p in patterns if p['label'] == 'MONEY']
        self.assertGreater(len(money), 0)
    
    def test_process_article(self):
        """条文処理のテスト"""
        result = self.processor.process_article(self.test_article)
        
        # 必要なキーが存在することを確認
        required_keys = ['title', 'caption', 'original_body', 'processed_text', 'entities']
        for key in required_keys:
            self.assertIn(key, result)
        
        # エンティティ情報の構造確認
        self.assertIn('spacy', result['entities'])
        self.assertIn('custom', result['entities'])
        self.assertIn('total_count', result['entities'])
        
        # カスタムパターンが検出されることを確認
        custom_entities = result['entities']['custom']
        self.assertGreater(len(custom_entities), 0)
    
    def test_process_chapters(self):
        """章処理のテスト"""
        results = self.processor.process_chapters(self.test_chapters)
        
        self.assertEqual(len(results), 1)
        
        chapter_result = results[0]
        self.assertIn('title', chapter_result)
        self.assertIn('articles', chapter_result)
        self.assertIn('summary', chapter_result)
        
        # サマリー情報の確認
        summary = chapter_result['summary']
        self.assertIn('total_articles', summary)
        self.assertIn('total_entities', summary)
        self.assertEqual(summary['total_articles'], 1)
    
    def test_save_results(self):
        """結果保存のテスト"""
        # 一時ディレクトリを作成
        with tempfile.TemporaryDirectory() as temp_dir:
            base_filename = os.path.join(temp_dir, 'test_result')
            
            # テスト結果を作成
            test_results = self.processor.process_chapters(self.test_chapters)
            
            # 保存実行
            self.processor.save_results(test_results, base_filename)
            
            # ファイルが作成されることを確認
            json_file = f"{base_filename}_ner.json"
            pickle_file = f"{base_filename}_ner.pickle"
            
            self.assertTrue(os.path.exists(json_file))
            self.assertTrue(os.path.exists(pickle_file))
            
            # JSONファイルの内容確認
            with open(json_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                self.assertEqual(len(loaded_data), 1)
    
    def test_generate_summary_report(self):
        """サマリーレポート生成のテスト"""
        test_results = self.processor.process_chapters(self.test_chapters)
        summary = self.processor.generate_summary_report(test_results)
        
        # 必要なキーの存在確認
        required_keys = [
            'total_chapters', 'total_articles', 'total_entities',
            'entity_types_count', 'average_entities_per_article'
        ]
        for key in required_keys:
            self.assertIn(key, summary)
        
        # 値の妥当性確認
        self.assertEqual(summary['total_chapters'], 1)
        self.assertEqual(summary['total_articles'], 1)
        self.assertGreaterEqual(summary['total_entities'], 0)


class TestNERIntegration(unittest.TestCase):
    """統合テストクラス"""
    
    def setUp(self):
        """テストセットアップ"""
        # 実際のpickleファイルが存在するかチェック
        self.pickle_file = '334AC0000000121_20230703_505AC0000000051.pickle'
        self.file_exists = os.path.exists(self.pickle_file)
    
    @unittest.skipUnless(os.path.exists('334AC0000000121_20230703_505AC0000000051.pickle'), 
                         "テスト用pickleファイルが存在しません")
    def test_full_ner_processing(self):
        """完全なNER処理のテスト"""
        import pickle
        
        # 実際のデータを読み込み
        with open(self.pickle_file, 'rb') as f:
            chapters = pickle.load(f)
        
        # 少数のサンプルのみテスト（時間短縮のため）
        test_chapters = chapters[:2] if len(chapters) > 2 else chapters
        
        # NER処理を実行
        processor = ArticleNERProcessor()
        results = processor.process_chapters(test_chapters)
        
        # 結果の妥当性確認
        self.assertEqual(len(results), len(test_chapters))
        
        for i, chapter_result in enumerate(results):
            self.assertIn('title', chapter_result)
            self.assertIn('articles', chapter_result)
            self.assertIn('summary', chapter_result)
            
            # 各条文の処理結果確認
            for article_result in chapter_result['articles']:
                self.assertIn('entities', article_result)
                entities = article_result['entities']
                self.assertIn('spacy', entities)
                self.assertIn('custom', entities)
                self.assertIn('total_count', entities)


class TestCustomPatterns(unittest.TestCase):
    """カスタムパターン抽出の詳細テスト"""
    
    def setUp(self):
        """テストセットアップ"""
        self.processor = ArticleNERProcessor()
    
    def test_law_reference_patterns(self):
        """法律参照パターンのテスト"""
        test_cases = [
            ("第1条について", ["第1条"]),
            ("第十二条及び第2項", ["第十二条", "第2項"]),
            ("第123号の規定により", ["第123号"]),
            ("第一条、第二項、第三号", ["第一条", "第二項", "第三号"])
        ]
        
        for text, expected in test_cases:
            patterns = self.processor.extract_custom_patterns(text)
            law_refs = [p['text'] for p in patterns if p['label'] == 'LAW_REFERENCE']
            
            for exp in expected:
                self.assertIn(exp, law_refs, f"'{exp}'が'{text}'から抽出されませんでした")
    
    def test_date_patterns(self):
        """日付パターンのテスト"""
        test_cases = [
            ("令和5年4月1日", ["令和5年4月1日"]),
            ("平成30年12月31日", ["平成30年12月31日"]),
            ("昭和64年1月7日", ["昭和64年1月7日"])
        ]
        
        for text, expected in test_cases:
            patterns = self.processor.extract_custom_patterns(text)
            dates = [p['text'] for p in patterns if p['label'] == 'DATE_JP']
            
            for exp in expected:
                self.assertIn(exp, dates, f"'{exp}'が'{text}'から抽出されませんでした")
    
    def test_money_patterns(self):
        """金額パターンのテスト"""
        test_cases = [
            ("100円", ["100円"]),
            ("1,000万円", ["1,000万円"]),
            ("50億円", ["50億円"]),
            ("1,234,567円", ["1,234,567円"])
        ]
        
        for text, expected in test_cases:
            patterns = self.processor.extract_custom_patterns(text)
            money = [p['text'] for p in patterns if p['label'] == 'MONEY']
            
            for exp in expected:
                self.assertIn(exp, money, f"'{exp}'が'{text}'から抽出されませんでした")


def run_simple_test():
    """簡単なテスト実行（ライブラリなしでも動作）"""
    print("=== NER機能の簡単テスト ===")
    
    try:
        # ArticleNERProcessorの基本テスト
        processor = ArticleNERProcessor()
        print("✓ ArticleNERProcessor の初期化成功")
        
        # テキスト前処理テスト
        test_html = '<section>第1条 この法律は令和5年4月1日から施行する。</section>'
        processed = processor.preprocess_article_text(test_html)
        print(f"✓ テキスト前処理成功: {processed[:50]}...")
        
        # カスタムパターン抽出テスト
        test_text = "第1条について、令和5年4月1日に100万円を支払う。"
        patterns = processor.extract_custom_patterns(test_text)
        print(f"✓ カスタムパターン抽出成功: {len(patterns)}個のパターンを検出")
        
        for pattern in patterns:
            print(f"  - {pattern['text']} ({pattern['label']})")
        
        # 条文処理テスト
        test_article = {
            'title': '第1条',
            'caption': 'テスト条文',
            'body': test_html
        }
        
        result = processor.process_article(test_article)
        print(f"✓ 条文処理成功: {result['entities']['total_count']}個の固有表現を検出")
        
        print("\n=== テスト完了 ===")
        print("全ての基本機能が正常に動作しています。")
        
    except Exception as e:
        print(f"✗ テスト中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # コマンドライン引数でテストモードを選択
    if len(sys.argv) > 1 and sys.argv[1] == 'simple':
        run_simple_test()
    else:
        # 通常のunittest実行
        unittest.main()