#https://github.com/tensorflow/probability/blob/master/tensorflow_probability/examples/jupyter_notebooks/A_Tour_of_TensorFlow_Probability.ipynb
import tensorflow as tf
print(tf.__version__)
import tensorflow_probability as tfp
tfd = tfp.distributions
tfb = tfp.bijectors

mats = tf.random.uniform(shape=[1000, 10, 10])
vecs = tf.random.uniform(shape=[1000, 10, 1])

import numpy as np
def for_loop_solve():
  return np.array(
    [tf.linalg.solve(mats[i, ...], vecs[i, ...]) for i in range(1000)])

def vectorized_solve():
  return tf.linalg.solve(mats, vecs)

# Vectorization for the win!
for_loop_solve()
%timeit vectorized_solve()

a = tf.constant(np.pi)
b = tf.constant(np.e)
with tf.GradientTape() as tape:
  tape.watch([a, b])
  c = .5 * (a**2 + b**2)
grads = tape.gradient(c, [a, b])
print(grads[0])
print(grads[1])

normal = tfd.Normal(loc=0., scale=1.)
print(normal)

import seaborn as sns
samples = normal.sample(1000)
sns.distplot(samples)



normal.log_prob(0.)

normal_cdf = tfp.bijectors.NormalCDF()
xs = np.linspace(-4., 4., 200)
import matplotlib.pyplot as plt
plt.plot(xs, normal_cdf.forward(xs))

exp_bijector = tfp.bijectors.Exp()
log_normal = exp_bijector(tfd.Normal(0., .5))

samples = log_normal.sample(1000)
xs = np.linspace(1e-10, np.max(samples), 200)
sns.distplot(samples, norm_hist=True, kde=False)
plt.plot(xs, log_normal.prob(xs), c='k', alpha=.75)


def f(x, w):
  x = tf.pad(x, [[1, 0], [0, 0]], constant_values=1)
  linop = tf.linalg.LinearOperatorFullMatrix(w[..., np.newaxis])
  result = linop.matmul(x, adjoint=True)
  return result[..., 0, :]

num_features = 2
num_examples = 50
noise_scale = .5
true_w = np.array([-1., 2., 3.])

xs = np.random.uniform(-1., 1., [num_features, num_examples])
ys = f(xs, true_w) + np.random.normal(0., noise_scale, size=num_examples)
# Visualize the data set
plt.scatter(*xs, c=ys, s=100, linewidths=0)

grid = np.meshgrid(*([np.linspace(-1, 1, 100)] * 2))
xs_grid = np.stack(grid, axis=0)
fs_grid = f(xs_grid.reshape([num_features, -1]), true_w)
fs_grid = np.reshape(fs_grid, [100, 100])
plt.contour(xs_grid[0, ...], xs_grid[1, ...], fs_grid, 20, linewidths=1)


import datetime
datetime
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
  ])

import matplotlib.pyplot as plt
plt.style.use('dark_background')
plt.plot(range(1,100),range(2,101))

model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(x=x_train,
          y=y_train,
          epochs=5,
          validation_data=(x_test, y_test),
          callbacks=[tensorboard_callback])





 #tensorboard --logdir logs/gradient_tape

import tensorflow as tf
import datetime
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

def create_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
  ])


model = create_model()
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(x=x_train,
          y=y_train,
          epochs=5,
          validation_data=(x_test, y_test),
          callbacks=[tensorboard_callback])





 #tensorboard --logdir logs/gradient_tape



import tensorflow as tf
tf.
import tensorflow.probability as tfp



# Pretend to load synthetic data set.
features = tfp.distributions.Normal(loc=0., scale=1.).sample(int(100e3))
labels = tfp.distributions.Bernoulli(logits=1.618 * features).sample()

# Specify model.
model = tfp.glm.Bernoulli()

# Fit model given data.
coeffs, linear_response, is_converged, num_iter = tfp.glm.fit(
    model_matrix=features[:, tf.newaxis],
    response=tf.cast(labels,tf.float32),
    model=model)

#https://matrices.io/deep-neural-network-from-scratch/ using https://www.tensorflow.org/alpha/guide/eager
#!sudo pip3 install tf-nightly-2.0-preview #guide https://threader.app/thread/1105139360226140160
import tensorflow as tf
#tf.enable_eager_execution()
tf.executing_eagerly()
tf.test.is_gpu_available()#:with tf.device("/gpu:0"):
tf.keras.backend.clear_session()

