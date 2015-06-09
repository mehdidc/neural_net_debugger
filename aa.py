import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from lasagne.generative import autoencoder
from lasagne.easy import (BatchOptimizer, LightweightModel,
                          get_2d_square_image_view)
from lasagne.misc.plot_weights import grid_plot
from lasagne import layers, nonlinearities, updates, init
from sklearn.datasets import load_digits
from lasagne.datasets.mnist import MNIST
import theano
from sklearn.utils import shuffle

import theano

import matplotlib.pyplot as plt

from theano.tensor.shared_randomstreams import RandomStreams
from debugger.utils import (send_state, fig_to_html, state_insert_curve, 
                            state_insert_html,
                            state_meta_insert_curve, state_meta_insert_html)

import base64
import StringIO
import urllib

import theano.tensor as T

from collections import defaultdict
from sklearn.cross_validation import train_test_split

if __name__ == "__main__":
    np.random.seed(0)

    data = MNIST()
    data.load()
    X = data.X

    X_train, X_valid = train_test_split(X, test_size=0.25)


    meta_state = defaultdict(dict)

    meta_state = state_meta_insert_curve(meta_state, 
                                        "learning_curve", 
                                        "Learning curve", 
                                        "epoch", "loss", ["train", "valid"])
    meta_state = state_meta_insert_html(
            meta_state,
            "filters"
    )
    #send_state("default", meta_state) 

    #data = load_digits()
    #X = data['data']
    #y = data['target']

    #X = X.astype(theano.config.floatX)
    #X /= X.max()
    n = 60000 
    #n = X.shape[0]
    X = X[0:n]

    #X, y = shuffle(X, y)
    X = shuffle(X, random_state=0)
    z_dim = 20

    # X to Z (decoder)
    sz = int(np.sqrt(X.shape[1]))
    x_in = layers.InputLayer(shape=(None, X.shape[1]))

    
    # ConvnetModel
    #x_in_2d = layers.ReshapeLayer(x_in, ([0], 1, sz, sz))
    #h = layers.Conv2DLayer(x_in_2d, num_filters=20, filter_size=(3, 3))

    h = layers.DenseLayer(x_in, num_units=z_dim,
                          W=init.GlorotUniform(),
                          nonlinearity=nonlinearities.tanh)

    X_batch = T.matrix()
    h_get = theano.function([X_batch], h.get_output(X_batch))

    z_out = layers.DenseLayer(h, num_units=z_dim,
                              W=init.GlorotUniform(),
                              nonlinearity=nonlinearities.tanh)
    nnet_x_to_z = LightweightModel([x_in],
                                   [z_out])
    # Z to X (encoder)

    z_in = layers.InputLayer(shape=(None, z_dim))
    x_out = layers.DenseLayer(z_in, num_units=X.shape[1],
                              W=init.GlorotUniform(),
                              nonlinearity=nonlinearities.sigmoid)
    nnet_z_to_x = LightweightModel([z_in],
                                   [x_out])
    # instantiate the model
    class MyBatchOptimizer(BatchOptimizer):

        def iter_update(self, epoch, nb_batches, iter_update_batch):
            status = super(MyBatchOptimizer, self).iter_update(epoch, nb_batches, iter_update_batch)

            #e = X[0:20]
            #h_e = h_get(e)

            #conv_filters = h.W.get_value()
            #conv_filters = conv_filters.reshape( (conv_filters.shape[0], conv_filters.shape[2], conv_filters.shape[3]))
            #grid_plot(conv_filters, imshow_options={"cmap": "gray", "interpolation": None})
            #plt.show()

            status["loss_valid"] = self.model.get_loss(X_valid)

            if epoch % 10 == 0:
                plt.clf()
                filters = h.W.get_value().T
                filters = get_2d_square_image_view(filters[0:50])
                grid_plot(filters, imshow_options={"cmap":"gray"})
                plt.show()
                fig = plt.gcf()
                s = defaultdict(dict)
                s = state_insert_html(s, "filters", fig_to_html(fig))
                s = state_insert_curve(s, "learning_curve", "train", (status["epoch"], float(status["loss_train"])))
                s = state_insert_curve(s, "learning_curve", "valid", (status["epoch"], float(status["loss_valid"])))
                s.update(meta_state)
                send_state("default", s)
                #del status["filters"]
            return status

    batch_optimizer = MyBatchOptimizer(max_nb_epochs=300,
                                       optimization_procedure=(updates.rmsprop, {"learning_rate" : 0.5}),
                                       batch_size=256,
                                       verbose=1)
    rng = RandomStreams(seed=1000)

    from theano.sandbox import rng_mrg
    rng = rng_mrg.MRG_RandomStreams(seed=1000)
    #noise_function = lambda X_batch: X_batch * rng.binomial(size=X_batch.shape, p=0.7)
    noise_function = None
    model = autoencoder.Autoencoder(nnet_x_to_z, nnet_z_to_x, batch_optimizer, noise_function=noise_function, walkback=1)
    model.fit(X_train)

    """
    conv_filters = h.W.get_value()
    conv_filters = conv_filters.reshape( (conv_filters.shape[0], conv_filters.shape[2], conv_filters.shape[3]))
    grid_plot(conv_filters, imshow_options={"cmap": "gray"})
    plt.savefig('out-filters-conv.png')
    plt.show()
    """

    filters = h.W.get_value().T
    filters = get_2d_square_image_view(filters)
    grid_plot(filters, imshow_options={"cmap":"gray"})
    plt.savefig("out-filters.png")
    plt.show()

    plt.clf()
    samples = model.sample(nb=100, nb_iterations=10000)
    samples = get_2d_square_image_view(samples)
    grid_plot(samples, imshow_options={"cmap": "gray"})
    plt.savefig('out-samples.png')
    plt.show()
