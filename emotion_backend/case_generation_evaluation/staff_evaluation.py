# 一级权重 基本服务能力 情绪控制能力 服务规范 案例平均得分 成长
# [0.2837049613091205, 0.49240566670836916, 0.11563716481010498, 0.06335960040559833, 0.04489260676680697]
# 基本服务能力二级权重 有效服务次数 问题解决 时长
# [0.2532558975260414, 0.693927957211826, 0.05281614526213258]
# 情绪控制能力二级权重 自身情绪良好率 自身情绪平均得分 客户情绪良好率 客户情绪平均得分
# [0.053138897078367976, 0.20228671410146137, 0.12588969305266567, 0.618684695767505]
# 服务规范二级权重 礼貌用语使用情况 语速 发音
# [0.7306446713611295, 0.0809612319997507, 0.1883940966391198]
# 成长二级权重 相比上次 近期（3次以内）长期（所有）
# [0.6483290138222367, 0.22965079406263714, 0.12202019211512623]
import datetime
import os
from typing import List
from collections import defaultdict

from sqlalchemy.exc import SQLAlchemyError

from case_evaluation import CaseEvaluation
import numpy as np
from distfit import distfit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from datetime import date, datetime
from sklearn import linear_model

Base = declarative_base()


class StaffEvaluation(Base):
    __tablename__ = 'staff_evaluation'
    id = Column(BigInteger, primary_key=True)
    staff_id = Column(BigInteger)
    create_date = Column(Date)
    score = Column(Float)
    service_num = Column(Integer)
    service_num_score = Column(Float)
    problem_solve_score = Column(Float)
    problem_unsolved_percent = Column(Float)
    problem_solve = Column(String(255))
    average_time = Column(Float)
    time_score = Column(Float)
    average_time_description = Column(String(255))
    staff_emotion_score = Column(Float)
    staff_pessimistic_num = Column(Integer)
    staff_optimistic_num = Column(Integer)
    staff_pessimistic_percent = Column(Float)
    staff_optimistic_percent = Column(Float)
    staff_emotion_control_ability = Column(String(255))
    customer_emotion_score = Column(Float)
    customer_pessimistic_num = Column(Integer)
    customer_optimistic_num = Column(Integer)
    customer_pessimistic_percent = Column(Float)
    customer_optimistic_percent = Column(Float)
    customer_emotion_control_ability = Column(String(255))
    polite_words_score = Column(Float)
    polite_words_usage = Column(String(255))
    speech_speed_score = Column(Float)
    average_speech_speed = Column(Float)
    speech_speed = Column(String(255))
    average_pronunciation_score = Column(Float)
    average_case_score = Column(Float)
    growth_score = Column(Float)
    short_term_growth_trend = Column(String(255))
    long_term_growth_trend = Column(String(255))


class Staff(Base):
    __tablename__ = 'staff'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255))


def get_service_num_score(staff_cases: List[CaseEvaluation]):
    case_num = len(staff_cases)
    if case_num == 0:
        return 0, 0

    all_staffs_cases_dict = defaultdict(int)
    for _ in all_cases:
        all_staffs_cases_dict[staff_id] += 1
    all_staffs_case_nums = list(all_staffs_cases_dict.values())

    if len(all_staffs_case_nums) == 0:
        return 100, case_num
    max_staff_case_num = max(all_staffs_case_nums)
    min_staff_case_num = min(all_staffs_case_nums)
    return 100 if min_staff_case_num == max_staff_case_num \
               else (case_num - min_staff_case_num) / (max_staff_case_num - min_staff_case_num) * 100, case_num


def get_problem_solve_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, 100, '不足'
    problem_solved_percent = len([_ for _ in staff_cases if _.staff_solve_problem_score >= 75]) / len(staff_cases)
    problem_solved_average_score = sum([_.staff_solve_problem_score for _ in staff_cases]) / len(staff_cases)
    problem_understand_average_score = sum([_.staff_understand_problem_score for _ in staff_cases]) / len(staff_cases)
    problem_unsolved_percent = len([_ for _ in staff_cases if _.staff_solve_problem_score <= 25]) / len(staff_cases)
    problem_solve_score = 0.5 * problem_solved_percent \
                          + (0.125 * problem_understand_average_score
                             + 0.875 * problem_solved_average_score) * 0.5
    if problem_solve_score >= 75:
        problem_solve = '优秀'
    elif 50 <= problem_solve_score < 75:
        problem_solve = '普通'
    else:
        problem_solve = '不足'

    return problem_solve_score, problem_unsolved_percent, problem_solve


