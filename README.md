# rokah_judge
rokah (offline) judge

# Setup
```
./docker-compose_up.sh
```
して、ブラウザでlocalhost:9090に接続
```
docker exec -it app /bin/bash
./entrypoint.sh
```
で、デフォルトの問題と言語が追加される。（なんとかしたい...）
# TODO
サンプルの表示
テストケース修正機能
ユーザーページ
submissionにRE,CE時のエラーメッセージ追加
ジャッジコードガバ修正
言語追加