inp=[0.05,0.10]
inpw=[[0.15,0.25],[0.20,0.3]]
hidw=[[0.4,0.5],[0.45,0.55]]
outputr=[0.01,0.99]
bias=[0.35,0.6]
lr=0.5

w1 = tf.Variable(inpw)
w2 = tf.Variable(hidw)
x = tf.constant(inp)
y = tf.constant(outputr)

layer_1 = 1/(1+tf.exp(-(tf.add(tf.matmul([x], w1), bias[0]))))
layer_2 = 1/(1+tf.exp(-(tf.add(tf.matmul(layer_1, w2), bias[1]))))
print(layer_2)

@tf.custom_gradient
def log1pexp(x):
  e = tf.exp(x)
  def grad(dy):
    return dy * (1 - 1 / (1 + e))
  return tf.math.log(1 + e), grad


def grad_log1pexp(x):
  with tf.GradientTape() as tape:
    tape.watch(x)
    value = log1pexp(x)
  return tape.gradient(value, x)

grad_log1pexp(tf.constant(100.))#.numpy()

regularization = tf.nn.l2_loss(w1) + tf.nn.l2_loss(w2)
loss = tf.reduce_mean(tf.square(layer_2 - y))
learning_rate = lr

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(2,1)),
  tf.keras.layers.Dense(2, activation='relu'),
  tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(x.reshape(2,1), y, epochs=1,steps_per_epoch=1)
#model.fit([[2,1],[1,2],[1,1]], y, epochs=1,steps_per_epoch=1)
#model.evaluate(x, y)


#https://www.tensorflow.org/alpha/guide/autograph
@tf.function
def simple_nn_layer(x, y):
  return tf.nn.relu(tf.matmul(x, y))


x = tf.random.uniform((3, 3))
y = tf.random.uniform((3, 3))

simple_nn_layer(x, y)

def square_if_positive_vectorized(x):
  return tf.where(x > 0, x ** 2, x)

square_if_positive_vectorized(tf.range(-5, 5))

from tensorflow.keras import layers
original_dim = 784
intermediate_dim = 64
latent_dim = 32

