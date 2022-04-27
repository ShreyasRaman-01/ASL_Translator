import tensorflow as tf
from tensorflow.keras import datasets, layers, models, callbacks
import os

import sys
sys.path.append('../scripts')
import config

class MetricsPrintingCallback(callbacks.Callback):
    def on_train_batch_end(self, batch, logs=None):
        print("Batch {}: loss {:7.2f} | accuracy {:7.2f}".format(batch, logs["loss"], logs["accuracy"]))

    def on_test_batch_end(self, batch, logs=None):
        print("Batch {}: loss {:7.2f} | accuracy {:7.2f}".format(batch, logs["loss"], logs["accuracy"]))

    def on_epoch_end(self, epoch, logs=None):
        print("Epoch {}: loss {:7.2f} | accuracy {:7.2f} | recall {:7.2f} | precision {:7.2f}".format(epoch, logs["loss"], logs["accuracy"], logs["recall"], logs["precision"]))


class CNN_Model:

    def __init__(self):

        #creating sequential CNN and detection model
        self.model = models.Sequential()

        #configs for model structure
        self.INPUT_SHAPE = (200, 300)

        self.CONV_BLOCKS = 3
        self.BLOCK_FILTERS = [32, 64, 128]
        self.BLOCK_SIZES = [8,5,3]
        self.PADDING = ['same','valid','valid']
        self.CONV_REGULARIZATION = [None, None, None]
        self.CONV_ACTIVATION = ['relu','relu','relu']

        self.DENSE_LAYERS = 2
        self.DENSE_SIZES = [256, 128]
        self.DENSE_REGULARIZATION = [None, None]
        self.DENSE_ACTIVATION = ['relu','relu']
        self.OUTPUT_SIZE = config.NUM_CLASSES


        #loss functions for models
        self.OPTIMIZER = 'adam'
        self.LOSS = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.METRICS = ['accuracy', 'precision', 'recall']


        #other hyper-parameters
        self.EPOCHS = 50
        self.BATCH_SIZE = 30
        self.LR = 1e-4



        #path to save weights
        checkpoint_path = os.path.relpath('./cnn/saved_models')

        num_weights = len(os.listdir(self.checkpoint_path)) + 1
        checkpoint_path = os.path.join(checkpoint_path, 'experiment{}_{epoch}.h5'.format(num_weights) )

        log_dir = os.path.join('./cnn/logs/experiment{}'.format(num_weights))

        self.tensorboard_callback = callbacks.TensorBoard(log_dir = log_dir, histogram_freq = 1)

        self.lr_scheduler_callback = callbacks.LearningRateScheduler(self.lr_scheduler, verbose=0)

        self.cp_callback = callbacks.ModelCheckpoint(filepath=checkpoint_path, monitor='val_loss', verbose=1, save_best_only=True, mode = 'min', save_weights_only=False, save_freq = 'epoch', period = 5)

    def lr_scheduler(epoch, lr):
        if epoch < 20:
            return lr
        elif epoch < 40:
            return lr * tf.math.exp(-0.1)
        else:
            return lr*tf.math.exp(-0.5)

    def build_model(self):

        print('Building Sequential Model...')

        assert (len(self.BLOCK_SIZES)==self.CONV_BLOCKS), "Error: BLOCK_SIZES don't match CONV_BLOCKS"
        assert (len(self.BLOCK_FILTERS)==self.CONV_BLOCKS), "Error: BLOCK_FILTERS don't match CONV_BLOCKS"
        assert (len(self.CONV_REGULARIZATION)==self.CONV_BLOCKS), "Error: CONV_REGULARIZATION don't match CONV_BLOCKS"
        assert (len(self.PADDING) == self.CONV_BLOCKS), "Error: PADDING don't match CONV_BLOCKS"
        assert (len(self.CONV_ACTIVATION) == self.CONV_BLOCKS), "Error: PADDING don't match CONV_BLOCKS"

        assert (len(self.DENSE_SIZES)==self.DENSE_LAYERS), "Error: DENSE_SIZES don't match DENSE_LAYERS"
        assert (len(self.DENSE_REGULARIZATION)==self.DENSE_LAYERS), "Error: DENSE_REGULARIZATION don't match DENSE_LAYERS"
        assert (len(self.DENSE_ACTIVATION)== self.DENSE_LAYERS), "Error: DENSE_ACTIVATION don't match DENSE_LAYERS"

        #first input layer
        self.model.add(layers.InputLayer(shape = self.INPUT_SHAPE, name = 'input'))

        #convolution blocks
        for i in range(1, self.CONV_BLOCKS + 1):

            filters = self.BLOCK_FILTERS[i-1]
            size = (self.BLOCK_SIZES[i-1], self.BLOCK_FILTERS[i-1])

            padding = self.PADDING[i-1]; regularization = self.CONV_REGULARIZATION[i-1]; activation = self.CONV_ACTIVATION[i-1]

            self.model.add( layers.Conv2D(filters, size, padding = padding, activation = activation, kernel_regularizer = regularization, name = 'conv_{}'.format(i)) )


        #dense layers
        for i in range(1, self.DENSE_LAYERS + 1):

            size = self.DENSE_SIZES[i-1]; regularization = self.DENSE_REGULARIZATION[i-1]; activation = self.DENSE_ACTIVATION[i-1]

            self.model.add(layers.Dense(units = size, activation = activation, kernel_regularizer = regularization, name = 'dense_{}'.format(i)))


        #output final layers
        self.model.add(layers.Dense(units = self.OUTPUT_SIZE, activation = 'sigmoid', name = 'output'))


        self.model.summary()

    def compile(self):

        print('Compiling Model...')

        self.model.compile(optimizer = self.OPTIMIZER, loss = self.LOSS, metrics = self.METRICS)


    def train(self, train_images, train_labels, test_images, test_labels):

        print('Training Model....')

        self.model.fit(train_images, train_labels, epochs = self.EPOCHS, batch_size = self.BATCH_SIZE, callbacks=[self.cp_callback, self.tensorboard_callback, self.lr_scheduler], validation_data = (test_images, test_labels))


    def evaluate(self, test_images, test_labels, checkpoint_dir):


        print('Loading checkpoint file...')
        model_eval = keras.models.load_model(checkpoint_dir)

        print('Evaluating Model...')
        test_loss, test_acc, test_precision, test_recall = model_eval.evaluate(test_images, test_labels, verbose = 2)

        print('Test Loss: {} | Test Acc. : {} | Test Precision: {} | Test Recall: {}'.format(test_loss, test_acc, test_precision, test_recall))
