# yaya-content-studio

Language: [繁體中文](README.md) | [English](README.en.md) | [日本語](README.ja.md)

`yaya-content-studio` は、個人のコンテンツ制作者向けのローカル CLI ツールです。

記事を自動生成するツールではありません。自動投稿もしません。どちらかというと、静かな「コンテンツ運営アシスタント」です。アイデアを保存し、Markdown の下書きを残し、記事の反応を記録し、無料の SVG カバーを作り、次に何を書くかを簡単なルールで考えるための道具です。

第一版はローカルファーストです。API 連携なし、アカウント不要、外部サービスへの送信なし。データは CSV と Markdown として、プロジェクトフォルダの中に残ります。

![yaya-content-studio CLI demo](docs/assets/demo.svg)

## Project Links

- [Usage examples](docs/usage_examples.md)
- [Content strategy notes](docs/content_strategy.md)
- [Launch article draft](docs/launch_article.md)
- [Roadmap](docs/roadmap.md)

## 向いている人

このツールは、こういう人に向いています。

- note、Medium、Threads、X で発信している
- アイデアはあるけれど、あとで文脈を忘れがち
- 無料記事と有料記事を分けて考えたい
- なんとなくではなく、記事の反応を見ながら次のテーマを決めたい
- Markdown や CSV のようなシンプルなローカルファイルが好き
- 最初から API やクラウドサービスにつなぎたくない

個人創作者、小さな知識労働者、日々の経験を記事にしたい人に向いています。

## インストール

Python 3 が使えるか確認します。

```bash
python --version
```

`python` がない場合は：

```bash
python3 --version
```

リポジトリを clone またはダウンロードして、フォルダに入ります。

```bash
cd yaya-content-studio
```

第一版では外部ライブラリは不要です。`requirements.txt` は将来のために残しています。

必要なら仮想環境を作れます。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

環境によっては `python` を `python3` に置き換えてください。

## 基本の流れ

1. 思いついたテーマを `new` で保存する
2. 書き始めるときに `save` で Markdown 下書きを保存する
3. 必要なら `cover` で無料 SVG カバーを作る
4. note や Medium に手動で投稿する
5. 投稿後の反応を `stats` で記録する
6. `analyze` で傾向を見る
7. `suggest` で次のテーマ候補を出す

このツールは、あなたの方向性を代わりに決めるものではありません。コンテンツ運営で散らばりやすい小さな情報を集めて、次の判断を少し楽にするためのものです。

## コマンド

プロジェクトルートで実行します。

```bash
python main.py <command>
```

`python3` を使う環境では：

```bash
python3 main.py <command>
```

### 記事アイデアを追加

```bash
python main.py new
```

入力項目：

- platform: note / Medium / Threads / X
- title
- category
- target_reader
- paid: yes / no
- memo

保存先：

```text
data/content_ideas.csv
```

### 下書きを保存

```bash
python main.py save
```

入力項目：

- title
- platform
- category
- tags
- body markdown

本文入力は、`.` だけの行で終了します。

保存先：

```text
articles/YYYY/MM/YYYYMMDD_platform_title.md
```

front matter：

```markdown
---
title:
date:
platform:
category:
tags:
status: draft
---
```

### 無料 SVG カバーを生成

```bash
python main.py cover
```

入力項目：

- title
- platform
- category
- tags
- subtitle

このコマンドは画像 API を呼びません。有料サービスも不要です。ローカルに SVG カバーを作ります。

```text
exports/covers/YYYY/MM/YYYYMMDD_platform_title_cover.svg
```

`exports/` は Git で無視されるので、個人の投稿素材をローカルに置けます。

### 最近の内容を表示

```bash
python main.py list
```

最近のアイデアと Markdown 下書きを表示します。

### 記事の反応を記録

```bash
python main.py stats
```

入力項目：

- date
- platform
- title
- views
- likes
- comments
- claps
- sales
- memo

保存先：

```text
data/stats.csv
```

### 反応を分析

```bash
python main.py analyze
```

簡単なルールで以下を出力します。

- 反応がよかった platform
- 反応がよかった category
- likes はあるが sales がない記事
- 有料記事にできそうな記事
- 次のアクション候補

### 次のテーマを提案

```bash
python main.py suggest
```

`content_ideas.csv` と `stats.csv` をもとに、次に書けそうなテーマを 5 個出します。

現在のルール：

- 最近 5 件と似すぎるテーマを避ける
- likes が多く sales が少ないテーマを、より具体的な有料記事案にする
- 反応のよい category からシリーズ案を出す
- note / Medium 用のタイトル案を出す

## note / Medium の流れ

たとえば「海外で働いたあと、どうやってコンテンツのアイデアを整理するか」を書きたい場合：

1. `python main.py new` でアイデアを保存
2. `python main.py save` で note 向けの個人的な下書きを保存
3. `python main.py cover` で無料 SVG カバーを作成
4. 反応がよければ、より構造化した Medium 記事に展開
5. `python main.py stats` で views、likes、comments、sales を記録
6. `python main.py analyze` と `python main.py suggest` で次を考える

無料記事は共感と信頼を作るためのもの。有料記事は具体的な問題を解くためのものです。有料記事には、手順、失敗、テンプレート、実例があると強くなります。

## Roadmap

### v1: ローカル CLI

- 記事アイデアの追加
- Markdown 下書きの保存
- 無料 SVG カバーの生成
- 最近のアイデアと下書きの表示
- 記事の反応の記録
- 簡単なルール分析
- 次のテーマ提案

### v2: より使いやすいローカル workflow

- アイデアの検索とフィルター
- 記事ステータスの更新
- 週次レビューの生成
- 有料記事テンプレートの追加
- 下書き bundle の export
- カバースタイル追加と PNG export

### v3: 任意の連携

- 任意の AI 要約やレビュー補助
- 任意の platform data import
- 任意の content calendar

自動投稿は初期目標ではありません。個人創作者にとっては、すべてのツールをつなぐよりも、まず自分の執筆フローを安定させることのほうが大事だと考えています。