class Sampling(layers.Layer):
  """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

  def call(self, inputs):
    z_mean, z_log_var = inputs
    batch = tf.shape(z_mean)[0]
    dim = tf.shape(z_mean)[1]
    epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon
# Define encoder model.
original_inputs = tf.keras.Input(shape=(original_dim,), name='encoder_input')
x = layers.Dense(intermediate_dim, activation='relu')(original_inputs)
z_mean = layers.Dense(latent_dim, name='z_mean')(x)
z_log_var = layers.Dense(latent_dim, name='z_log_var')(x)
z = Sampling()((z_mean, z_log_var))
encoder = tf.keras.Model(inputs=original_inputs, outputs=z, name='encoder')

# Define decoder model.
latent_inputs = tf.keras.Input(shape=(latent_dim,), name='z_sampling')
x = layers.Dense(intermediate_dim, activation='relu')(latent_inputs)
outputs = layers.Dense(original_dim, activation='sigmoid')(x)
decoder = tf.keras.Model(inputs=latent_inputs, outputs=outputs, name='decoder')

# Define VAE model.
outputs = decoder(z)
vae = tf.keras.Model(inputs=original_inputs, outputs=outputs, name='vae')

# Add KL divergence regularization loss.
kl_loss = - 0.5 * tf.reduce_sum(
    z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1)
vae.add_loss(kl_loss)

# Train.
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
vae.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
(x_train, _), _ = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(60000, 784).astype('float32') / 255
vae.fit(x_train, x_train, epochs=3, batch_size=64)


#https://www.tensorflow.org/tensorboard/r2/get_started
import datetime
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
test_log_dir = 'logs/gradient_tape/' + current_time + '/test'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer = tf.summary.create_file_writer(test_log_dir)
tf.summary.summary_scope
#train_loss.reset_states()
#test_loss.reset_states()
#train_accuracy.reset_states()
#test_accuracy.reset_states()

#!python3 -m tensorflow.tensorboard  --logdir logs/gradient_tape
#python -m tensorflow.tensorboard
#%tensorboard --logdir logs/gradient_tape

import pandas as pd
data = pd.read_csv('F:/OneDrive - NTNU/UTR/data2.csv')
data.head()
data.describe()

import matplotlib.pyplot as plt
import numpy as np
data['RFPlog']=np.log2(data['Fluorescence'])
data['RFPlog'].hist()

data['ReadsLog']=np.log2(data['#Reads Col'])
data['ReadsLog'].hist()
plt.scatter(data['RFPlog'],data['ReadsLog'])
plt.scatter(data['RFPlog'],data['ReadsLog'])

from functools import reduce
DNAortho = ('A','1000') , ('T','0100') ,  ('G','0010'), ('C','0001')
data['DNASeqOrtho']=reduce(lambda a, kv: a.str.replace(*kv), DNAortho, data['Sequence'])
print(data['DNASeqOrtho'])


df = data.dropna(axis=1, how='all')
df = df.dropna(axis=0, how='all')

input=df['DNASeqOrtho'].apply(lambda x: pd.Series(list(x)))
input = input.dropna(axis=1, how='all')
input = input.dropna(axis=0, how='all')
input.describe()

output=data['RFPlog']
output.describe()

import seaborn as sns
corr=input.corr()
sns.heatmap(corr)
#sns.pairplot(input)
#https://colab.research.google.com/github/kweinmeister/notebooks/blob/master/tensorflow-shap-college-debt.ipynb#scrollTo=NSmjv4K4sl8C
def build_model(df):
  model = keras.Sequential([
    layers.Dense(16, activation=tf.nn.relu, input_shape=[len(df.keys())]),
    layers.Dense(16, activation=tf.nn.relu),
    layers.Dense(1)
  ])

  # TF 2.0: optimizer = tf.keras.optimizers.RMSprop()
  optimizer = tf.keras.optimizers.RMSprop()
  # optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae'])
  return model

model = build_model(df_train_normed)
model.summary()

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

history = model.fit(
  df_train_normed, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[early_stop, PrintDot()])
 hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch

def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Absolute Error')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  plt.legend()
plot_history(history)


import shap
shap.initjs()
df_train_normed_summary = shap.kmeans(df_train_normed.values, 25)
explainer = shap.KernelExplainer(model.predict, df_train_normed_summary)
shap_values = explainer.shap_values(df_train_normed.values)
shap.summary_plot(shap_values[0], df_train)
INSTANCE_NUM = 0
shap.force_plot(explainer.expected_value[0], shap_values[0][INSTANCE_NUM], df_train.iloc[INSTANCE_NUM,:])
NUM_ROWS = 10
shap.force_plot(explainer.expected_value[0], shap_values[0][0:NUM_ROWS], df_train.iloc[0:NUM_ROWS])
shap.dependence_plot('FIRST_GEN', shap_values[0], df_train, interaction_index='PPTUG_EF')
explainer = shap.DeepExplainer(model, df_train_normed)
shap_values = explainer.shap_values(df_train_normed.values)
shap.summary_plot(shap_values[0], df_train)


import autokeras as ak
clf = ak.ImageClassifier()
clf.fit(input, output)
results = clf.predict(input)



import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)




def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.

  It does a matrix multiply, bias add, and then uses relu to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights)
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases)
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate)
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations)
    return activations

#hidden1 = nn_layer(x_train, 784, 500, 'layer1')

with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32)
  tf.summary.scalar('dropout_keep_probability', keep_prob)
  dropped = tf.nn.dropout(hidden1, keep_prob)

# Do not apply softmax activation yet, see below.
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

with tf.name_scope('cross_entropy'):
  # The raw formulation of cross-entropy,
  #
  # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
  #                               reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.losses.sparse_softmax_cross_entropy on the
  # raw logit outputs of the nn_layer above.
  with tf.name_scope('total'):
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
  train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(
      cross_entropy)

with tf.name_scope('accuracy'):
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to /tmp/mnist_logs (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/train',
                                      sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/test')
tf.global_variables_initializer().run()



# Train the model, and also write summaries.
# Every 10th step, measure test-set accuracy, and write test summaries
# All other steps, run train_step on training data, & add training summaries

def feed_dict(train):
  """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
  if train or FLAGS.fake_data:
    xs, ys = mnist.train.next_batch(100, fake_data=FLAGS.fake_data)
    k = FLAGS.dropout
  else:
    xs, ys = mnist.test.images, mnist.test.labels
    k = 1.0
  return {x: xs, y_: ys, keep_prob: k}

