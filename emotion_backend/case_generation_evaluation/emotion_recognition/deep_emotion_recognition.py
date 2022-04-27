import os
# disable keras loggings
import sys
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import tensorflow as tf

from tensorflow.keras.layers import LSTM, GRU, Dense, Activation, LeakyReLU, Dropout

from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.keras.utils import to_categorical

from sklearn.metrics import accuracy_score, mean_absolute_error, confusion_matrix
from emotion_recognition.emotionRecognizer import EmotionRecognizer
from utils.utils import get_first_letters, AVAILABLE_EMOTIONS, extract_feature, get_dropout_str

import numpy as np
import pandas as pd
import random


class DeepEmotionRecognizer(EmotionRecognizer):
    """
    深度学习版本的 Emotion Recognizer.
    该类使用了 RNN (LSTM, GRU, etc.) 和 Dense layers.
    #TODO add CNNs
    """
    def __init__(self, **kwargs):
        """
        params:
            emotions (list): 需要进行分类的情绪列表, 默认 ["sad", "neutral", "happy"].
            tess_ravdess (bool): 是否使用 TESS & RAVDESS Speech 数据库, 默认 True.
            emodb (bool): 是否使用 EMO-DB Speech 数据库, default is True.
            custom_db (bool): 是否使用 custom Speech 数据库， 该数据库存储在 `data/train-custom` 和 `data/test-custom`中, 默认 True.
            tess_ravdess_name (str): TESS&RAVDESS 数据库 文件的输出文件名, 默认 "tess_ravdess.csv".
            emodb_name (str): EMO-DB 数据库 文件的输出文件名, 默认 "emodb.csv".
            custom_db_name (str): custom 数据库 文件的输出文件名, 默认 "custom.csv".
            features (list): 要使用的语音特征列表, 默认 ["mfcc", "chroma", "mel"]
            classification (bool): 是否使用分类或回归, 默认 True.
            balance (bool): 是否对数据库进行平衡 ( 包括 training 和 testing ), 默认 True.
            verbose (bool/int): 是否对认为进行输出
            ==========================================================
            模型参数
            n_rnn_layers (int): RNN 层数, 默认 2.
            cell (keras.layers.RNN instance): 用来训练模型的 RNN cell, 默认 LSTM.
            rnn_units (int): 'cell'的单位数, 默认 128.
            n_dense_layers (int): Dense 层数, 默认 2.
            dense_units (int): Dense layers 的单位数, 默认 128.
            dropout (list/float): dropout rate,
                - 如果是 list, 它表示每一层的 dropout rate.
                - 如果是 float, 它表示所有层的 dropout rate.
                Default is 0.3.
            ==========================================================
            训练参数
            batch_size (int): 每个梯度更新的样本数量, 默认 64.
            epochs (int): 训练的 epochs 数目 , 默认 1000.
            optimizer (str/keras.optimizers.Optimizer instance): 用来训练的优化器, 默认 "adam".
            loss (str/callback from keras.losses): 损失函数,
                分类的损失函数默认为 "categorical_crossentropy"
                回归的损失函数默认为 "mean_squared_error"
        """
        # 初始化 EmotionRecognizer
        super().__init__(**kwargs)

        self.n_rnn_layers = kwargs.get("n_rnn_layers", 2)
        self.n_dense_layers = kwargs.get("n_dense_layers", 2)
        self.rnn_units = kwargs.get("rnn_units", 128)
        self.dense_units = kwargs.get("dense_units", 128)
        self.cell = kwargs.get("cell", LSTM)

        # dropouts list
        self.dropout = kwargs.get("dropout", 0.3)
        self.dropout = self.dropout if isinstance(self.dropout, list) else [self.dropout] * ( self.n_rnn_layers + self.n_dense_layers )
        # number of classes ( emotions )
        self.output_dim = len(self.emotions)

        # 优化器属性
        self.optimizer = kwargs.get("optimizer", "adam")
        self.loss = kwargs.get("loss", "categorical_crossentropy")

        # 训练属性
        self.batch_size = kwargs.get("batch_size", 64)
        self.epochs = kwargs.get("epochs", 300)
        
        # 模型名称
        self.model_name = "AHNS-c-LSTM-layers-2-2-units-128-128-dropout-0.3_0.3_0.3_0.3.h5"
        self._update_model_name()

        # 初始化模型
        self.model = None

        # 计算输入长度
        self._compute_input_length()

        # boolean attributes
        self.model_created = False

    def _update_model_name(self):
        """
        Generates a unique model name based on parameters passed and put it on `self.model_name`.
        This is used when saving the model.
        """
        # get first letters of emotions, for instance:
        # ["sad", "neutral", "happy"] => 'HNS' (sorted alpshabetically)
        emotions_str = get_first_letters(self.emotions)
        # 'c' for classification & 'r' for regression
        problem_type = 'c' if self.classification else 'r'
        dropout_str = get_dropout_str(self.dropout, n_layers=self.n_dense_layers + self.n_rnn_layers)
        self.model_name = f"{emotions_str}-{problem_type}-{self.cell.__name__}-layers-{self.n_rnn_layers}-{self.n_dense_layers}-units-{self.rnn_units}-{self.dense_units}-dropout-{dropout_str}.h5"

    def _get_model_filename(self):
        """Returns the relative path of this model name"""
        return f"results/{self.model_name}"

    def _model_exists(self):
        """
        Checks if model already exists in disk, returns the filename,
        and returns `None` otherwise.
        """
        filename = self._get_model_filename()
        return filename if os.path.isfile(filename) else None

    def _compute_input_length(self):
        """
        Calculates the input shape to be able to construct the model.
        """
