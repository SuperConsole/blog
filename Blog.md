  
  
# [SpCn-Blog](https://github.com/SuperConsole/SpCn-Diary/tree/master)  
Blog: セキュリティ・ハッキング・Tor・ダークウェブなど  

## Burp Suiteで構築するHTTPSプロキシ(07/24/19)
　前回はOWASP ZAPを使って自前で運用しているWebサイトの脆弱性を診断しました。  
今回はBurp Suiteを用いてローカルプロキシを立ち上げ、中継されるリクエスト/レスポンスを傍受または改竄できるかを試してみます。  
  
　流れ:  
　　1. https://portswigger.net/burp からBurp Suiteをダウンロード、適宜インストール  
　　　　＊Kali Linuxユーザは既にBurp Suiteが同梱されているのでそれを用いるてもよい  
    
　　2. Burp Suiteを起動した後にブラウザ(Firefox等)で「127.0.0.1:8080」をプロキシに登録する  
  
　　3. ブラウザで「127.0.0.1:8080」にアクセス、Burpの証明書をインポートする  
  
　　4. 以降通信内容がすべてプロキシに記録される  
 <img src="https://raw.githubusercontent.com/SuperConsole/SpCn-Diary/master/src/img/Burp-Suite-Https-Log.png" width="100%" style="max-width:400px;">
  
　　5. proxyタブの「Intercept is on」の状態時には通信がプロキシで一度停止  
　　　　内容を確認したり必要によって書き換えたり(悪用厳禁)して通信再開「Forward」することが可能  

　今回はBurp Suiteでローカルプロキシを立ち上げ、Burp証明書を用いてHTTPSの通信に割り込んでみました。  
この機能はOWASP ZAPでも使用可能らしいですが、個人的にこっちのが使いやすいかなーと思います。  
　ところで、OWASP ZAPとBurp Suiteの用途の違いが曖昧でよくわかっていなかった自分ですが調べたところBurp SuiteはOSSではないらしいです。今回使用した無料版はCommunity版、有料版はEnterprise版が$3999/年、Professional版が$399/年。個人ではやや厳しい価格なのかなと思いますが商用利用などを考えている場合、有料版でサポートがしっかりしていると安心なのかなと。OSSの数少ないデメリットなので。  
　次回からはWebの脆弱性診断から離れてネットワークやOS, ミドルウェアらへんに焦点を当てて行きたいところです。  
　...ブログと日記を分割しなきゃな...。おわり。

---
## OWASP ZAPを用いたWebサイトの脆弱性診断(07/15/19)
　久しぶりの投稿。今回はOWASP ZAPを用いてWebサイトの脆弱性診断を行ったのでその流れと結果を報告します。  
　OWASP ZAPはOSSで提供される脆弱性診断を行う為のアプリケーションです。機能が概ねGUIで提供されていて容易に診断、結果のフィードバックが行えます。動的スキャンを用いたのでその流れを示します。  
 
　流れ:   
　　1. 以下の公式リポジトリの「wiki」タブからダウンロード -> OSに合わせて適宜インストールする  
　　　- https://github.com/zaproxy/zaproxy  
  
　　2. OWASP ZAPを使用するためにFirefox等のブラウザでプロキシの設定を行う(以下は例)  
　　　proxy: 127.0.0.1 / port: 57777  
　　　＊これによりブラウザの通信を傍受可能になる(脆弱性診断に用いるため設定必須)
  
　　3. OWASP ZAPの証明書を生成し、ブラウザにインポートする
　　　＊基本ブラウザはFirefoxが推奨されている、プロキシや
  
　　4. OWASP ZAPを起動、ここからは参考文献(本:OWASP ZAPではじめるウェブアプリ脆弱性診断/脆弱性診断研究会)に沿って以下を設定した  
　　　モード, 診断範囲(コンテキスト, スコープ), スキャンポリシー  
  
　　5. コンテキスト内のターゲット上で動的スキャンを選択し、実行する -> アラートタブにスキャンの結果(検出した脆弱性や改善点等)が表示される  
  
　ざっくり言うとこんな流れになります。OWASP ZAPを使っていてすごいなと感じたのはこの動的スキャンの結果に「設定ミス」の類についてもフィードバックされた点ですね。自前で運営している某サイトの試験環境に動的スキャンを走らせた結果、「X-Content-Type-Optionsヘッダ」の設定がされておらず悪意のあるスクリプトがインジェクションされる危険性が潜んでいました(怖い...)。サイトの開発のなかでHTTPヘッダの設定を意識しないまま開発していたが故のミスです...。奥が深いなぁ...。  