def get_time_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, 0, '偏短'
    # 客服时间的可能性(单边p值)的平均值 乘2 乘100
    staff_cases_times = [_.time_in_seconds for _ in staff_cases]
    average_time = sum(staff_cases_times) / len(staff_cases_times)
    time_score = np.mean(dist.predict(staff_cases_times)['y_proba']) * 2 * 100
    if time_score <= 0.3:
        if average_time >= dist.model['loc']:
            average_time_description = '偏长'
        else:
            average_time_description = '偏短'
    else:
        average_time_description = '正常'
    return float(time_score), average_time, average_time_description


def get_staff_emotion_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, 0, 0, 0, 0, '一般'
    pessimistic_num = len([_ for _ in staff_cases if _.staff_pessimistic_num > 0])
    pessimistic_percent = pessimistic_num / len(staff_cases) * 100
    optimistic_num = len([_ for _ in staff_cases if _.staff_optimistic_num > 0])
    optimistic_percent = optimistic_num / len(staff_cases) * 100
    average_emotion_score = sum([_.staff_emotion_score for _ in staff_cases]) / len(staff_cases)
    if average_emotion_score >= 80:
        emotion_control_ability = '优秀'
    elif 60 <= average_emotion_score < 80:
        emotion_control_ability = '普通'
    else:
        emotion_control_ability = '一般'
    return average_emotion_score, \
           pessimistic_percent, optimistic_percent, \
           pessimistic_num, optimistic_num, \
           emotion_control_ability


def get_customer_emotion_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, 0, 0, 0, 0, '一般'
    pessimistic_num = len([_ for _ in staff_cases if _.customer_pessimistic_num > 0])
    pessimistic_percent = pessimistic_num / len(staff_cases) * 100
    optimistic_num = len([_ for _ in staff_cases if _.customer_optimistic_num > 0])
    optimistic_percent = optimistic_num / len(staff_cases) * 100
    average_emotion_score = sum([_.customer_emotion_score for _ in staff_cases]) / len(staff_cases)
    if average_emotion_score >= 80:
        emotion_control_ability = '优秀'
    elif 60 <= average_emotion_score < 80:
        emotion_control_ability = '普通'
    else:
        emotion_control_ability = '一般'
    return average_emotion_score, \
           pessimistic_percent, optimistic_percent, \
           pessimistic_num, optimistic_num, \
           emotion_control_ability


def get_polite_words_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, '不足'
    polite_words_score = sum([_.staff_polite_words_percent for _ in staff_cases]) / len(staff_cases)
    if polite_words_score >= 70:
        polite_words_usage = '良好'
    else:
        polite_words_usage = '不足'
    return polite_words_score, polite_words_usage


def get_speech_speed_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0, 0, '偏慢'
    best_speed = 300
    min_speed = 180
    max_speed = 500
    speech_speed_scores = []
    for _ in staff_cases:
        speech_speed = _.speech_words_per_min
        if speech_speed > 300:
            speech_speed = min(float(max_speed), speech_speed)
            speech_speed_scores.append((max_speed - speech_speed) / (max_speed - best_speed) * 100)
        else:
            speech_speed = max(float(min_speed), speech_speed)
            speech_speed_scores.append((speech_speed - min_speed) / (best_speed - min_speed) * 100)
    speech_speed_score = sum(speech_speed_scores) / len(speech_speed_scores)
    average_speech_speed = sum([_.speech_words_per_min for _ in staff_cases]) / len(speech_speed_scores)
    if speech_speed_score >= 70:
        speech_speed = '正常'
    else:
        if average_speech_speed >= 300:
            speech_speed = '偏快'
        else:
            speech_speed = '偏慢'
    return speech_speed_score, average_speech_speed, speech_speed


def get_average_pronunciation_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0
    return sum([_.pronunciation_score for _ in staff_cases]) / len(staff_cases)


def get_average_case_score(staff_cases: List[CaseEvaluation]):
    if len(staff_cases) == 0:
        return 0
    return sum([_.case_score for _ in staff_cases]) / len(staff_cases)


def get_proxy_growth_score(staff_id):
    proxy_growth_score = 60
    past_staff_evaluations = session.query(StaffEvaluation).filter(StaffEvaluation.staff_id == int(staff_id)).all()
    past_staff_evaluations.sort(key=lambda staff_evaluation: staff_evaluation.id)
    if len(past_staff_evaluations) > 0:
        proxy_growth_score = past_staff_evaluations[-1].growth_score
    return proxy_growth_score, past_staff_evaluations


