import contextlib
import wave
import os
from pronunciation_evaluation import get_pronunciation_score
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, BigInteger

Base = declarative_base()


class CaseEvaluation(Base):
    __tablename__ = 'case_evaluation'
    name = Column(String(24), primary_key=True)
    staff_id = Column(BigInteger, primary_key=True)
    customer_phone = Column(String(11))
    create_date = Column(Date)
    case_score = Column(Float)
    staff_emotion_score = Column(Float)
    staff_polite_words_percent = Column(Float)
    customer_emotion_score = Column(Float)
    customer_satisfied_score = Column(Integer)
    staff_understand_problem_score = Column(Integer)
    staff_solve_problem_score = Column(Integer)
    staff_pessimistic_num = Column(Integer)
    staff_optimistic_num = Column(Integer)
    customer_pessimistic_num = Column(Integer)
    customer_optimistic_num = Column(Integer)
    customer_satisfied = Column(String(255))
    staff_understand_problem = Column(String(255))
    staff_solve_problem = Column(String(255))
    time_in_seconds = Column(Float)
    speech_words_per_min = Column(Float)
    pronunciation_score = Column(Float)


def get_staff_audio_score(staff_audio_emotions):
    score = 80
    pessimistic_num = 0
    optimistic_num = 0
    for emotion in staff_audio_emotions:
        if emotion == 'angry':
            pessimistic_num += 1
            score -= 15
        elif emotion == 'sad':
            pessimistic_num += 1
            score -= 3
        elif emotion == 'happy':
            optimistic_num += 1
            score += 3
    return score, pessimistic_num, optimistic_num


def get_customer_audio_score(customer_audio_emotions):
    score = 80
    pessimistic_num = 0
    optimistic_num = 0
    for emotion in customer_audio_emotions:
        if emotion == 'angry':
            pessimistic_num += 1
            score -= 10
        elif emotion == 'sad':
            pessimistic_num += 1
            score -= 5
        elif emotion == 'happy':
            optimistic_num += 1
            score += 3
    return score, pessimistic_num, optimistic_num


def get_staff_text_score(staff_text_emotions):
    score = 80
    pessimistic_num = 0
    optimistic_num = 0
    for emotion in staff_text_emotions:
        emotion = emotion.split(' ')
        if emotion[0] == 'optimistic':
            optimistic_num += 1
            score += 3
        elif emotion[0] == 'pessimistic':
            pessimistic_num += 1
            score -= 5
            if len(emotion) > 1 and emotion[1] == 'angry':
                score -= 5
    return score, pessimistic_num, optimistic_num


def get_customer_text_score(customer_text_emotions):
    score = 80
    pessimistic_num = 0
    optimistic_num = 0
    for emotion in customer_text_emotions:
        emotion = emotion.split(' ')
        if emotion[0] == 'optimistic':
            optimistic_num += 1
            score += 3
            if len(emotion) > 1 and emotion[1] == 'thankful':
                score += 2
        elif emotion[0] == 'pessimistic':
            pessimistic_num += 1
            score -= 5
            if len(emotion) > 1 and emotion[1] == 'angry':
                score -= 5
    return score, pessimistic_num, optimistic_num


def get_staff_polite_words_percent(staff_sentences):
    if len(staff_sentences) == 0:
        return 0
    polite_words = ['您好', '你好', '欢迎', '致电',  # 问候
                    '先生', '小姐', '女士',  # 称呼
                    '请问', '为您', '帮您',  # 服务
                    '抱歉', '不好意思', '对不起',  # 道歉
                    '能否', '请您',  # 要求
                    '稍后', '稍候', '稍等',  # 等待
                    '再见', '谢谢', '感谢', '来电'  # 结束
                    ]
    times = 0
    for sentence in staff_sentences:
        for word in polite_words:
            if word in sentence:
                times += 1
                break
    return times / len(staff_sentences) * 100


