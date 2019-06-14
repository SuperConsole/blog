# 畳み込みニューラルネットワーク(09/20/18)
```
画像の分析においては、各ピクセルデータを入力としたNNでは意味のある情報と
ノイズの比率が極端に低いため、学習が困難になる。あるいは進まない状況になる。
そこで、従来の機械学習での観点として判断材料になる情報を人間が選び、
特徴ベクトルとして作成する(特徴抽出)を見出した。
しかし、顔の認識ではあまり役に立たなかった。
畳み込みという考え方はこの画像に特化した検出の方法で、検出器(例えば"縦線"
のみに反応するものなど)を対象画像の全域に対して通して検出(この結果を特徴マップという)
していく。これが一つの特徴量として扱われる(フィルタ内の画像とフィルタとの乗算)。
CNNはこの操作をNNに取り入れたもので、ニューロンと接続の一連のまとまりにあたるものがフィルター、
隠れ層のニューロンが特徴マップとして形成されている。また、カラー(RGB)での入力は色ごとに奥行きを
持つため、入力, 特徴マップともに三次元になる。
```
---
# DeeR(09/17/18)
```
論文(Combined Reinforcement Learning via Abstract Representations)のモデルを実装したPythonライブラリ
強化学習のモデルベース型とモデルフリー型のいいとこ取りみたいな手法の提案で、
学習効率の増加につながるらしい。
論文は英語なのでよくわかんなかったのでarXivTimesの要約だけで学んだことにした。

arXivTimesの要約( https://github.com/arXivTimes/arXivTimes/issues/932 )
```
---
# TensorFlow(09/16/18)
```
TensorFlow:
    2015年にGoogleからリリースされた機械学習のライブラリ(OSS), 任意の計算をデータフローとして扱う。
    学習の流れとして、パラメータとして用意されているVariableを作成し、それを勾配降下法を使い繰り返し更新していく。
    Chainerとの違いはFW自体の実装がC++なのと、宣言的にコーディングしていくところかな。Chainer触ったこと無いので触り心地とかはわかんないや。
```