def get_growth_score(score, past_staff_evaluations: List[StaffEvaluation]):
    if len(past_staff_evaluations) == 0:
        diff = score
    else:
        diff = score - past_staff_evaluations[-1].score
    diff_score = (diff + 100) / 200 * 100  # diff的范围是[-100,100] 归一化后放缩到[0,100]

    long_term_scores = [_.score for _ in past_staff_evaluations]
    long_term_scores.append(score)

    long_term_days_deltas = []
    if len(past_staff_evaluations) > 0:
        for _ in past_staff_evaluations:
            long_term_days_deltas.append((_.create_date - past_staff_evaluations[0].create_date).days)
        long_term_days_deltas.append((datetime.now().date() - past_staff_evaluations[0].create_date).days)
    else:
        long_term_days_deltas.append(0)

    # 双指针查找是否有重复天 合并重复天
    i = 0
    while i < len(long_term_days_deltas) - 1:
        start = i
        end = i + 1
        while end < len(long_term_days_deltas):
            if long_term_days_deltas[end] == long_term_days_deltas[start]:
                end += 1
            else:
                break
        if end - start > 1:
            interval_average_score = sum(long_term_scores[start:end]) / (end - start)
            long_term_scores = long_term_scores[:start + 1] + long_term_scores[end:]
            long_term_scores[start] = interval_average_score
            long_term_days_deltas = long_term_days_deltas[:start + 1] + long_term_days_deltas[end:]
        i += 1

    # 如果只有一个点 不能做趋势线性回归
    if len(long_term_scores) == 1:
        long_term_growth_score = 100
        short_term_growth_score = 100
        short_term_growth_trend = '平稳'
        long_term_growth_trend = '平稳'
    else:
        if len(long_term_scores) > 3:
            short_term_scores = long_term_scores[-3:]
        else:
            short_term_scores = long_term_scores

        if len(long_term_days_deltas) > 3:
            short_term_days_deltas = [_ - long_term_days_deltas[-3] for _ in long_term_days_deltas[-3:]]
        else:
            short_term_days_deltas = long_term_days_deltas

        long_term_linear_model = linear_model.LinearRegression()
        long_term_linear_model.fit([[_] for _ in long_term_days_deltas], [[_] for _ in long_term_scores])
        long_term_linear_model_coef = long_term_linear_model.coef_[0][0]
        short_term_linear_model = linear_model.LinearRegression()
        short_term_linear_model.fit([[_] for _ in short_term_days_deltas], [[_] for _ in short_term_scores])
        short_term_linear_model_coef = short_term_linear_model.coef_[0][0]

        if short_term_linear_model_coef >= 0.1:
            short_term_growth_trend = '上升'
        elif -0.1 < short_term_linear_model_coef < 0.1:
            short_term_growth_trend = '平稳'
        else:
            short_term_growth_trend = '下降'

        if long_term_linear_model_coef >= 0.1:
            long_term_growth_trend = '上升'
        elif -0.1 < long_term_linear_model_coef < 0.1:
            long_term_growth_trend = '平稳'
        else:
            long_term_growth_trend = '下降'

        # 斜率<=-1为0分 >=1为100分
        if long_term_linear_model_coef >= 1:
            long_term_growth_score = 100
        elif long_term_linear_model_coef <= -1:
            long_term_growth_score = 0
        else:
            long_term_growth_score = (long_term_linear_model_coef + 1) / 2 * 100
        if short_term_linear_model_coef >= 1:
            short_term_growth_score = 100
        elif short_term_linear_model_coef <= -1:
            short_term_growth_score = 0
        else:
            short_term_growth_score = (short_term_linear_model_coef + 1) / 2 * 100

    return 0.6483290138222367 * diff_score \
           + 0.22965079406263714 * short_term_growth_score \
           + 0.12202019211512623 * long_term_growth_score, short_term_growth_trend, long_term_growth_trend


