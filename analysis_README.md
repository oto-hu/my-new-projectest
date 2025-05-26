# 健康診断データ解析システム

このプロジェクトは、健康診断データ（health_check_sample.csv）を解析し、結果をWebダッシュボードで表示するシステムです。

## 機能

### 解析機能（health_analysis.py）
- **TASK-01**: データ読み込みと基本情報確認
  - CSVファイルの読み込み
  - データ型と欠損値の確認
  - 基本統計情報の出力

- **TASK-02**: 要約統計量の算出
  - 全数値列の記述統計
  - 平均、中央値、標準偏差などの算出

- **TASK-03**: 主要指標の算出と分析
  - BMI計算とカテゴリ分類
  - 年代別健康指標の平均値算出
  - 健康リスク分析

- **TASK-04**: データ可視化
  - BMIカテゴリ別分布の棒グラフ
  - 年代別BMI推移の折れ線グラフ
  - 運動と健康指標の相関散布図
  - 各健康指標の分布ヒストグラム

### Web ダッシュボード（app.py）
- 解析結果の可視化
- インタラクティブなグラフ表示
- リアルタイム解析再実行機能
- レスポンシブデザイン

## インストールと実行

### 1. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 2. 解析実行
```bash
python health_analysis.py
```

### 3. Webアプリケーション起動
```bash
python app.py
```

アプリケーションは http://localhost:5000 で利用できます。

## ファイル構成

```
├── health_check_sample.csv    # 元データ
├── health_analysis.py         # 解析スクリプト
├── app.py                    # Flaskアプリケーション
├── requirements.txt          # Python依存関係
├── templates/
│   └── index.html           # Webダッシュボード
└── static/
    ├── analysis_results.json # 解析結果データ
    └── images/              # 生成された画像
        ├── bmi_category_distribution.png
        ├── age_group_bmi_trend.png
        ├── exercise_correlation_scatter.png
        └── health_indicators_distribution.png
```

## データ項目

- **ID**: 個人識別番号
- **Age**: 年齢
- **Height_cm**: 身長（cm）
- **Weight_kg**: 体重（kg）
- **Systolic_BP**: 収縮期血圧
- **Diastolic_BP**: 拡張期血圧
- **Cholesterol**: コレステロール値
- **Fasting_Blood_Sugar**: 空腹時血糖値
- **Exercise_Days_Per_Week**: 週間運動日数

## 解析内容

### BMI分析
- BMI計算（体重kg ÷ 身長m²）
- BMIカテゴリ分類：
  - 低体重: < 18.5
  - 標準体重: 18.5-24.9
  - 肥満1度: 25.0-29.9
  - 肥満2度以上: ≥ 30.0

### 年代別分析
- 20代、30代、40代、50代、60代以上でグループ化
- 各年代の平均BMI、血圧、コレステロール値、運動日数を算出

### 相関分析
- 運動日数と各健康指標の相関係数を算出
- 散布図による視覚的な相関関係の確認

## 技術スタック

- **Python 3.9+**
- **pandas**: データ処理
- **matplotlib**: グラフ作成
- **seaborn**: 統計的可視化
- **Flask**: Webアプリケーションフレームワーク
- **Bootstrap 5**: フロントエンドUI

## API エンドポイント

- `GET /`: メインダッシュボード
- `GET /api/analysis`: 解析結果JSON取得
- `GET /api/rerun-analysis`: 解析再実行

## 注意事項

- 初回実行時は解析に数秒かかる場合があります
- 大量のデータを扱う場合は、メモリ使用量にご注意ください
- 画像ファイルは static/images/ ディレクトリに保存されます