for i in range(FLAGS.max_steps):
  if i % 10 == 0:  # Record summaries and test-set accuracy
    summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
    test_writer.add_summary(summary, i)
    print('Accuracy at step %s: %s' % (i, acc))
  else:  # Record train set summaries, and train
    summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
    train_writer.add_summary(summary, i)




tensorboard --logdir=path/to/log-directory



def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.

  It does a matrix multiply, bias add, and then uses ReLU to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights)
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases)
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate)
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations)
    return activations

hidden1 = nn_layer(x, 784, 500, 'layer1')

with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32)
  tf.summary.scalar('dropout_keep_probability', keep_prob)
  dropped = tf.nn.dropout(hidden1, keep_prob)

# Do not apply softmax activation yet, see below.
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

with tf.name_scope('cross_entropy'):
  # The raw formulation of cross-entropy,
  #
  # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
  #                               reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.losses.sparse_softmax_cross_entropy on the
  # raw logit outputs of the nn_layer above, and then average across
  # the batch.
  with tf.name_scope('total'):
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(
        labels=y_, logits=y)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
  train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(
      cross_entropy)

with tf.name_scope('accuracy'):
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to
# /tmp/tensorflow/mnist/logs/mnist_with_summaries (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.log_dir + '/train', sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.log_dir + '/test')
tf.global_variables_initializer().run()



import tensorflow as tf
import numpy as np

X_train = (np.random.sample((10000,5)))
y_train =  (np.random.sample((10000,1)))
X_train.shape

feature_columns = [
      tf.feature_column.numeric_column('x', shape=X_train.shape[1:])]
DNN_reg = tf.estimator.DNNRegressor(feature_columns=feature_columns,
# Indicate where to store the log file
     model_dir='train/linreg',
     hidden_units=[500, 300],
     optimizer=tf.train.AdamOptimizer(
          learning_rate=0.1,
          l1_regularization_strength=0.001
      )
)

# Train the estimator
train_input = tf.estimator.inputs.numpy_input_fn(
     x={"x": X_train},
     y=y_train, shuffle=False,num_epochs=None)
DNN_reg.train(train_input,steps=3000)


import tensorflow as tf

k = tf.float32

# Make a normal distribution, with a shifting mean
mean_moving_normal = tf.random_normal(shape=[1000], mean=(5*k), stddev=1)
# Record that distribution into a histogram summary
tf.summary.histogram("normal/moving_mean", mean_moving_normal)

# Setup a session and summary writer
sess = tf.Session()
writer = tf.summary.FileWriter("/tmp/histogram_example")

summaries = tf.summary.merge_all()

# Setup a loop and write the summaries to disk
N = 400
for step in range(N):
  k_val = step/float(N)
  summ = sess.run(summaries, feed_dict={k: k_val})
  writer.add_summary(summ, global_step=step)


import tensorflow as tf
import tensorflow_probability as tfp

# Pretend to load synthetic data set.
features = tfp.distributions.Normal(loc=0., scale=1.).sample(int(100e3))
labels = tfp.distributions.Bernoulli(logits=1.618 * features).sample()

# Specify model.
model = tfp.glm.Bernoulli()

# Fit model given data.
coeffs, linear_response, is_converged, num_iter = tfp.glm.fit(
    model_matrix=features[:, tf.newaxis],
    response=tf.cast(labels,tf.float32),
    model=model)

#https://matrices.io/deep-neural-network-from-scratch/ using https://www.tensorflow.org/alpha/guide/eager
#!sudo pip3 install tf-nightly-2.0-preview #guide https://threader.app/thread/1105139360226140160
import tensorflow as tf
print(tf.__version__)
#tf.enable_eager_execution()
tf.executing_eagerly()
tf.test.is_gpu_available()#:with tf.device("/gpu:0"):
tf.keras.backend.clear_session()

inp=[0.05,0.10]
inpw=[[0.15,0.25],[0.20,0.3]]
hidw=[[0.4,0.5],[0.45,0.55]]
outputr=[0.01,0.99]
bias=[0.35,0.6]
lr=0.5

w1 = tf.Variable(inpw)
w2 = tf.Variable(hidw)
x = tf.constant(inp)
y = tf.constant(outputr)

layer_1 = 1/(1+tf.exp(-(tf.add(tf.matmul([x], w1), bias[0]))))
layer_2 = 1/(1+tf.exp(-(tf.add(tf.matmul(layer_1, w2), bias[1]))))
print(layer_2)

