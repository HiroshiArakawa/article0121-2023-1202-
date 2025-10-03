# -*- coding: utf-8 -*-
"""
条文から固有表現抽出（NER）を行うモジュール
"""
import io
import sys
import pickle
import json
import re
from typing import List, Dict, Any, Tuple
from bs4 import BeautifulSoup
import spacy
from spacy import displacy

# WindowsのPython3で標準出力をUTF8にする
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class ArticleNERProcessor:
    """条文のNER処理を行うクラス"""
    
    def __init__(self, model_name: str = "ja_ginza"):
        """
        初期化
        
        Args:
            model_name: 使用するspaCyモデル名
        """
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            print(f"モデル {model_name} が見つかりません。ja_coreを試します...")
            try:
                self.nlp = spacy.load("ja_core_news_sm")
            except OSError:
                print("日本語モデルが見つかりません。基本モデルを使用します...")
                self.nlp = spacy.blank("ja")
    
    def preprocess_article_text(self, article_body: str) -> str:
        """
        条文テキストの前処理
        
        Args:
            article_body: 条文のHTML文字列またはテキスト
            
        Returns:
            前処理されたテキスト
        """
        # HTMLタグを除去
        if "<" in article_body and ">" in article_body:
            soup = BeautifulSoup(article_body, 'html.parser')
            text = soup.get_text()
        else:
            text = article_body
        
        # 不要な空白、改行を正規化
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # 法律特有の記号の処理
        text = re.sub(r'（', '(', text)
        text = re.sub(r'）', ')', text)
        
        return text
    
    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        テキストから固有表現を抽出
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            抽出された固有表現のリスト
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entity_info = {
                'text': ent.text,
                'label': ent.label_,
                'label_description': spacy.explain(ent.label_),
                'start_char': ent.start_char,
                'end_char': ent.end_char,
                'confidence': getattr(ent, 'kb_score_', None)  # GiNZAの場合に利用可能
            }
            entities.append(entity_info)
        
        return entities
    
    def extract_custom_patterns(self, text: str) -> List[Dict[str, Any]]:
        """
        法律文書特有のパターンを抽出
        
        Args:
            text: 処理対象のテキスト
            
        Returns:
            抽出されたカスタムパターンのリスト
        """
        patterns = []
        
        # 法律条文の参照パターン（例：第1条、第2項など）
        law_ref_pattern = r'第[０-９0-9一二三四五六七八九十百千万]+条|第[０-９0-9一二三四五六七八九十百千万]+項|第[０-９0-9一二三四五六七八九十百千万]+号'
        for match in re.finditer(law_ref_pattern, text):
            patterns.append({
                'text': match.group(),
                'label': 'LAW_REFERENCE',
                'label_description': '法律条文参照',
                'start_char': match.start(),
                'end_char': match.end(),
                'confidence': 1.0
            })
        
        # 日付パターン（年月日）
        date_pattern = r'[令平昭]和[０-９0-9一二三四五六七八九十百千万]+年[０-９0-9一二三四五六七八九十百千万]+月[０-９0-9一二三四五六七八九十百千万]+日'
        for match in re.finditer(date_pattern, text):
            patterns.append({
                'text': match.group(),
                'label': 'DATE_JP',
                'label_description': '日本式日付',
                'start_char': match.start(),
                'end_char': match.end(),
                'confidence': 1.0
            })
        
        # 金額パターン
        money_pattern = r'[０-９0-9,，]+円|[０-９0-9,，]+万円|[０-９0-9,，]+億円'
        for match in re.finditer(money_pattern, text):
            patterns.append({
                'text': match.group(),
                'label': 'MONEY',
                'label_description': '金額',
                'start_char': match.start(),
                'end_char': match.end(),
                'confidence': 1.0
            })
        
        return patterns
    
    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        単一の条文を処理
        
        Args:
            article: 条文データ（title, caption, bodyを含む辞書）
            
        Returns:
            NER結果を含む条文データ
        """
        # テキストの前処理
        processed_text = self.preprocess_article_text(article['body'])
        
        # 固有表現抽出
        spacy_entities = self.extract_entities(processed_text)
        custom_entities = self.extract_custom_patterns(processed_text)
        
        # 結果をまとめる
        result = {
            'title': article['title'],
            'caption': article.get('caption', ''),
            'original_body': article['body'],
            'processed_text': processed_text,
            'entities': {
                'spacy': spacy_entities,
                'custom': custom_entities,
                'total_count': len(spacy_entities) + len(custom_entities)
            }
        }
        
        return result
    
    def process_chapters(self, chapters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        全章の条文を処理
        
        Args:
            chapters: 章データのリスト
            
        Returns:
            NER結果を含む章データのリスト
        """
        processed_chapters = []
        
        for chapter in chapters:
            processed_articles = []
            
            for article in chapter['articles']:
                processed_article = self.process_article(article)
                processed_articles.append(processed_article)
            
            processed_chapter = {
                'title': chapter['title'],
                'articles': processed_articles,
                'summary': {
                    'total_articles': len(processed_articles),
                    'total_entities': sum(article['entities']['total_count'] for article in processed_articles)
                }
            }
            processed_chapters.append(processed_chapter)
        
        return processed_chapters
    
    def save_results(self, results: List[Dict[str, Any]], base_filename: str):
        """
        結果を保存
        
        Args:
            results: 処理結果
            base_filename: 基本ファイル名
        """
        # JSON形式で保存
        with open(f"{base_filename}_ner.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # Pickle形式で保存
        with open(f"{base_filename}_ner.pickle", 'wb') as f:
            pickle.dump(results, f)
        
        print(f"結果を {base_filename}_ner.json と {base_filename}_ner.pickle に保存しました")
    
    def generate_summary_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        サマリーレポートを生成
        
        Args:
            results: 処理結果
            
        Returns:
            サマリーレポート
        """
        total_chapters = len(results)
        total_articles = sum(chapter['summary']['total_articles'] for chapter in results)
        total_entities = sum(chapter['summary']['total_entities'] for chapter in results)
        
        # エンティティタイプ別の統計
        entity_types = {}
        for chapter in results:
            for article in chapter['articles']:
                for entity in article['entities']['spacy'] + article['entities']['custom']:
                    label = entity['label']
                    if label not in entity_types:
                        entity_types[label] = 0
                    entity_types[label] += 1
        
        summary = {
            'total_chapters': total_chapters,
            'total_articles': total_articles,
            'total_entities': total_entities,
            'entity_types_count': entity_types,
            'average_entities_per_article': total_entities / total_articles if total_articles > 0 else 0
        }
        
        return summary


def main():
    """メイン処理"""
    # pickleファイルから条文データを読み込み
    pickle_file = '334AC0000000121_20230703_505AC0000000051.pickle'
    
    try:
        with open(pickle_file, 'rb') as f:
            chapters = pickle.load(f)
        
        print(f"条文データを読み込みました: {len(chapters)}章")
        
        # NER処理器を初期化
        processor = ArticleNERProcessor()
        
        # 条文を処理
        print("NER処理を開始します...")
        results = processor.process_chapters(chapters)
        
        # 結果を保存
        base_filename = pickle_file.replace('.pickle', '')
        processor.save_results(results, base_filename)
        
        # サマリーレポートを生成
        summary = processor.generate_summary_report(results)
        print("\n=== NER処理サマリー ===")
        print(f"総章数: {summary['total_chapters']}")
        print(f"総条文数: {summary['total_articles']}")
        print(f"総固有表現数: {summary['total_entities']}")
        print(f"条文あたり平均固有表現数: {summary['average_entities_per_article']:.2f}")
        print("\n=== エンティティタイプ別統計 ===")
        for entity_type, count in sorted(summary['entity_types_count'].items()):
            print(f"{entity_type}: {count}")
        
    except FileNotFoundError:
        print(f"ファイル {pickle_file} が見つかりません")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == '__main__':
    main()