#         if not self.data_loaded:
#             self.load_data()
#         print("self.X_train[0].shape[1]:",self.X_train[0].shape[1])
        self.input_length = 180

    def _verify_emotions(self):
        super()._verify_emotions()
        self.int2emotions = {i: e for i, e in enumerate(self.emotions)}
        self.emotions2int = {v: k for k, v in self.int2emotions.items()}

    def create_model(self):
        """
        Constructs the neural network based on parameters passed.
        """
        if self.model_created:
            # model already created, why call twice
            print("[+] self.model_created is True")
            return

        print("[-] self.load_data()")
#         if not self.data_loaded:
#             # if data isn't loaded yet, load it
#             print("[+] self.load_data()")
#             self.load_data()
        
        model = Sequential()

        # rnn layers
        for i in range(self.n_rnn_layers):
            if i == 0:
                # first layer
                model.add(self.cell(self.rnn_units, return_sequences=True, input_shape=(None, self.input_length)))
                model.add(Dropout(self.dropout[i]))
            else:
                # middle layers
                model.add(self.cell(self.rnn_units, return_sequences=True))
                model.add(Dropout(self.dropout[i]))

        if self.n_rnn_layers == 0:
            i = 0

        # dense layers
        for j in range(self.n_dense_layers):
            # if n_rnn_layers = 0, only dense
            if self.n_rnn_layers == 0 and j == 0:
                model.add(Dense(self.dense_units, input_shape=(None, self.input_length)))
                model.add(Dropout(self.dropout[i+j]))
            else:
                model.add(Dense(self.dense_units))
                model.add(Dropout(self.dropout[i+j]))
                
        if self.classification:
            model.add(Dense(self.output_dim, activation="softmax"))
            model.compile(loss=self.loss, metrics=["accuracy"], optimizer=self.optimizer)
        else:
            model.add(Dense(1, activation="linear"))
            model.compile(loss="mean_squared_error", metrics=["mean_absolute_error"], optimizer=self.optimizer)
        
        self.model = model
        self.model_created = True
        if self.verbose > 0:
            print("[+] Model created")

    def load_data(self):
        """
        Loads and extracts features from the audio files for the db's specified.
        And then reshapes the data.
        """
        print("def load_data(self):")
        super().load_data()
        # reshape X's to 3 dims
        X_train_shape = self.X_train.shape
        X_test_shape = self.X_test.shape
        self.X_train = self.X_train.reshape((1, X_train_shape[0], X_train_shape[1]))
        self.X_test = self.X_test.reshape((1, X_test_shape[0], X_test_shape[1]))

        if self.classification:
            # one-hot encode when its classification
            self.y_train = to_categorical([ self.emotions2int[str(e)] for e in self.y_train ])
            self.y_test = to_categorical([ self.emotions2int[str(e)] for e in self.y_test ])
        
        # reshape labels
        y_train_shape = self.y_train.shape
        y_test_shape = self.y_test.shape
        if self.classification:
            self.y_train = self.y_train.reshape((1, y_train_shape[0], y_train_shape[1]))    
            self.y_test = self.y_test.reshape((1, y_test_shape[0], y_test_shape[1]))
        else:
            self.y_train = self.y_train.reshape((1, y_train_shape[0], 1))
            self.y_test = self.y_test.reshape((1, y_test_shape[0], 1))
    
    def train(self, override=False):
        """
        Trains the neural network.
        Params:
            override (bool): whether to override the previous identical model, can be used
                when you changed the dataset, default is False
        """
        # if model isn't created yet, create it
        if not self.model_created:
            self.create_model()

        # if the model already exists and trained, just load the weights and return
        # but if override is True, then just skip loading weights
        if not override:
            model_name = self._model_exists()
            if model_name:
                self.model.load_weights(model_name)
                self.model_trained = True
                if self.verbose > 0:
                    print("[*] Model weights loaded")
                return
        
        if not os.path.isdir("results"):
            os.mkdir("results")

        if not os.path.isdir("logs"):
            os.mkdir("logs")

        model_filename = self._get_model_filename()

        self.checkpointer = ModelCheckpoint(model_filename, save_best_only=True, verbose=1)
        self.tensorboard = TensorBoard(log_dir=os.path.join("logs", self.model_name))