@tf.custom_gradient
def log1pexp(x):
  e = tf.exp(x)
  def grad(dy):
    return dy * (1 - 1 / (1 + e))
  return tf.math.log(1 + e), grad


def grad_log1pexp(x):
  with tf.GradientTape() as tape:
    tape.watch(x)
    value = log1pexp(x)
  return tape.gradient(value, x)

grad_log1pexp(tf.constant(100.))#.numpy()

regularization = tf.nn.l2_loss(w1) + tf.nn.l2_loss(w2)
loss = tf.reduce_mean(tf.square(layer_2 - y))
learning_rate = lr

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(2,1)),
  tf.keras.layers.Dense(2, activation='relu'),
  tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#model.fit(x.reshape(2,1), y, epochs=1,steps_per_epoch=1)
#model.fit([[2,1],[1,2],[1,1]], y, epochs=1,steps_per_epoch=1)
#model.evaluate(x, y)


#https://www.tensorflow.org/alpha/guide/autograph
@tf.function
def simple_nn_layer(x, y):
  return tf.nn.relu(tf.matmul(x, y))


x = tf.random.uniform((3, 3))
y = tf.random.uniform((3, 3))

simple_nn_layer(x, y)

def square_if_positive_vectorized(x):
  return tf.where(x > 0, x ** 2, x)

square_if_positive_vectorized(tf.range(-5, 5))

from tensorflow.keras import layers
original_dim = 784
intermediate_dim = 64
latent_dim = 32