<img src="https://raw.githubusercontent.com/SuperConsole/SpCn-Diary/master/src/img/OWASP-ZAP-result-alert.png" width="100%" style="max-width:381px;">  
  
　次は気が向いたら似たようなアプリであるBurp Suiteに触れた所感を書こうかなーと思っていたりいなかったりですね。おわり。  
  
　＊追記: HTTPヘッダの設定とセキュリティについていい感じのサイトを見つけたのでメモ  
　セキュリティを強化する7つの便利なHTTPヘッダ / https://devcentral.f5.com/s/articles/7http  
 
---
## Apache Struts 2におけるリモートコード実行[CVE-2018-11776]の脆弱性検証(07/02/19)
　某セキュリティ会社が発行している「JSOC INSIGHT」のvol.22にて「Apache Struts 2におけるリモートコード実行の脆弱性」が取り上げられていたので持ち前の情報収集力を生かしてこの脆弱性を再現・検証したのでそれをまとめます。
まず、この脆弱性はURLに数値計算式またはOSコマンドを実行するOGNL文をインジェクションすることで悪用されます。Apache Struts2の設定ファイルである「struts.xml」において、  
　 ・「alwaysSelectFullNamespace」をtrueにしている  
　 ・「actionタグ」または「urlタグ」が含まれている  
  
これらの条件をいずれも満たす場合に影響を受けます。今回の検証ではこの脆弱性を持つApache Struts 2.3.12内蔵のDockerコンテナ(piesecurity/apache-struts2-cve-2017-5638、以下Dockerコンテナ)を用意し、struts.xmlに設定を追加したのちにPoC(python)を実行し、サーバ内の機密情報(ここでは/etc/passwdファイル)を読み取るまでの流れを示す。  
  
