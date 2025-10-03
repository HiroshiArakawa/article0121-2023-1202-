# -*- coding: utf-8 -*-
"""
NER結果の可視化と分析機能
"""
import json
import pickle
import csv
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from collections import Counter, defaultdict
import os


class NERResultAnalyzer:
    """NER結果の分析と可視化を行うクラス"""
    
    def __init__(self):
        """初期化"""
        # 日本語フォントの設定
        self._setup_japanese_font()
    
    def _setup_japanese_font(self):
        """日本語フォントの設定"""
        try:
            # Linux環境での日本語フォント設定
            japanese_fonts = [
                'DejaVu Sans', 
                'Liberation Sans', 
                'Arial Unicode MS',
                'Hiragino Sans',
                'Yu Gothic'
            ]
            
            for font_name in japanese_fonts:
                try:
                    plt.rcParams['font.family'] = font_name
                    break
                except:
                    continue
            
            plt.rcParams['font.size'] = 10
            plt.rcParams['axes.unicode_minus'] = False
            
        except Exception as e:
            print(f"日本語フォント設定でエラー: {e}")
            print("デフォルトフォントを使用します")
    
    def load_ner_results(self, filepath: str) -> List[Dict[str, Any]]:
        """
        NER結果を読み込み
        
        Args:
            filepath: 結果ファイルのパス
            
        Returns:
            NER結果のリスト
        """
        if filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif filepath.endswith('.pickle'):
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        else:
            raise ValueError("サポートされていないファイル形式です")
    
    def export_to_csv(self, results: List[Dict[str, Any]], output_file: str):
        """
        結果をCSV形式で出力
        
        Args:
            results: NER結果
            output_file: 出力ファイル名
        """
        rows = []
        
        for chapter in results:
            chapter_title = chapter['title']
            
            for article in chapter['articles']:
                article_title = article['title']
                article_caption = article.get('caption', '')
                
                # spaCyエンティティ
                for entity in article['entities']['spacy']:
                    rows.append({
                        'chapter': chapter_title,
                        'article_title': article_title,
                        'article_caption': article_caption,
                        'entity_text': entity['text'],
                        'entity_type': entity['label'],
                        'entity_description': entity['label_description'],
                        'start_pos': entity['start_char'],
                        'end_pos': entity['end_char'],
                        'confidence': entity.get('confidence', ''),
                        'source': 'spacy'
                    })
                
                # カスタムエンティティ
                for entity in article['entities']['custom']:
                    rows.append({
                        'chapter': chapter_title,
                        'article_title': article_title,
                        'article_caption': article_caption,
                        'entity_text': entity['text'],
                        'entity_type': entity['label'],
                        'entity_description': entity['label_description'],
                        'start_pos': entity['start_char'],
                        'end_pos': entity['end_char'],
                        'confidence': entity.get('confidence', ''),
                        'source': 'custom'
                    })
        
        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"CSV結果を {output_file} に保存しました")
    
    def generate_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        統計情報を生成
        
        Args:
            results: NER結果
            
        Returns:
            統計情報
        """
        stats = {
            'total_chapters': len(results),
            'total_articles': 0,
            'total_entities': 0,
            'entity_by_type': Counter(),
            'entity_by_chapter': defaultdict(int),
            'entity_frequency': Counter(),
            'top_entities': {},
            'coverage_by_article': []
        }
        
        for chapter in results:
            chapter_title = chapter['title']
            chapter_entity_count = 0
            
            for article in chapter['articles']:
                stats['total_articles'] += 1
                article_entity_count = article['entities']['total_count']
                stats['total_entities'] += article_entity_count
                chapter_entity_count += article_entity_count
                
                # 条文ごとの固有表現カバレッジ
                text_length = len(article['processed_text'])
                coverage = article_entity_count / max(text_length, 1) * 100
                stats['coverage_by_article'].append({
                    'chapter': chapter_title,
                    'article': article['title'],
                    'entity_count': article_entity_count,
                    'text_length': text_length,
                    'coverage': coverage
                })
                
                # エンティティタイプ別統計
                for entity in article['entities']['spacy'] + article['entities']['custom']:
                    entity_type = entity['label']
                    entity_text = entity['text']
                    
                    stats['entity_by_type'][entity_type] += 1
                    stats['entity_frequency'][entity_text] += 1
            
            stats['entity_by_chapter'][chapter_title] = chapter_entity_count
        
        # 各タイプの上位エンティティ
        for entity_type in stats['entity_by_type'].keys():
            type_entities = []
            for chapter in results:
                for article in chapter['articles']:
                    for entity in article['entities']['spacy'] + article['entities']['custom']:
                        if entity['label'] == entity_type:
                            type_entities.append(entity['text'])
            
            stats['top_entities'][entity_type] = Counter(type_entities).most_common(10)
        
        return stats
    
    def create_visualizations(self, results: List[Dict[str, Any]], output_dir: str = "visualizations"):
        """
        可視化グラフを作成
        
        Args:
            results: NER結果
            output_dir: 出力ディレクトリ
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        stats = self.generate_statistics(results)
        
        # 1. エンティティタイプ別分布
        self._plot_entity_distribution(stats['entity_by_type'], 
                                     os.path.join(output_dir, 'entity_type_distribution.png'))
        
        # 2. 章別エンティティ数
        self._plot_chapter_distribution(stats['entity_by_chapter'], 
                                      os.path.join(output_dir, 'chapter_entity_count.png'))
        
        # 3. 頻出エンティティ
        self._plot_frequent_entities(stats['entity_frequency'], 
                                   os.path.join(output_dir, 'frequent_entities.png'))
        
        # 4. 条文別カバレッジ
        self._plot_coverage_distribution(stats['coverage_by_article'], 
                                       os.path.join(output_dir, 'article_coverage.png'))
        
        print(f"可視化結果を {output_dir} ディレクトリに保存しました")
    
    def _plot_entity_distribution(self, entity_by_type: Counter, output_file: str):
        """エンティティタイプ別分布グラフ"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        types = list(entity_by_type.keys())
        counts = list(entity_by_type.values())
        
        bars = ax.bar(types, counts, color='skyblue', alpha=0.7)
        ax.set_title('Entity Type Distribution', fontsize=16)
        ax.set_xlabel('Entity Type', fontsize=12)
        ax.set_ylabel('Count', fontsize=12)
        
        # 値を棒グラフの上に表示
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   str(count), ha='center', va='bottom')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_chapter_distribution(self, entity_by_chapter: defaultdict, output_file: str):
        """章別エンティティ数グラフ"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        chapters = list(entity_by_chapter.keys())
        counts = list(entity_by_chapter.values())
        
        # 章名を短縮（長すぎる場合）
        short_chapters = [ch[:20] + '...' if len(ch) > 20 else ch for ch in chapters]
        
        bars = ax.bar(range(len(chapters)), counts, color='lightgreen', alpha=0.7)
        ax.set_title('Entity Count by Chapter', fontsize=16)
        ax.set_xlabel('Chapter', fontsize=12)
        ax.set_ylabel('Entity Count', fontsize=12)
        
        # 値を棒グラフの上に表示
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                   str(count), ha='center', va='bottom')
        
        ax.set_xticks(range(len(chapters)))
        ax.set_xticklabels(short_chapters, rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_frequent_entities(self, entity_frequency: Counter, output_file: str, top_n: int = 20):
        """頻出エンティティグラフ"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        top_entities = entity_frequency.most_common(top_n)
        entities, counts = zip(*top_entities) if top_entities else ([], [])
        
        # エンティティ名を短縮
        short_entities = [ent[:15] + '...' if len(ent) > 15 else ent for ent in entities]
        
        y_pos = range(len(entities))
        bars = ax.barh(y_pos, counts, color='orange', alpha=0.7)
        
        ax.set_title(f'Top {top_n} Most Frequent Entities', fontsize=16)
        ax.set_xlabel('Frequency', fontsize=12)
        ax.set_ylabel('Entity', fontsize=12)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(short_entities)
        
        # 値を棒グラフの右に表示
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                   str(count), ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_coverage_distribution(self, coverage_data: List[Dict], output_file: str):
        """条文別カバレッジ分布"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        coverages = [item['coverage'] for item in coverage_data]
        
        ax.hist(coverages, bins=20, color='purple', alpha=0.7, edgecolor='black')
        ax.set_title('Entity Coverage Distribution by Article', fontsize=16)
        ax.set_xlabel('Coverage (%)', fontsize=12)
        ax.set_ylabel('Number of Articles', fontsize=12)
        
        # 統計情報を追加
        mean_coverage = sum(coverages) / len(coverages)
        ax.axvline(mean_coverage, color='red', linestyle='--', 
                  label=f'Mean: {mean_coverage:.2f}%')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_detailed_report(self, results: List[Dict[str, Any]], output_file: str):
        """
        詳細レポートを生成
        
        Args:
            results: NER結果
            output_file: 出力ファイル名
        """
        stats = self.generate_statistics(results)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 固有表現抽出（NER）詳細レポート\n\n")
            
            # 基本統計
            f.write("## 基本統計\n")
            f.write(f"- 総章数: {stats['total_chapters']}\n")
            f.write(f"- 総条文数: {stats['total_articles']}\n")
            f.write(f"- 総固有表現数: {stats['total_entities']}\n")
            f.write(f"- 条文あたり平均固有表現数: {stats['total_entities'] / stats['total_articles']:.2f}\n\n")
            
            # エンティティタイプ別統計
            f.write("## エンティティタイプ別統計\n")
            for entity_type, count in stats['entity_by_type'].most_common():
                percentage = count / stats['total_entities'] * 100
                f.write(f"- {entity_type}: {count} ({percentage:.1f}%)\n")
            f.write("\n")
            
            # 各タイプの上位エンティティ
            f.write("## 各タイプの頻出エンティティ（上位10）\n")
            for entity_type, top_entities in stats['top_entities'].items():
                f.write(f"\n### {entity_type}\n")
                for i, (entity, count) in enumerate(top_entities, 1):
                    f.write(f"{i}. {entity}: {count}回\n")
            
            # 章別統計
            f.write("\n## 章別エンティティ数\n")
            for chapter, count in sorted(stats['entity_by_chapter'].items(), 
                                       key=lambda x: x[1], reverse=True):
                f.write(f"- {chapter}: {count}\n")
            
            # カバレッジ統計
            coverages = [item['coverage'] for item in stats['coverage_by_article']]
            f.write(f"\n## カバレッジ統計\n")
            f.write(f"- 平均カバレッジ: {sum(coverages) / len(coverages):.2f}%\n")
            f.write(f"- 最大カバレッジ: {max(coverages):.2f}%\n")
            f.write(f"- 最小カバレッジ: {min(coverages):.2f}%\n")
        
        print(f"詳細レポートを {output_file} に保存しました")


def main():
    """メイン処理"""
    try:
        # NER結果ファイルを指定
        ner_result_file = "334AC0000000121_20230703_505AC0000000051_ner.json"
        
        if not os.path.exists(ner_result_file):
            print(f"NER結果ファイル {ner_result_file} が見つかりません")
            print("まず ner_processor.py を実行してNER処理を行ってください")
            return
        
        # 分析器を初期化
        analyzer = NERResultAnalyzer()
        
        # 結果を読み込み
        print("NER結果を読み込んでいます...")
        results = analyzer.load_ner_results(ner_result_file)
        
        # CSV出力
        print("CSV形式で出力しています...")
        analyzer.export_to_csv(results, "ner_results.csv")
        
        # 可視化
        print("可視化グラフを作成しています...")
        analyzer.create_visualizations(results)
        
        # 詳細レポート生成
        print("詳細レポートを生成しています...")
        analyzer.generate_detailed_report(results, "ner_detailed_report.md")
        
        print("\n分析完了！以下のファイルが生成されました:")
        print("- ner_results.csv: CSV形式の結果")
        print("- visualizations/: 可視化グラフ")
        print("- ner_detailed_report.md: 詳細レポート")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == '__main__':
    main()