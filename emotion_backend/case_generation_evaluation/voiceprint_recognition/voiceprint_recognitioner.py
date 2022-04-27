import argparse
import functools
import numpy as np
import tensorflow as tf
import librosa
import distutils.util

# 添加参数
def add_arguments(argname, type, default, help, argparser, **kwargs):
    type = distutils.util.strtobool if type == bool else type
    argparser.add_argument("--" + argname,
                           default=default,
                           type=type,
                           help=help + ' 默认: %(default)s.',
                           **kwargs)


# 加载并预处理音频
def load_audio(audio_path, mode='train', win_length=400, sr=16000, hop_length=160, n_fft=512, spec_len=257):
    # 读取音频数据
    wav, sr_ret = librosa.load(audio_path, sr=sr)
    # 数据拼接
    if mode == 'train':
        extended_wav = np.append(wav, wav)
        if np.random.random() < 0.3:
            extended_wav = extended_wav[::-1]
    else:
        extended_wav = np.append(wav, wav[::-1])
    # 计算短时傅里叶变换
    linear = librosa.stft(extended_wav, n_fft=n_fft, win_length=win_length, hop_length=hop_length)
    mag, _ = librosa.magphase(linear)
    freq, freq_time = mag.shape
    # assert freq_time >= spec_len, "非静音部分长度不能低于1.3s"
    if mode == 'train':
        # 随机裁剪
        rand_time = np.random.randint(0, freq_time - spec_len)
        spec_mag = mag[:, rand_time:rand_time + spec_len]
    else:
        spec_mag = mag[:, :spec_len]
    mean = np.mean(spec_mag, 0, keepdims=True)
    std = np.std(spec_mag, 0, keepdims=True)
    spec_mag = (spec_mag - mean) / (std + 1e-5)
    spec_mag = spec_mag[:, :, np.newaxis]
    return spec_mag


# 利用模型预测音频
def infer(audio_path):
    data = load_audio(audio_path, mode='test', spec_len=input_shape[1])
    data = data[np.newaxis, :]
    feature = model.predict(data)
    return feature


# 预测，获得余弦结果
def predict(audio_path1,audio_path2):
    # 要预测的两个人的音频文件
    feature1 = infer(audio_path1)[0]
    feature2 = infer(audio_path2)[0]
    # 对角余弦值
    dist = np.dot(feature1, feature2) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))
    return dist


parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('input_shape',      str,    '(257, 257, 1)',          '数据输入的形状')
add_arg('threshold',        float,   0.7,                     '判断是否为同一个人的阈值')
add_arg('model_path',       str,    'models/infer_model.h5',  '预测模型的路径')
args = parser.parse_args()


# 加载模型
model = tf.keras.models.load_model(args.model_path)
model = tf.keras.models.Model(inputs=model.input, outputs=model.get_layer('batch_normalization').output)

# 数据输入的形状
input_shape = eval(args.input_shape)

# 打印模型
model.build(input_shape=input_shape)
model.summary()
