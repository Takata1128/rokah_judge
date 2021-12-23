# rokah_judge
rokah (offline) judge

# Setup
## Local
```
./docker-compose_up.sh
```
して、ブラウザでlocalhost:9123に接続

## Deploy

```
docker context use <ecsのcontext>
docker compose up
```

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
