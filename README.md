# Pollen App

花粉の飛散状況を確認するためのアプリケーションです。

## 機能
- 花粉情報の表示
- エリア選択機能
- データベース（SQLite）によるデータ管理
- Open-Meteo API から最新花粉データを取り込み

## セットアップ手順
プロジェクトをクローンした後、以下の手順で環境を構築してください。

### 1. 仮想環境の作成と有効化
```bash
python -m venv venv
# Windowsの場合
.\venv\Scripts\activate

# Mac/Linuxの場合
source venv/bin/activate
```

### 2. Flask の起動
```bash
cd venv/Apps
python main.py
```

### API
- `GET /areas/<area_key>`
  - DBにデータがない場合は外部APIから自動取得して返却
  `GET /api/areas`
  - DBに保存されている全レコードを返却
  `POST /api/areas/<ara_key>/sync`
  - 外部APIから最新データを取り込みDBに保存

対応エリアキー: `tokyo`, `osaka`, `nagoya`, `hokkaido`
