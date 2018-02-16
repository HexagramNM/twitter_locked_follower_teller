import json
import sys
import os.path
import traceback
from twitter import *
commandline_args = sys.argv
commandline_argc = len(sys.argv)
#下のアカウント名を自分自身のものに変更すること
account_screen_name = "HexagramNM"

log_file = open("error_log.txt", "a")
sys.stderr = log_file
try:
    with open("secret.json") as f:
        secretjson = json.load(f)

    t = Twitter(auth=OAuth(secretjson["access_token"], secretjson["access_token_secret"], secretjson["consumer_key"], secretjson["consumer_secret"]))
    newfollowerlists = t.followers.ids(screen_name=account_screen_name, stringify_ids=True, account=5000)['ids']
    if commandline_argc == 2 and commandline_args[1] == '-init':
        followerfile = open("followerlists.txt", "a")
        for id_str in newfollowerlists:
            followerfile.write(id_str + '\n')
        followerfile.close()
        sys.exit()
    else:
        if not os.path.exists("followerlists.txt"):
            sys.stderr.write("Please execute this code with the option \'-init\' at first.\n")
            log_file.close()
            sys.exit()
        followerfile = open("followerlists.txt", "r")
        filelines = followerfile.readlines()
        oldfollowerlists = []
        newLockedUserExist = False
        follower_elase = False
        delete_account_num = 0
        followerfile.close()
        for line in filelines:
            if not line=='\n':
                follower = line.rstrip('\n')
                oldfollowerlists.extend([follower])

        DM_string = ""
        for old_id in oldfollowerlists:
            if not(old_id in newfollowerlists):
                follower_elase = True
                try:
                    old_account = t.users.lookup(user_id=old_id)
                    DM_string = DM_string + old_account[0]['name'] + "さん（@" + old_account[0]['screen_name'] + "）からのフォローが解除されました．\n"
                except:
                    delete_account_num += 1
        if delete_account_num > 0:
            DM_string = DM_string + "その他，" + str(delete_account_num) + "人のフォロワーが削除されています．\n"
        if follower_elase:
            t.direct_messages.new(screen_name=account_screen_name, text=DM_string)

        DM_string = ""
        for new_id in newfollowerlists:
            if not(new_id in oldfollowerlists):
                new_account = t.users.lookup(user_id=new_id)
                if new_account[0]['protected'] == True:
                    DM_string = DM_string + "鍵垢の" + new_account[0]['name'] + "さん (@" + new_account[0]['screen_name'] + ") にフォローされました．\n"
                    newLockedUserExist = True
        if newLockedUserExist:
            t.direct_messages.new(screen_name=account_screen_name, text=DM_string)

    if(newLockedUserExist):
        t.statuses.update(status="@" + account_screen_name + "\n通知：新しい鍵垢フォロワーを確認．\n推奨：DMの確認．")
    datefile = open("followerlists.txt", "w")
    for line in newfollowerlists:
        datefile.write(line + '\n')
    datefile.close()
except:
    sys.stderr.write(traceback.format_exc())
log_file.close()
