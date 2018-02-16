# twitter_locked_follwer_teller
鍵アカウントフォロー，フォロー解除通知用バックシールドシステムのソース．

![例](https://raw.githubusercontent.com/HexagramNM/twitter_locked_follower_teller/master/TwitterLockedFollowerTeller.PNG)


実際の実行にはTwitter APIのアクセストークン等の情報や，データベース用のファイル"followerlists.txt"，エラーログ用のファイル"error_log.txt"が必要．

LockedFollowerTeller.pyを実行することで，前回実行時から新たにフォローされた鍵アカウント，フォロー解除されたアカウントがあればDM経由で通知される．鍵アカウントからフォローされた場合は自分自身に対して通知用リプライも飛ばされる（エゴサにより参照可能）

・エラーが生じた際のエラーログ記録機能つき

最初に引数として-initをつけて実行し，"followerlists.txt"を作成してください．
また，コード内のaccount_screen_nameを自身のアカウント名に変更してください．
