import wave
import numpy
import pandas as pd


# 求数组平均值
def mean(a):
    return numpy.longlong(sum(a)) / len(a)


# 绝对值函数
def abslist(a):
    return list(map(abs, a))


def recvoice(wav_path, csv_path):
    # 打开WAV文档，文件路径根据需要做修改
    wf = wave.open(wav_path, "rb")

    nframes = wf.getnframes()
    framerate = wf.getframerate()
    # 读取完整的帧数据到str_data中，这是一个string类型的数据
    str_data = wf.readframes(nframes)
    wf.close()
    # 将波形数据转换为数组
    wave_data = numpy.frombuffer(str_data, dtype=numpy.short)
    # wave_data=list(map(abs,wave_data))
    M = []
    seconds = 1
    # 求seconds秒取样的平均值，若为双声道，再多乘2
    n = framerate * seconds
    for i in range(0, len(wave_data), n):
        M.append(wave_data[i:i + n] / 10)  # 传化成分贝
    M = map(abslist, M)
    sound = list(map(mean, M))
    # 时间数组，与sound配对形成系列点坐标
    time = numpy.arange(0, nframes / (seconds * framerate))
    time = time.astype(int) * seconds

    # 生成csv文件
    dataframe = pd.DataFrame({'Time(s)': time, 'Sound': sound})
    dataframe.to_csv(csv_path, index=False, sep=',')
