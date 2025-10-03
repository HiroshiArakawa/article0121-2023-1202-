# 条文固有表現抽出（NER）システム

このプロジェクトは、法律文書の条文から固有表現（NER: Named Entity Recognition）を抽出する機能を提供します。

## 機能概要

1. **条文テキストの前処理**: HTMLタグの除去、文字正規化
2. **固有表現抽出**: 
   - spaCy/GiNZAによる標準的な固有表現抽出（人名、組織名、地名など）
   - 法律文書特有のパターン抽出（条文参照、日付、金額など）
3. **結果出力**: JSON、CSV、可視化グラフ、詳細レポート
4. **分析機能**: 統計情報の生成、カバレッジ分析

## ファイル構成

- `ner_processor.py`: メインのNER処理モジュール
- `ner_analyzer.py`: 結果分析・可視化モジュール
- `test_ner.py`: テストコード
- `parse-html.py`: HTML解析（既存）

## セットアップ

### 1. 仮想環境の作成とアクティベート

```bash
# .venv-inDockerフォルダで仮想環境を作成
python -m venv .venv-inDocker

# 仮想環境をアクティベート（Linux/Mac）
source .venv-inDocker/bin/activate
# shシェルの場合
. .venv-inDocker/bin/activate
```

### 2. 必要パッケージのインストール

```bash
pip install --upgrade pip
pip install spacy ginza pandas matplotlib beautifulsoup4
```

### 3. 日本語モデルのダウンロード

```bash
# GiNZAの日本語モデル
python -m spacy download ja_ginza

# または標準のspaCy日本語モデル
python -m spacy download ja_core_news_sm
```

## 使用方法

### 1. 基本的なNER処理

```bash
# メインのNER処理を実行
python ner_processor.py
```

これにより以下のファイルが生成されます：
- `{元ファイル名}_ner.json`: NER結果（JSON形式）
- `{元ファイル名}_ner.pickle`: NER結果（Python pickle形式）

### 2. 結果の分析・可視化

```bash
# 分析・可視化を実行
python ner_analyzer.py
```

これにより以下のファイルが生成されます：
- `ner_results.csv`: CSV形式の結果
- `visualizations/`: 可視化グラフのディレクトリ
  - `entity_type_distribution.png`: エンティティタイプ別分布
  - `chapter_entity_count.png`: 章別エンティティ数
  - `frequent_entities.png`: 頻出エンティティ
  - `article_coverage.png`: 条文別カバレッジ分布
- `ner_detailed_report.md`: 詳細レポート

### 3. テストの実行

```bash
# 簡単なテスト（ライブラリなしでも動作）
python test_ner.py simple

# 完全なテストスイート
python test_ner.py
```

## 抽出される固有表現の種類

### spaCy/GiNZAによる標準固有表現
- PERSON: 人名
- ORG: 組織名
- GPE: 地政学的実体（国、都市など）
- DATE: 日付
- TIME: 時間
- MONEY: 金額
- PERCENT: パーセンテージ
- その他多数

### 法律文書特有のカスタムパターン
- LAW_REFERENCE: 法律条文参照（第1条、第2項など）
- DATE_JP: 日本式日付（令和5年4月1日など）
- MONEY: 金額表現（100万円、50億円など）

## 出力形式

### JSON形式の例
```json
{
  "title": "第1条",
  "caption": "目的",
  "entities": {
    "spacy": [
      {
        "text": "令和5年",
        "label": "DATE",
        "label_description": "日付",
        "start_char": 10,
        "end_char": 14,
        "confidence": 0.99
      }
    ],
    "custom": [
      {
        "text": "第1条",
        "label": "LAW_REFERENCE",
        "label_description": "法律条文参照",
        "start_char": 0,
        "end_char": 3,
        "confidence": 1.0
      }
    ],
    "total_count": 2
  }
}
```

### CSV形式の列
- chapter: 章名
- article_title: 条文タイトル
- article_caption: 条文見出し
- entity_text: 固有表現のテキスト
- entity_type: 固有表現の種類
- entity_description: 固有表現の説明
- start_pos: 開始位置
- end_pos: 終了位置
- confidence: 信頼度
- source: 抽出元（spacy/custom）

## カスタマイズ

### 新しいパターンの追加

`ner_processor.py`の`extract_custom_patterns`メソッドに新しい正規表現パターンを追加できます：

```python
# 例：新しいパターンの追加
new_pattern = r'新しい正規表現パターン'
for match in re.finditer(new_pattern, text):
    patterns.append({
        'text': match.group(),
        'label': 'NEW_PATTERN',
        'label_description': '新しいパターンの説明',
        'start_char': match.start(),
        'end_char': match.end(),
        'confidence': 1.0
    })
```

### 使用モデルの変更

`ArticleNERProcessor`の初期化時にモデル名を指定：

```python
# GiNZAを使用
processor = ArticleNERProcessor("ja_ginza")

# 標準spaCyモデルを使用
processor = ArticleNERProcessor("ja_core_news_sm")
```

## トラブルシューティング

### モデルが見つからない場合
```bash
# モデルを再インストール
python -m spacy download ja_ginza
python -m spacy download ja_core_news_sm
```

### 日本語フォントの問題
可視化で文字化けが発生する場合は、システムに適切な日本語フォントをインストールしてください。

### メモリ不足
大きなファイルを処理する場合は、章数を制限して処理するか、より高いメモリを持つマシンを使用してください。

## パフォーマンス

- 処理速度: 条文数に依存（目安：100条文/分）
- メモリ使用量: モデルサイズ + データサイズ（目安：1-2GB）
- 推奨環境: RAM 4GB以上、Python 3.8以上

## 既知の制限事項

1. spaCyモデルの日本語精度は学習データに依存
2. 法律特有の用語は追加学習が必要な場合がある
3. 古い法律文書の文体には対応が不完全な場合がある

## 更新履歴

- v1.0.0: 初期リリース
  - 基本的なNER機能
  - カスタムパターン抽出
  - 結果出力・可視化機能
  - テストコード

## ライセンス

このプロジェクトは既存のプロジェクトの一部として開発されています。