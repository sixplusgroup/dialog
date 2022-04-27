import csv
import json
import os
import shutil
from datetime import datetime, date

from pydub import AudioSegment
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from case_evaluation import evaluate_case
from emotion_recognition.deep_emotion_recognition import DeepEmotionRecognizer
from voiceprint_recognition.voiceprint_recognitioner import predict
from text_emotion_recognition import get_text_emotion
from transcription import RequestApi
from utils.fusion_emotion import gen_fusion_emotion
from utils.loudness import recvoice
from build_recommendation_library import build_recommendation_library
from do_recommend import do_recommend

# 讯飞api的密钥
appid = "e7d58cd0"
secret_key = "ad667b0a35ef9c35afbb112e8e7b6cfa"

customer = "客户"
staff = "客服"

# 加载“情绪识别”模型
# inherited from emotion_recognition.EmotionRecognizer
# default parameters (LSTM: 128x2, Dense:128x2)
deeprec = DeepEmotionRecognizer(emotions=['angry', 'sad', 'neutral', 'happy'], n_rnn_layers=2, n_dense_layers=2,
                                rnn_units=128, dense_units=128)
# train the model
deeprec.train()


# 降噪
# rate, data = wavfile.read(filename)
# reduced_noise = nr.reduce_noise(y=data, sr=rate)
# wavfile.write("133016226210226170142261.wav", rate, reduced_noise)

def rm_and_mk_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def is_machine_words(sentence):
    for word in ('欢迎致电', '转接', '星号', '服务质量', '录音', '坐席', '座席', '所有做皮', '所有坐', '所有座', '当前坐', '当前座'):
        if word in sentence:
            return True
    return False


def determine_which_is_staff(character, sentences, speaker):
    # 确定哪个是客服
    speaker2_num = 0
    speaker3_num = 0
    speaker2_staff_num = 0
    speaker3_staff_num = 0
    for i in range(len(sentences)):
        if sentences[i] == '2':
            speaker2_num += 1
            if character[i] == staff:
                speaker2_staff_num += 1
        else:
            speaker3_num += 1
            if character[i] == staff:
                speaker3_staff_num += 1
    speaker2_staff_ratio = speaker2_staff_num / speaker2_num if speaker2_num > 0 else 0
    speaker3_staff_ratio = speaker3_staff_num / speaker3_num if speaker3_num > 0 else 0
    # 如果没识别出来
    if speaker2_staff_ratio + speaker3_staff_ratio <= 0.001:
        staff_speaker = '0'
    # 如果有一方的数量极少，误识别会造成比率极高
    elif speaker2_num < 3 and speaker3_num > speaker2_num and speaker3_staff_num > speaker2_staff_num:
        staff_speaker = '3'
    elif speaker3_num < 3 and speaker2_num > speaker3_num and speaker2_staff_num > speaker3_staff_num:
        staff_speaker = '2'
    # 看比率
    elif speaker2_staff_ratio == speaker3_staff_ratio:
        staff_speaker = '2' if speaker2_num >= speaker3_num else '3'
    else:
        staff_speaker = '2' if speaker2_staff_ratio > speaker3_staff_ratio else '3'
    # 修正
    for i in range(len(sentences)):
        if speaker[i] == staff_speaker:
            character[i] = staff
        else:
            character[i] = customer


def process(wav_path, chunks_path, staff_audio_path):
    rm_and_mk_dir(chunks_path)

    sentences = []  # 对话转写
    speaker = []  # api识别出的说话者
    character = []  # 对话对应角色
    audio_emotions = []  # 对话对应情绪
    text_emotions = []  # 文本情绪
    index = 0

    # 语音转写
    print('开始转写')
    api = RequestApi(appid=appid, secret_key=secret_key, upload_file_path=wav_path)
    data = json.loads(api.all_api_request()["data"])
    print('转写成功')
    print(data)

    # 切割，导出，并进行情绪识别
    wav = AudioSegment.from_wav(wav_path)
    for dialogue in data:
        if dialogue['speaker'] == '1':  # 去掉speaker1机器音=
            continue

        speaker.append(dialogue['speaker'])

        sentences.append(dialogue['onebest'])

        # 切割
        print('开始切割')
        begin_time = int(dialogue['bg'])
        end_time = int(dialogue['ed'])
        print('切割成功 {} {}'.format(begin_time, end_time))

        # 导出
        print('开始导出')
        wav[begin_time:end_time].export(os.path.join(chunks_path, str(index) + ".wav"), format="wav")
        print('导出成功')

        # 情绪识别
        print('开始语音情绪识别')
        audio_emotion = deeprec.predict(os.path.join(chunks_path, str(index) + ".wav"))
        print('语音情绪识别成功 {}'.format(audio_emotion))
        print('开始文本情绪识别')
        print(dialogue['onebest'])
        text_emotion = get_text_emotion(dialogue['onebest'])
        print('文本情绪识别成功 {}'.format(text_emotion))
        audio_emotions.append(audio_emotion)
        text_emotions.append(text_emotion)

        # 声纹识别
        print('开始声纹识别')
        result = predict(staff_audio_path, os.path.join(chunks_path, str(index) + ".wav"))
        print('声纹识别完毕')
        if result < 0.7:  # 推荐相似的阈值为0.7，可调
            character.append(customer)
        else:
            character.append(staff)

        index += 1

    determine_which_is_staff(character, sentences, speaker)

    return speaker, character, sentences, audio_emotions, text_emotions, index