def evaluate_staff(staff_id):
    staff_cases = [_ for _ in all_cases if _.staff_id == int(staff_id)]
    service_num_score, service_num = get_service_num_score(staff_cases)
    problem_solve_score, problem_unsolved_percent, problem_solve = get_problem_solve_score(staff_cases)
    time_score, average_time, average_time_description = get_time_score(staff_cases)
    staff_emotion_score, \
    staff_pessimistic_percent, staff_optimistic_percent, \
    staff_pessimistic_num, staff_optimistic_num, \
    staff_emotion_control_ability = get_staff_emotion_score(staff_cases)
    customer_emotion_score, \
    customer_pessimistic_percent, customer_optimistic_percent, \
    customer_pessimistic_num, customer_optimistic_num, \
    customer_emotion_control_ability = get_customer_emotion_score(staff_cases)
    polite_words_score, polite_words_usage = get_polite_words_score(staff_cases)
    speech_speed_score, average_speech_speed, speech_speed = get_speech_speed_score(staff_cases)
    average_pronunciation_score = get_average_pronunciation_score(staff_cases)
    average_case_score = get_average_case_score(staff_cases)
    proxy_growth_score, past_staff_evaluations = get_proxy_growth_score(staff_id)
    without_growth_score = 0.2837049613091205 * (0.2532558975260414 * service_num_score
                                                 + 0.693927957211826 * problem_solve_score
                                                 + 0.05281614526213258 * time_score) \
                           + 0.49240566670836916 * (0.053138897078367976 * (100 - staff_pessimistic_percent)
                                                    + 0.20228671410146137 * staff_emotion_score
                                                    + 0.12588969305266567 * (100 - customer_pessimistic_percent)
                                                    + 0.618684695767505 * customer_emotion_score) \
                           + 0.11563716481010498 * (0.7306446713611295 * polite_words_score
                                                    + 0.0809612319997507 * speech_speed_score
                                                    + 0.1883940966391198 * average_pronunciation_score) \
                           + 0.06335960040559833 * average_case_score
    tmp_score = without_growth_score + 0.04489260676680697 * proxy_growth_score
    tmp_growth_score, short_term_growth_trend, long_term_growth_trend = get_growth_score(tmp_score,
                                                                                         past_staff_evaluations)
    tmp_score = without_growth_score + 0.04489260676680697 * tmp_growth_score
    growth_score, short_term_growth_trend, long_term_growth_trend = get_growth_score(tmp_score, past_staff_evaluations)
    score = without_growth_score + 0.04489260676680697 * growth_score

    evaluation_result = StaffEvaluation()
    evaluation_result.staff_id = staff_id
    evaluation_result.create_date = datetime.now().date()
    evaluation_result.score = float(score)
    evaluation_result.service_num = service_num
    evaluation_result.service_num_score = service_num_score
    evaluation_result.problem_solve_score = problem_solve_score
    evaluation_result.problem_unsolved_percent = problem_unsolved_percent
    evaluation_result.problem_solve = problem_solve
    evaluation_result.average_time = average_time
    evaluation_result.time_score = time_score
    evaluation_result.average_time_description = average_time_description
    evaluation_result.staff_emotion_score = staff_emotion_score
    evaluation_result.staff_pessimistic_num = staff_pessimistic_num
    evaluation_result.staff_optimistic_num = staff_optimistic_num
    evaluation_result.staff_pessimistic_percent = staff_pessimistic_percent
    evaluation_result.staff_optimistic_percent = staff_optimistic_percent
    evaluation_result.staff_emotion_control_ability = staff_emotion_control_ability
    evaluation_result.customer_emotion_score = customer_emotion_score
    evaluation_result.customer_pessimistic_num = customer_pessimistic_num
    evaluation_result.customer_optimistic_num = customer_optimistic_num
    evaluation_result.customer_pessimistic_percent = customer_pessimistic_percent
    evaluation_result.customer_optimistic_percent = customer_optimistic_percent
    evaluation_result.customer_emotion_control_ability = customer_emotion_control_ability
    evaluation_result.polite_words_score = polite_words_score
    evaluation_result.polite_words_usage = polite_words_usage
    evaluation_result.speech_speed_score = speech_speed_score
    evaluation_result.average_speech_speed = average_speech_speed
    evaluation_result.speech_speed = speech_speed
    evaluation_result.average_pronunciation_score = average_pronunciation_score
    evaluation_result.average_case_score = average_case_score
    evaluation_result.growth_score = float(growth_score)
    evaluation_result.short_term_growth_trend = short_term_growth_trend
    evaluation_result.long_term_growth_trend = long_term_growth_trend

    return evaluation_result


if __name__ == '__main__':
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/emotion')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()

    all_cases = session.query(CaseEvaluation).all()

    # 拟合通话时间分布
    all_cases_time = [_.time_in_seconds for _ in all_cases]
    dist = distfit()
    dist.fit_transform(np.array(all_cases_time))

    csv_root_path = os.path.join('DONE', 'speaker_role_text_emotion_csvs')

    # staff_ids = []
    # for _ in os.listdir(csv_root_path):
    #     if os.path.isdir(os.path.join(csv_root_path, _)) and not _[0] == '.':
    #         staff_ids.append(_)
    staff_ids = set([_.id for _ in session.query(Staff).all()])
    for staff_id in staff_ids:
        evaluation_result = evaluate_staff(staff_id)
        try:
            session.add(evaluation_result)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(e)

    session.close()