#         self.history = self.model.fit(self.X_train, self.y_train,
#                         batch_size=self.batch_size,
#                         epochs=self.epochs,
#                         validation_data=(self.X_test, self.y_test),
#                         callbacks=[self.checkpointer, self.tensorboard],
#                         verbose=self.verbose)
        
        self.model_trained = True
        
        if self.verbose > 0:
            print("[+] Model trained")

    def predict(self, audio_path):
        feature = extract_feature(audio_path, **self.audio_config).reshape((1, 1, self.input_length))
        if self.classification:
            return self.int2emotions[self.model.predict_classes(feature)[0][0]]
        else:
            return self.model.predict(feature)[0][0][0]

    def predict_proba(self, audio_path):
        if self.classification:
            feature = extract_feature(audio_path, **self.audio_config).reshape((1, 1, self.input_length))
            proba = self.model.predict(feature)[0][0]
            result = {}
            for prob, emotion in zip(proba, self.emotions):
                result[emotion] = prob
            return result
        else:
            raise NotImplementedError("Probability prediction doesn't make sense for regression")



    def test_score(self):
        y_test = self.y_test[0]
        if self.classification:
            y_pred = self.model.predict_classes(self.X_test)[0]
            y_test = [np.argmax(y, out=None, axis=None) for y in y_test]
            return accuracy_score(y_true=y_test, y_pred=y_pred)
        else:
            y_pred = self.model.predict(self.X_test)[0]
            return mean_absolute_error(y_true=y_test, y_pred=y_pred)
        
    def train_score(self):
        y_train = self.y_train[0]
        if self.classification:
            y_pred = self.model.predict_classes(self.X_train)[0]
            y_train = [np.argmax(y, out=None, axis=None) for y in y_train]
            return accuracy_score(y_true=y_train, y_pred=y_pred)
        else:
            y_pred = self.model.predict(self.X_train)[0]
            return mean_absolute_error(y_true=y_train, y_pred=y_pred)

    def confusion_matrix(self, percentage=True, labeled=True):
        """Compute confusion matrix to evaluate the test accuracy of the classification"""
        if not self.classification:
            raise NotImplementedError("Confusion matrix works only when it is a classification problem")
        y_pred = self.model.predict_classes(self.X_test)[0]
        # invert from keras.utils.to_categorical
        y_test = np.array([ np.argmax(y, axis=None, out=None) for y in self.y_test[0] ])
        matrix = confusion_matrix(y_test, y_pred, labels=[self.emotions2int[e] for e in self.emotions]).astype(np.float32)
        if percentage:
            for i in range(len(matrix)):
                matrix[i] = matrix[i] / np.sum(matrix[i])
            # make it percentage
            matrix *= 100
        if labeled:
            matrix = pd.DataFrame(matrix, index=[ f"true_{e}" for e in self.emotions ],
                                    columns=[ f"predicted_{e}" for e in self.emotions ])
        return matrix

    def get_n_samples(self, emotion, partition):
        """Returns number data samples of the `emotion` class in a particular `partition`
        ('test' or 'train')
        """
        if partition == "test":
            if self.classification:
                y_test = np.array([ np.argmax(y, axis=None, out=None)+1 for y in np.squeeze(self.y_test) ]) 
            else:
                y_test = np.squeeze(self.y_test)
            return len([y for y in y_test if y == emotion])
        elif partition == "train":
            if self.classification:
                y_train = np.array([ np.argmax(y, axis=None, out=None)+1 for y in np.squeeze(self.y_train) ])
            else:
                y_train = np.squeeze(self.y_train)
            return len([y for y in y_train if y == emotion])

    def get_samples_by_class(self):
        """
        Returns a dataframe that contains the number of training 
        and testing samples for all emotions
        """
        train_samples = []
        test_samples = []
        total = []
        for emotion in self.emotions:
            n_train = self.get_n_samples(self.emotions2int[emotion]+1, "train")
            n_test = self.get_n_samples(self.emotions2int[emotion]+1, "test")
            train_samples.append(n_train)
            test_samples.append(n_test)
            total.append(n_train + n_test)
        
        # get total
        total.append(sum(train_samples) + sum(test_samples))
        train_samples.append(sum(train_samples))
        test_samples.append(sum(test_samples))
        return pd.DataFrame(data={"train": train_samples, "test": test_samples, "total": total}, index=self.emotions + ["total"])

    def get_random_emotion(self, emotion, partition="train"):
        """
        Returns random `emotion` data sample index on `partition`
        """
        if partition == "train":
            y_train = self.y_train[0]
            index = random.choice(list(range(len(y_train))))
            element = self.int2emotions[np.argmax(y_train[index])]
            while element != emotion:
                index = random.choice(list(range(len(y_train))))
                element = self.int2emotions[np.argmax(y_train[index])]
        elif partition == "test":
            y_test = self.y_test[0]
            index = random.choice(list(range(len(y_test))))
            element = self.int2emotions[np.argmax(y_test[index])]
            while element != emotion:
                index = random.choice(list(range(len(y_test))))
                element = self.int2emotions[np.argmax(y_test[index])]
        else:
            raise TypeError("Unknown partition, only 'train' or 'test' is accepted")

        return index

    def determine_best_model(self):
        # TODO
        # raise TypeError("This method isn't supported yet for deep nn")
        pass


if __name__ == "__main__":
    rec = DeepEmotionRecognizer(emotions=['angry', 'sad', 'neutral', 'ps', 'happy'],
                                epochs=300, verbose=0)
    rec.train(override=False)
    print("Test accuracy score:", rec.test_score() * 100, "%")