　方法([hook-s3c氏のPoC](https://github.com/hook-s3c/CVE-2018-11776-Python-PoC)より):  
　 1. Dockerコンテナ(piesecurity/apache-struts2-cve-2017-5638)をdockerhubよりプル  
   $docker pull piesecurity/apache-struts2-cve-2017-5638  
  
　 2. コンテナをポート32771番に指定しデタッチモードにて起動//被害側  
　  $docker run -d -p 32771:8080 piesecurity/apache-struts2-cve-2017-5638  
  
　 3.  エディタ(vim)をインストールした後設定ファイルを編集する(内容はリンク先参照,設定ファイルの様式にしたがって追加すること)  
　  $vim /usr/local/tomcat/webapps/ROOT/WEB-INF/classes/struts.xml  
  
　 4. Apache Struts2(Dockerコンテナ)を再起動  
　  $exit  
　  $docker restart [コンテナID]  
　  $docker exec -it [コンテナID] bash  
  
　 5. 攻撃側PCからDockerコンテナの32771番ポートにアクセス　　

<img src="https://raw.githubusercontent.com/SuperConsole/SpCn-Diary/master/src/img/CVE-2018-11776-poc-struts2.png" width="100%" style="max-width:400px;">  
  
　 6. URLの指定部(JSOC INSIGHTを参照)にOGNL文を挿入する([atucom.net](http://blog.atucom.net/2018/08/apache-struts-2-vulnerability-exploit.html)よりOSコマンドからOGNL文生成するPoCが公開されているのでこれを利用した。ウイルスに感染する恐れがあるので実行は自己責任)  
　  $python ./a.py  
  
　 7. OSインジェクションが行われ、攻撃側にて被害側内にある機密情報/etc/passwdファイル)の読み取りに成功していることを確認できる。  

<img src="https://raw.githubusercontent.com/SuperConsole/SpCn-Diary/master/src/img/CVE-2018-11776-poc-result.png" width="100%" style="max-width:600px;">  
  
　以上。数値計算式を挿入するPoCはザッと調べただけでもかなりのサイトに載っていたが実際に悪用可能なOGNL文を挿入するコードを公開するJSOC INSIGHTは一味違うなと実感しました(誰目線)。話は変わるのですが、以前[PoCに見せかけて本当にリモートで実行されるやつ](https://web.archive.org/web/20190702145836/https:/twitter.com/x64koichi/status/1141635520419602432/photo/1)が巷で話題になりましたね。こういうことが少なからずあるのでPoCを使って検証するにはソースコードに目を通すことが大前提です。  
　今回の環境ではtruts.xmlの「alwaysSelectFullNamespace」を無効にしたことでONGL文によるOSインジェクションが効かなくなったこと、バージョンアップによって脆弱性が解消されたことを確認しました。セキュリティ、日頃から意識していきましょう...。おわり。


---
## VPNGate with Proxyを用いた通信の秘匿(06/15/19)
　先日にTorネットワークを用いてIPアドレスを隠蔽する方法を記事にしたが、今回は通信自体の隠蔽について。VPNGate with Proxyを用いることでVPNでの通信を可能にし、情報の盗聴を防ぐことができます。また、末端接続先(Webサイトなど)からはVPNサーバのIPアドレスしか見られない状態になります。  
 しかしVPNサーバが情報を開示した場合はIPアドレスが丸わかりになるので悪用厳禁。  
  
通信方法(Debian9):  
　1. VPNGate With Proxyに必要なアプリケーションをインストールする  
　　$apt install gir1.2-appindicator3-0.1 gir1.2-notify-0.7 python-gobject  
    
　2. VPNGate with Proxyをインストール(クローン→解凍)する(・・・部はGithubのドメイン)  
　　$git clone ・・・/Dragon2fly/vpngate-with-proxy  
　　(\*クローンしたディレクトリ配下にアプリケーションがある)   
  
　3. VPNGate with Proxyを起動する  
　　$./vpngate-with-proxy/run  
  
　4. 一覧から接続したいサーバを選択し、番号をコマンドラインに入力する  
 　　(サーバのindexが0の場合) >>0  
   
　5. コネクションの確立後、IPアドレスがサーバのものになっているか確認する  
　　$curl -sL ipinfo.io  
 
　以上。また、VPN Gateway with Proxyは筑波大学が提供するサービス「VPN Gate」の非公式Linuxクライアントである。利用する際は自己責任で。  
   
　この記事を書く上で本当は「VPN Over Tor」というTorを経由した後にVPN通信を行ってインターネットに接続する環境を構築したかったがTor経由でのVPN Gateway with Proxyのサーバへの接続がうまくいかずに断念した。原因は今も模索中であるがTorネットワークは一般的なプロキシとはやや違う仕組みで動いているのでいろいろ設定をする必要があると考えている。保証のきいたVPNサービスを利用するのが無難だが向きになっている自分がいるので一つ一つ自分のペースで対処していきます。次回はペネトレーションテストツールを使ってみたりしようかなと思っています。おわり。

---
## 防衛のためのTorネットワーク(06/14/19)
　Torとは、The Onion Routerの略でSOCKSプロキシを何重に経由することでIPアドレスの匿名性を向上させる技術を指します。もとは米軍により開発された技術ですが現在はTor Projectが管理運営をしています。IP匿名化の仕組みは説明すると長くなるので端的に言えば寄り道をしまくって経由するサーバごとにIPアドレスを書き換えるといった感じになりますね。また、SOCKSはTCPを包括するシステムなのでHTTP/HTTPSだけでなくTCP上で動作するプロトコルなら通信が可能です(もちろんUDPはできない)。  
  
通信方法:  
　1. Torをインストールする(aptコマンドなどで直接行う方法が簡単)  
　　ex: $sudo apt install tor  
　2. Torを実行する  
　　ex: $tor  
　3. Torの入り口となるプロキシを通すため、アドレスとポート番号を設定する  
　　\*具体的なアドレス、ポート番号は正規のモノを参照して適宜入力  
　4. IPアドレスが偽装できているか確認する  
　　ex: curl -sL ipinfo.io  
　　(\*IPアドレスの確認方法に関して指定はない)
  
　注意: TorはIPアドレスの匿名には貢献できるがセキュリティの信頼性を保証するものではないです。HTTPやIMAP, POPなどの通信化を行わないプロトコルでの通信は盗聴されるリスクがあります。また、中継サーバのにはトラフィックを解析したり捜査関係者のサーバが紛れ込んでいることがあるので最低限のリテラシーは必要です。  
  
　調べてみたらTor Over VPNという言葉があるらしく、Torネットワークにアクセスする前に一度VPNを通す方法で、Torネットワークの入り口ですら送信元IPを隠蔽し、匿名性を高める方法だそう。フリーだとOpenVPNなどがありますがNordVPNというところが提供している「Tor Over Vpn」といった保証付きのサービスを使うのも手段としてありですね。  
  
 <img src="https://i.imgur.com/XddQXJd.jpg" width="100%" style="max-width:900px;">
  
遅延が大変なことになりそうだけど...。  
あと、Torの話はしたもののダークウェブには興味ないです。本当に...。  
  
　あと、身元を完全に隠したいユーザには匿名OS「Tails」があり、これを使えば万が一Torの中継サーバが裏切って生身のIPが特定されても直接の被害はなくなります。以上Torに関する記事(殴り書き)でした。おわり。

---
## ハッシュによるファイルの正当性検証(06/08/19)
　何気なくインターネットからファイルをダウンロードしてファイルの正当性を疑うこともなくそのままインストールして...
でもセキュリティリテラシーの観点からするとよろしくないのでハッシュによる検証を癖つけるために記事にしました。  
方法(kali-linux-2019.2-amd64.isoの例):  

　1. 公式サイトから検証対象の.isoファイル(kali-linux-2019.2-amd64.iso)をダウンロードする  

　2. OpenSSLを使ってハッシュ(今回はサイトのアルゴリズムにしたがってsha256)を以下のコマンドで算出(パイプで渡すのは個人的な好み)  
　　$cat ./kali-linux-2019.2-amd64.iso | openssl sha256  

　3. 出力されたハッシュ値とサイト上にあるSHA256Sumの値が一致しているか確かめる  
　　>67574ee0039eaf4043a237e7c4b0...(例におけるハッシュ値)

　4. 同じであれば正当性が確立, 異なればハッシュのアルゴリズムが同じか見直すか再ダウンロードを行う

　簡単にできますね。しかし正当性の検証は大事なことです。なので忘れずにパソコンライフを送りたいと思います。  

余談:  
　ちなみに今日はデジタル署名とか認証まわりも学習していて、ネットサーフィンしてたら本物の"オレオレ証明書"のサイトを見つけました。でもChromeがちゃんと警告出してくれたのですぐに気づきました。詳細で確認するとルート証明書があからさまに怪しいドメインで面白かったです。以上。おわり。


---
## Metasploit+docker(+nmap)で試すHeartbleed(04/10/19)
　Heartbleedというメモリリークから個人・機密情報を漏洩させる脆弱性。頑張ればこの脆弱性を持ったサーバーをイントラネットに立てて擬似攻撃できるんじゃね？って思ったのでやってみました。サーバーを立てるのにdockerを使い、コンテナイメージは[hmlio/vaas-cve-2014-0160
](https://hub.docker.com/r/hmlio/vaas-cve-2014-0160/)を使用します(VaaSなんて言葉があるのな...)。以下に手順記載しますー  

1.dockerで[hmlio/vaas-cve-2014-0160
](https://hub.docker.com/r/hmlio/vaas-cve-2014-0160/)をプル  

2.ポート(usageに書いてあったので8443にした)を指定して起動(dockerhub内の手順に従った。このコンテナが被害者側)  

(2'.nmapのHeartbleed検知スクリプトを使って被害者側が脆弱性を持つか確認)  

3.攻撃者側(Kali Linux)でMetasploitを起動  

4.CVE番号で検索をかけてHeartbleedモジュールを使用  

5.オプションをいくつか設定して実行(RHOST, RPORT, VERBOSEの三つを設定した)  

6.被害者側のメモリがリークしたのを確認できた。  

ちなみに、HeartbleedはOpenSSLで暗号化通信をしていても通信の末端では復号してメモリに展開されているという隙をついた脆弱性です。もともとは接続確認とか応答の意味を兼ねてパケットをとんぼ返りするHeartbeatパケットというのがあり、その中のLengthというパケットの大きさを返すパラメータに実際の大きさを超える値をセットし、偽装した大きさと実際の大きさの差分だけメモリがリークする仕組みだ。JVNのデータを見るとOpenSSLはv1.0.1~v1.0.1fまでとのこと。執筆時点での最新版がv3.0.0なのでアップデートしていれば心配することはない。ただ、2014年に見つかったこの脆弱性は2016年ごろまで被害が起きていたことからユーザのインシデント対応の遅さが問題に繋がる原因ともなるので注意が必要です。

うーん、それにしてもただただマニュアル読んでその通りにしただけでは？スクリプトキディみたい...。でもそれだけツールが充実しているということですね。手順がかなり端折っているのは詳しく書きすぎるとクラッキングの助長になってしまうかなと思ったからです。たぶんこの記事を読んだだけでクラッキングができたら元から知ってたよね？くらいの抽象度合いなので大目にみてくださいー。あ、このコンテナでOpenSSLをアップデートして脆弱性が解消されてるか確認しようとしたけどアップデートができなかった...脆弱性確認用だから対策されてるのかな...?おわり。

参考:  
　[JVNDB-2014-001920
](https://jvndb.jvn.jp/ja/contents/2014/JVNDB-2014-001920.html)  
　[え？今さらHeartBleedの話ですか？](https://www.lac.co.jp/lacwatch/people/20161013_001056.html)
 
---