def get_customer_satisfied_score(customer_sentences, customer_text_emotions):
    if len(customer_sentences) == 0:
        return 50

    satisfied_words = ['感谢', '谢谢', '多谢', '谢了', '再见', '拜拜', '没事']
    last_several_sentences_num = min(len(customer_sentences) // 5, 3)
    customer_pessimistic = False
    for i in range(len(customer_sentences) - last_several_sentences_num, len(customer_sentences)):
        for word in satisfied_words:
            if word in customer_sentences[i]:
                return 100
        if customer_text_emotions[i].startswith('pessimistic'):
            customer_pessimistic = True
    return 0 if customer_pessimistic else 50


def get_staff_understand_problem_score(character, sentences, fusioned_emotions):
    not_understand_words = ['什么意思', '不懂', '不能理解',
                            '说什么', '说的是', '再说一遍',
                            '意思吗', '是吗', '是不是', '这样吗',
                            ]
    not_understand_words_last_index = -1
    not_understand_words_num = 0
    for i in range(len(sentences)):
        if character[i] == '客服':
            for word in not_understand_words:
                if word in sentences[i]:
                    not_understand_words_last_index = i
                    not_understand_words_num += 1
    if not_understand_words_num == 0:
        return 100
    customer_pessimistic = False
    for i in range(0, not_understand_words_last_index + 1):
        if character[i] == '客户' and fusioned_emotions[i][0] == 'pessimistic':
            customer_pessimistic = True
            break
    # 多次表达不理解 且客户情绪不好
    if not_understand_words_num > 1 and customer_pessimistic:
        return 0
    # 多次表达不理解 且客户情绪没有不好
    elif not_understand_words_num > 1 and not customer_pessimistic:
        return 25
    # 表达不理解1次 且客户情绪不好
    elif not_understand_words_num == 1 and customer_pessimistic:
        return 50
    # 表达不理解1次 且客户情绪没有不好
    elif not_understand_words_num == 1 and not customer_pessimistic:
        return 75
    else:
        return 100


def get_staff_solve_problem_score(customer_sentences, customer_fusioned_emotions):
    if len(customer_sentences) == 0:
        return 50

    solved_words = ['可以', '行', '好好', '好的', '没问题', '先这样']
    not_solved_words = ['算了', '再说', '投诉', '怎么', '不能', '不行', '不可以', '不好', '不方便']
    last_several_sentences_num = min(len(customer_sentences) // 4, 5)
    solved_words_num = 0
    not_solved_words_num = 0
    for i in range(len(customer_sentences) - last_several_sentences_num, len(customer_sentences)):
        for word in solved_words:
            if word in customer_sentences[i]:
                solved_words_num += 1
        for word in not_solved_words:
            if word in customer_sentences[i]:
                not_solved_words_num += 1
    pessimistic_num = 0
    optimistic_num = 0
    for i in range(len(customer_fusioned_emotions) // 2, len(customer_fusioned_emotions)):
        if customer_fusioned_emotions[i][0] == 'optimistic':
            optimistic_num += 1
        elif customer_fusioned_emotions[i][0] == 'pessimistic':
            pessimistic_num += 1
    if solved_words_num > not_solved_words_num and optimistic_num > pessimistic_num:
        return 100
    elif solved_words_num > not_solved_words_num and optimistic_num <= pessimistic_num:
        return 75
    elif solved_words_num == not_solved_words_num:
        return 50
    elif solved_words_num < not_solved_words_num and optimistic_num > pessimistic_num:
        return 25
    else:
        return 0


def get_case_score(staff_emotion_score, staff_polite_words_percent, customer_emotion_score, customer_satisfied_score,
                   staff_understand_problem_score,
                   staff_solve_problem_score):
    # 一级权重 [0.27895456548641834, 0.6491180046313252, 0.07192742988225646]
    # 服务态度二级权重 [0.8571428571428571, 0.14285714285714285]
    # 客户满意二级权重 [0.8999999999999999, 0.09999999999999999]
    # 问题处理二级权重 [0.12499999999999999, 0.875]
    return (staff_emotion_score * 0.8571428571428571 + staff_polite_words_percent * 0.14285714285714285) \
           * 0.27895456548641834 \
           + (customer_emotion_score * 0.8999999999999999 + customer_satisfied_score * 0.09999999999999999) \
           * 0.6491180046313252 \
           + (staff_understand_problem_score * 0.12499999999999999 + staff_solve_problem_score * 0.875) \
           * 0.07192742988225646


def evaluate_case(character, sentences, audio_emotions, text_emotions, fusioned_emotions,
                  wav_path, chunks_path):
    staff_indexs = []
    staff_audio_emotions = []
    customer_audio_emotions = []
    staff_text_emotions = []
    customer_text_emotions = []
    staff_sentences = []
    customer_sentences = []
    customer_fusioned_emotions = []
    for i in range(len(character)):
        if character[i] == '客服':
            staff_indexs.append(i)
            staff_audio_emotions.append(audio_emotions[i])
            staff_text_emotions.append(text_emotions[i])
            staff_sentences.append(sentences[i])
        else:
            customer_audio_emotions.append(audio_emotions[i])
            customer_text_emotions.append(text_emotions[i])
            customer_sentences.append(sentences[i])
            customer_fusioned_emotions.append(fusioned_emotions[i])

    staff_audio_score, staff_audio_pessimistic_num, staff_audio_optimistic_num = get_staff_audio_score(
        staff_audio_emotions)
    staff_text_score, staff_text_pessimistic_num, staff_text_optimistic_num = get_staff_text_score(
        staff_text_emotions)
    staff_emotion_score = 0.7 * staff_audio_score + 0.3 * staff_text_score
    staff_pessimistic_num = staff_audio_pessimistic_num + staff_text_pessimistic_num
    staff_optimistic_num = staff_audio_optimistic_num + staff_text_optimistic_num

    staff_polite_words_percent = get_staff_polite_words_percent(staff_sentences)

    customer_audio_score, customer_audio_pessimistic_num, customer_audio_optimistic_num = get_customer_audio_score(
        customer_audio_emotions)
    customer_text_score, customer_text_pessimistic_num, customer_text_optimistic_num = get_customer_text_score(
        customer_text_emotions)
    customer_emotion_score = 0.7 * customer_audio_score + 0.3 * customer_text_score
    customer_pessimistic_num = customer_audio_pessimistic_num + customer_text_pessimistic_num
    customer_optimistic_num = customer_audio_optimistic_num + customer_text_optimistic_num

    customer_satisfied_score = get_customer_satisfied_score(customer_sentences, customer_text_emotions)

    staff_understand_problem_score = get_staff_understand_problem_score(character, sentences, fusioned_emotions)

    staff_solve_problem_score = get_staff_solve_problem_score(customer_sentences, customer_fusioned_emotions)

    case_score = get_case_score(staff_emotion_score, staff_polite_words_percent, customer_emotion_score,
                                customer_satisfied_score, staff_understand_problem_score, staff_solve_problem_score)

    evaluation_result = CaseEvaluation()
    evaluation_result.case_score = case_score
    evaluation_result.staff_emotion_score = staff_emotion_score
    evaluation_result.staff_polite_words_percent = staff_polite_words_percent
    evaluation_result.customer_emotion_score = customer_emotion_score
    evaluation_result.customer_satisfied_score = customer_satisfied_score
    evaluation_result.staff_understand_problem_score = staff_understand_problem_score
    evaluation_result.staff_solve_problem_score = staff_solve_problem_score
    evaluation_result.staff_pessimistic_num = staff_pessimistic_num
    evaluation_result.staff_optimistic_num = staff_optimistic_num
    evaluation_result.customer_pessimistic_num = customer_pessimistic_num
    evaluation_result.customer_optimistic_num = customer_optimistic_num
    if customer_satisfied_score == 100:
        evaluation_result.customer_satisfied = '客户表达了满意'
    elif customer_satisfied_score == 50:
        evaluation_result.customer_satisfied = '客户未明确表达是否满意'
    else:
        evaluation_result.customer_satisfied = '客户表达了不满'

    if staff_understand_problem_score == 100:
        evaluation_result.staff_understand_problem = '客服快速理解了问题'
    elif staff_understand_problem_score >= 50:
        evaluation_result.staff_understand_problem = '客服理解了问题'
    else:
        evaluation_result.staff_understand_problem = '客服没有很好地理解问题'

    if staff_solve_problem_score >= 75:
        evaluation_result.staff_solve_problem = '客户的问题得到了解决'
    elif staff_solve_problem_score == 50:
        evaluation_result.staff_solve_problem = '客户的问题解决情况不明确'
    else:
        evaluation_result.staff_solve_problem = '客户的问题未得到解决'

    with contextlib.closing(wave.open(wav_path, 'rb')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
        evaluation_result.time_in_seconds = wav_length

    if len(staff_indexs) == 0:
        evaluation_result.speech_words_per_min = 0
        evaluation_result.pronunciation_score = 100
    else:
        staff_words_num = sum([len(_) for _ in staff_sentences])
        staff_time = 0
        for i in staff_indexs:
            chunk_path = os.path.join(chunks_path, str(i) + '.wav')
            with contextlib.closing(wave.open(chunk_path, 'rb')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                chunk_length = frames / float(rate)
                staff_time += chunk_length
        evaluation_result.speech_words_per_min = 0 if staff_time == 0 else staff_words_num / staff_time * 60

        # 语音评测
        # 找到小于100字的最长客服句子
        cur_max_sentence_len = 0
        cur_max_sentence_index = -1
        for i in range(len(staff_sentences)):
            if 100 >= len(staff_sentences[i]) > cur_max_sentence_len:
                cur_max_sentence_index = staff_indexs[i]
                cur_max_sentence_len = len(staff_sentences[i])
        pronunciation_text = sentences[cur_max_sentence_index]
        pronunciation_chunk_path = os.path.join(chunks_path, str(cur_max_sentence_index) + '.wav')
        print('开始语音评测')
        pronunciation_score = get_pronunciation_score(pronunciation_text, pronunciation_chunk_path)
        evaluation_result.pronunciation_score = pronunciation_score

    return evaluation_result
