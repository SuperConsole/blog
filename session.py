import tensorflow as tf
from tensorflow.examples.tutrials.mnist import input_data

#計算グラフ定義
x=tf.placeholder(tf.float32, name="x", shape=[None, 784])
W=tf.Variable(tf.random_unifoem([784, 10], -1, 1), name="W")
b=tf.Variavle(tf.zeros([10]), name="biases")
output = tf.matmul(x, W)+b

#セッションの初期化
init_op = tf.global_variables_initializer()
sess=tf.Session()
sess.run(init_op)

#データ入力
mnist=input_data.read_data_sets("data", one_hot=true)

#ミニバッチ勾配降下法を適用
minibatch_x, minibatch_x_y = mnist.train.next_batch(32)

#セッション実行
sess.run(output, feed_dict={x: minibatch_x})