if __name__ == '__main__':
    todo_root_path = 'TODO'
    done_root_path = 'DONE'
    todo_wav_root_path = os.path.join(todo_root_path, 'wav_new')
    todo_chunks_root_path = os.path.join(todo_root_path, 'chunks')
    todo_csv_root_path = os.path.join(todo_root_path, 'speaker_role_text_emotion_csvs')
    todo_loudness_root_path = os.path.join(todo_root_path, 'loudness')
    todo_recommendation_root_path = os.path.join(todo_root_path, 'recommendation')
    done_wav_root_path = os.path.join(done_root_path, 'wav')
    done_chunks_root_path = os.path.join(done_root_path, 'chunks')
    done_csv_root_path = os.path.join(done_root_path, 'speaker_role_text_emotion_csvs')
    done_loudness_root_path = os.path.join(done_root_path, 'loudness')
    done_recommendation_root_path = os.path.join(done_root_path, 'recommendation')

    staff_audio_root_path = "staff_voice_library"  # 客服的声纹音频

    rm_and_mk_dir(todo_chunks_root_path)
    rm_and_mk_dir(todo_csv_root_path)
    rm_and_mk_dir(todo_loudness_root_path)
    rm_and_mk_dir(todo_recommendation_root_path)

    staff_ids = []
    for _ in os.listdir(todo_wav_root_path):
        if os.path.isdir(os.path.join(todo_wav_root_path, _)) and not _[0] == '.':
            staff_ids.append(_)

    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/emotion')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()

    for staff_id in staff_ids:
        # 声纹文件
        staff_audio_path = os.path.join(staff_audio_root_path, '{}.wav'.format(staff_id))

        # 创建生成的主csv所在的目录 不然写文件失败
        todo_csv_staff_dir_path = os.path.join(todo_csv_root_path, staff_id)
        if not os.path.exists(todo_csv_staff_dir_path):
            os.makedirs(todo_csv_staff_dir_path)
        # 创建生成的响度csv所在的目录 不然写文件失败
        todo_loudness_staff_dir_path = os.path.join(todo_loudness_root_path, staff_id)
        if not os.path.exists(todo_loudness_staff_dir_path):
            os.makedirs(todo_loudness_staff_dir_path)
        # 创建生成的推荐json所在的目录
        todo_recommendation_staff_dir_path = os.path.join(todo_recommendation_root_path, staff_id)
        if not os.path.exists(todo_recommendation_staff_dir_path):
            os.makedirs(todo_recommendation_staff_dir_path)

        # todo处理完成后需要移动到done
        done_csv_staff_dir_path = os.path.join(done_csv_root_path, staff_id)
        done_chunks_staff_dir_path = os.path.join(done_chunks_root_path, staff_id)
        done_wav_staff_dir_path = os.path.join(done_wav_root_path, staff_id)
        done_loudness_staff_dir_path = os.path.join(done_loudness_root_path, staff_id)
        done_recommendation_staff_dir_path = os.path.join(done_recommendation_root_path, staff_id)
        # 如果之前没有这个客服的通话记录 需要在done中创建该客服的目录
        if not os.path.exists(done_csv_staff_dir_path):
            os.makedirs(done_csv_staff_dir_path)
        if not os.path.exists(done_chunks_staff_dir_path):
            os.makedirs(done_chunks_staff_dir_path)
        if not os.path.exists(done_wav_staff_dir_path):
            os.makedirs(done_wav_staff_dir_path)
        if not os.path.exists(done_loudness_staff_dir_path):
            os.makedirs(done_loudness_staff_dir_path)
        if not os.path.exists(done_recommendation_staff_dir_path):
            os.makedirs(done_recommendation_staff_dir_path)

        wav_filenames = list(filter(lambda name: name[0] != '.' and name.endswith('.wav'),
                                    os.listdir(os.path.join(todo_wav_root_path, staff_id))))
        months = set()
        for wav_filename in wav_filenames:
            months.add(int(wav_filename[11:13]))
        cross_year = False
        if (12 in months or 11 in months or 10 in months) and (1 in months or 2 in months or 3 in months):
            cross_year = True

        for wav_filename in wav_filenames:
            filename_without_extension = wav_filename.split('.')[0]
            wav_path = os.path.join(todo_wav_root_path, staff_id, wav_filename)
            chunks_path = os.path.join(todo_chunks_root_path, staff_id, filename_without_extension)
            print('开始处理音频{}'.format(wav_path))
            speaker, character, sentences, audio_emotions, text_emotions, index = process(wav_path, chunks_path,
                                                                                          staff_audio_path)
            print('处理音频完成')

            # 第二遍过滤全机器音
            machine_sentence_num = 0
            for s in sentences:
                if is_machine_words(s):
                    machine_sentence_num += 1
            if index - machine_sentence_num <= 2:
                continue

            # 情绪融合 魏凯旋做的 推荐部分用到
            fusioned_emotions = gen_fusion_emotion(character, audio_emotions, text_emotions, index)

            # 输出主csv
            rows = []
            for i in range(index):
                rows.append((i, speaker[i], character[i], sentences[i], audio_emotions[i], text_emotions[i],
                             fusioned_emotions[i][0], fusioned_emotions[i][1]))
            csv_path = os.path.join(todo_csv_staff_dir_path, filename_without_extension + '.csv')
            print('开始输出主csv {}'.format(csv_path))
            with open(csv_path, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(rows)
            print('输出主csv成功')

            # 输出响度csv
            loudness_path = os.path.join(todo_loudness_staff_dir_path, filename_without_extension + '.csv')
            print('开始输出响度csv')
            recvoice(wav_path, loudness_path)
            print('输出响度csv成功')

            # 案例评价 插入数据库
            evaluation_result = evaluate_case(character, sentences, audio_emotions, text_emotions, fusioned_emotions,
                                              wav_path,
                                              chunks_path)
            evaluation_result.name = filename_without_extension
            evaluation_result.staff_id = staff_id
            evaluation_result.customer_phone = filename_without_extension[0:11]
            year = datetime.now().year
            month = int(filename_without_extension[11:13])
            if cross_year and 10 <= month <= 12:
                year -= 1
            evaluation_result.create_date = date(year, month, int(filename_without_extension[13:15]))
            try:
                session.add(evaluation_result)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                print(e)

            # 生成改案例的推荐点
            print('生成{} {}的推荐点'.format(staff_id, filename_without_extension))
            build_recommendation_library()
            print('推荐点生成完毕')
            # 对这些案例进行推荐
            print('对{} {}进行推荐'.format(staff_id, filename_without_extension))
            do_recommend(csv_path)
            print('推荐完毕')

            # 移动到done
            # 防止移动时冲突
            target_csv_path = os.path.join(done_csv_staff_dir_path, filename_without_extension + '.csv')
            if os.path.exists(target_csv_path):
                os.remove(target_csv_path)
            target_chunks_path = os.path.join(done_chunks_staff_dir_path, filename_without_extension)
            if os.path.exists(target_chunks_path):
                shutil.rmtree(target_chunks_path)
            target_loudness_path = os.path.join(done_loudness_staff_dir_path, filename_without_extension + '.csv')
            if os.path.exists(target_loudness_path):
                os.remove(target_loudness_path)
            target_wav_path = os.path.join(done_wav_staff_dir_path, wav_filename)
            if os.path.exists(target_wav_path):
                os.remove(target_wav_path)
            target_recommendation_path = os.path.join(done_recommendation_staff_dir_path,
                                                      filename_without_extension + '.json')
            if os.path.exists(target_recommendation_path):
                os.remove(target_recommendation_path)

            # 移动
            shutil.move(csv_path, done_csv_staff_dir_path)
            shutil.move(chunks_path, done_chunks_staff_dir_path)
            shutil.move(wav_path, done_wav_staff_dir_path)
            shutil.move(loudness_path, done_loudness_staff_dir_path)
            shutil.move(target_recommendation_path.replace('DONE', 'TODO', 1), done_recommendation_staff_dir_path)

    # 关闭session:
    session.close()
    # 清空todo目录
    rm_and_mk_dir(todo_root_path)