class Sampling(layers.Layer):
  """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""

  def call(self, inputs):
    z_mean, z_log_var = inputs
    batch = tf.shape(z_mean)[0]
    dim = tf.shape(z_mean)[1]
    epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
    return z_mean + tf.exp(0.5 * z_log_var) * epsilon
# Define encoder model.
original_inputs = tf.keras.Input(shape=(original_dim,), name='encoder_input')
x = layers.Dense(intermediate_dim, activation='relu')(original_inputs)
z_mean = layers.Dense(latent_dim, name='z_mean')(x)
z_log_var = layers.Dense(latent_dim, name='z_log_var')(x)
z = Sampling()((z_mean, z_log_var))
encoder = tf.keras.Model(inputs=original_inputs, outputs=z, name='encoder')

# Define decoder model.
latent_inputs = tf.keras.Input(shape=(latent_dim,), name='z_sampling')
x = layers.Dense(intermediate_dim, activation='relu')(latent_inputs)
outputs = layers.Dense(original_dim, activation='sigmoid')(x)
decoder = tf.keras.Model(inputs=latent_inputs, outputs=outputs, name='decoder')

# Define VAE model.
outputs = decoder(z)
vae = tf.keras.Model(inputs=original_inputs, outputs=outputs, name='vae')

# Add KL divergence regularization loss.
kl_loss = - 0.5 * tf.reduce_sum(
    z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1)
vae.add_loss(kl_loss)

# Train.
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
vae.compile(optimizer, loss=tf.keras.losses.MeanSquaredError())
(x_train, _), _ = tf.keras.datasets.mnist.load_data()
x_train = x_train.reshape(60000, 784).astype('float32') / 255
vae.fit(x_train, x_train, epochs=3, batch_size=64)


#https://www.tensorflow.org/tensorboard/r2/get_started
import datetime
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
test_log_dir = 'logs/gradient_tape/' + current_time + '/test'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer = tf.summary.create_file_writer(test_log_dir)
tf.summary.summary_scope
#train_loss.reset_states()
#test_loss.reset_states()
#train_accuracy.reset_states()
#test_accuracy.reset_states()

#!python3 -m tensorflow.tensorboard  --logdir logs/gradient_tape
#python -m tensorflow.tensorboard
#%tensorboard --logdir logs/gradient_tape

import pandas as pd
data = pd.read_csv('F:/OneDrive - NTNU/UTR/data2.csv')
data.head()
data.describe()

import matplotlib.pyplot as plt
import numpy as np
data['RFPlog']=np.log2(data['Fluorescence'])
data['RFPlog'].hist()

data['ReadsLog']=np.log2(data['#Reads Col'])
data['ReadsLog'].hist()
plt.scatter(data['RFPlog'],data['ReadsLog'])
plt.scatter(data['RFPlog'],data['ReadsLog'])

from functools import reduce
DNAortho = ('A','1000') , ('T','0100') ,  ('G','0010'), ('C','0001')
data['DNASeqOrtho']=reduce(lambda a, kv: a.str.replace(*kv), DNAortho, data['Sequence'])
print(data['DNASeqOrtho'])


df = data.dropna(axis=1, how='all')
df = df.dropna(axis=0, how='all')

input=df['DNASeqOrtho'].apply(lambda x: pd.Series(list(x)))
input = input.dropna(axis=1, how='all')
input = input.dropna(axis=0, how='all')
input.describe()

output=data['RFPlog']
output.describe()

import seaborn as sns
corr=input.corr()
sns.heatmap(corr)
#sns.pairplot(input)
#https://colab.research.google.com/github/kweinmeister/notebooks/blob/master/tensorflow-shap-college-debt.ipynb#scrollTo=NSmjv4K4sl8C
def build_model(df):
  model = keras.Sequential([
    layers.Dense(16, activation=tf.nn.relu, input_shape=[len(df.keys())]),
    layers.Dense(16, activation=tf.nn.relu),
    layers.Dense(1)
  ])

  # TF 2.0: optimizer = tf.keras.optimizers.RMSprop()
  optimizer = tf.keras.optimizers.RMSprop()
  # optimizer = tf.train.RMSPropOptimizer(learning_rate=0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae'])
  return model

model = build_model(df_train_normed)
model.summary()

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)

history = model.fit(
  df_train_normed, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[early_stop, PrintDot()])
 hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch

def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Absolute Error')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  plt.legend()
plot_history(history)


import shap
shap.initjs()
df_train_normed_summary = shap.kmeans(df_train_normed.values, 25)
explainer = shap.KernelExplainer(model.predict, df_train_normed_summary)
shap_values = explainer.shap_values(df_train_normed.values)
shap.summary_plot(shap_values[0], df_train)
INSTANCE_NUM = 0
shap.force_plot(explainer.expected_value[0], shap_values[0][INSTANCE_NUM], df_train.iloc[INSTANCE_NUM,:])
NUM_ROWS = 10
shap.force_plot(explainer.expected_value[0], shap_values[0][0:NUM_ROWS], df_train.iloc[0:NUM_ROWS])
shap.dependence_plot('FIRST_GEN', shap_values[0], df_train, interaction_index='PPTUG_EF')
explainer = shap.DeepExplainer(model, df_train_normed)
shap_values = explainer.shap_values(df_train_normed.values)
shap.summary_plot(shap_values[0], df_train)


import autokeras as ak
clf = ak.ImageClassifier()
clf.fit(input, output)
results = clf.predict(input)



import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(512, activation=tf.nn.relu),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)




def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.

  It does a matrix multiply, bias add, and then uses relu to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights)
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases)
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate)
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations)
    return activations

#hidden1 = nn_layer(x_train, 784, 500, 'layer1')

with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32)
  tf.summary.scalar('dropout_keep_probability', keep_prob)
  dropped = tf.nn.dropout(hidden1, keep_prob)

# Do not apply softmax activation yet, see below.
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

with tf.name_scope('cross_entropy'):
  # The raw formulation of cross-entropy,
  #
  # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
  #                               reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.losses.sparse_softmax_cross_entropy on the
  # raw logit outputs of the nn_layer above.
  with tf.name_scope('total'):
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(labels=y_, logits=y)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
  train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(
      cross_entropy)

with tf.name_scope('accuracy'):
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to /tmp/mnist_logs (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/train',
                                      sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.summaries_dir + '/test')
tf.global_variables_initializer().run()



# Train the model, and also write summaries.
# Every 10th step, measure test-set accuracy, and write test summaries
# All other steps, run train_step on training data, & add training summaries

def feed_dict(train):
  """Make a TensorFlow feed_dict: maps data onto Tensor placeholders."""
  if train or FLAGS.fake_data:
    xs, ys = mnist.train.next_batch(100, fake_data=FLAGS.fake_data)
    k = FLAGS.dropout
  else:
    xs, ys = mnist.test.images, mnist.test.labels
    k = 1.0
  return {x: xs, y_: ys, keep_prob: k}

for i in range(FLAGS.max_steps):
  if i % 10 == 0:  # Record summaries and test-set accuracy
    summary, acc = sess.run([merged, accuracy], feed_dict=feed_dict(False))
    test_writer.add_summary(summary, i)
    print('Accuracy at step %s: %s' % (i, acc))
  else:  # Record train set summaries, and train
    summary, _ = sess.run([merged, train_step], feed_dict=feed_dict(True))
    train_writer.add_summary(summary, i)




tensorboard --logdir=path/to/log-directory



def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)

def nn_layer(input_tensor, input_dim, output_dim, layer_name, act=tf.nn.relu):
  """Reusable code for making a simple neural net layer.

  It does a matrix multiply, bias add, and then uses ReLU to nonlinearize.
  It also sets up name scoping so that the resultant graph is easy to read,
  and adds a number of summary ops.
  """
  # Adding a name scope ensures logical grouping of the layers in the graph.
  with tf.name_scope(layer_name):
    # This Variable will hold the state of the weights for the layer
    with tf.name_scope('weights'):
      weights = weight_variable([input_dim, output_dim])
      variable_summaries(weights)
    with tf.name_scope('biases'):
      biases = bias_variable([output_dim])
      variable_summaries(biases)
    with tf.name_scope('Wx_plus_b'):
      preactivate = tf.matmul(input_tensor, weights) + biases
      tf.summary.histogram('pre_activations', preactivate)
    activations = act(preactivate, name='activation')
    tf.summary.histogram('activations', activations)
    return activations

hidden1 = nn_layer(x, 784, 500, 'layer1')

with tf.name_scope('dropout'):
  keep_prob = tf.placeholder(tf.float32)
  tf.summary.scalar('dropout_keep_probability', keep_prob)
  dropped = tf.nn.dropout(hidden1, keep_prob)

# Do not apply softmax activation yet, see below.
y = nn_layer(dropped, 500, 10, 'layer2', act=tf.identity)

with tf.name_scope('cross_entropy'):
  # The raw formulation of cross-entropy,
  #
  # tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.softmax(y)),
  #                               reduction_indices=[1]))
  #
  # can be numerically unstable.
  #
  # So here we use tf.losses.sparse_softmax_cross_entropy on the
  # raw logit outputs of the nn_layer above, and then average across
  # the batch.
  with tf.name_scope('total'):
    cross_entropy = tf.losses.sparse_softmax_cross_entropy(
        labels=y_, logits=y)
tf.summary.scalar('cross_entropy', cross_entropy)

with tf.name_scope('train'):
  train_step = tf.train.AdamOptimizer(FLAGS.learning_rate).minimize(
      cross_entropy)

with tf.name_scope('accuracy'):
  with tf.name_scope('correct_prediction'):
    correct_prediction = tf.equal(tf.argmax(y, 1), y_)
  with tf.name_scope('accuracy'):
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)

# Merge all the summaries and write them out to
# /tmp/tensorflow/mnist/logs/mnist_with_summaries (by default)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.log_dir + '/train', sess.graph)
test_writer = tf.summary.FileWriter(FLAGS.log_dir + '/test')
tf.global_variables_initializer().run()



import tensorflow as tf
import numpy as np

X_train = (np.random.sample((10000,5)))
y_train =  (np.random.sample((10000,1)))
X_train.shape

feature_columns = [
      tf.feature_column.numeric_column('x', shape=X_train.shape[1:])]
DNN_reg = tf.estimator.DNNRegressor(feature_columns=feature_columns,
# Indicate where to store the log file
     model_dir='train/linreg',
     hidden_units=[500, 300],
     optimizer=tf.train.AdamOptimizer(
          learning_rate=0.1,
          l1_regularization_strength=0.001
      )
)

# Train the estimator
train_input = tf.estimator.inputs.numpy_input_fn(
     x={"x": X_train},
     y=y_train, shuffle=False,num_epochs=None)
DNN_reg.train(train_input,steps=3000)


import tensorflow as tf

k = tf.float32

# Make a normal distribution, with a shifting mean
mean_moving_normal = tf.random_normal(shape=[1000], mean=(5*k), stddev=1)
# Record that distribution into a histogram summary
tf.summary.histogram("normal/moving_mean", mean_moving_normal)

# Setup a session and summary writer
sess = tf.Session()
writer = tf.summary.FileWriter("/tmp/histogram_example")

summaries = tf.summary.merge_all()

# Setup a loop and write the summaries to disk
N = 400
for step in range(N):
  k_val = step/float(N)
  summ = sess.run(summaries, feed_dict={k: k_val})
  writer.add_summary(summ, global_step=step)
