# 台湾留学情報サイト　- Looben

[※ ここからサイトへ移動できます](http://looben.org)  
[※ このプロジェクトの振り返り記事](https://kanta-blog.tokyo/looben-review/)

1. [概要](#概要)
2. [使用技術](#使用技術)


## 概要
台湾留学という選択をする学生が、後悔のない大学生活を送れるように、情報の少ない台湾の大学情報をまとめ、交流できるwebアプリ。
現役留学生に質問したり、現役留学生による台湾の大学の口コミを見ることで、リアルな大学情報を手軽に得ることができます。


## 使用技術
- Python 3.9
- Django 4.1
- Postgres
- psycopg2-binary
- python-dotenv
- AWS(EC2)
- nginx
- gunicorn
- postgreSQL

## 機能一覧
- ユーザー登録、ログイン,ログアウト機能
- 大学検索機能
- プロフィール編集機能
- 就活状況登録、削除、編集機能
- 留学情報登録、削除、編集機能
- 留学情報検索機能
- リアルタイムチャット機能
- フォロー機能
- 質問作成、回答、ベストアンサー機能
- 質問検索機能
- 大学の口コミ作成機能

## ER図
![Looben ER図](https://user-images.githubusercontent.com/96579474/233837300-fac1870a-ff00-4b40-855d-85444e20c891.png)

## System Architecure
![Looben SystemArchitecture](https://user-images.githubusercontent.com/96579474/233837318-9a045687-5b8a-409a-acad-88b3439c020f.png)
