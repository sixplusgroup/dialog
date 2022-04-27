# -*- coding: UTF-8
import json
import os
import time

import gensim
import jieba
import numpy as np
from scipy.linalg import norm
import random
import csv

import re
from zhon.hanzi import punctuation

start = time.time()
model_file = 'word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
end = time.time()
print("加载模型花费时间")
print(end - start)

customer_start_bad_emotion = []
customer_end_bad_emotion = []
service_start_bad_emotion = []
service_end_bad_emotion = []
customer_bad_emotion = []
customerService_bad_emotion = []

to_recommend_root_path = 'TODO/recommendation'


class Sentence:
    isCustomerService = False
    line = ""
    emotion = ""  # pessimistic  neutral   optimistic

    def __init__(self, isCustomerService, line, emotion):
        self.isCustomerService = isCustomerService
        self.line = line
        self.emotion = emotion

    def __str__(self):  # 定义打印对象时打印的字符串

        return " ".join(str(item) for item in (
            self.isCustomerService, self.line, self.emotion))


# 自定义 class ：音频情绪，文本情绪，客服or客户 ，line内容
# 根据前三个内容进行 匹配句过滤 音频（|文本）情绪好or坏， 指定客服or客户
# 然后进行所需要的 相似度语句匹配 并筛选

# 识别：每个模板进行遍历标记 如下模板 ：：
# -------------------------------------------------------------------------

# 均为客户情绪处理：
#   客户情绪不好  客服说话  客户情绪正常，
#       作为 处理 客户坏情绪 的推荐点。 append到csv最后：：内容为 整段对话； 客户 客服 客户
#   客户情绪不好  客服说话  客户情绪不好  过程中收集
#       作为坏情绪标记点，针对 客户坏情绪  进行 话术模板推荐（车轱辘话）
#       同时可以 通过客户的说话内容，在推荐的 模板中，进行 相似度文本匹配，从而得到 内容相近的 问题的模板！！
#
#
# 客服情绪处理：
#   客服情绪不好：
#        针对客服的内容，进行相似语句匹配，从而得到 相似的内容，但客服语句比较好的。
#        同时可以推荐车轱辘话。
#


# todo
# 首先读取每一个文件，同时进行推荐点标记。。  直接放到案例生成的地方去进行使用
# todo 既然是推荐，直接生成一个推荐库算了。。向推荐库里面append，已经ok了

# 对每一个 模板，进行 推荐点 遍历寻找：：
#   推荐库查找：
#      客户坏情绪：
#        客服和客户对话问题在推荐库中，进行相似度匹配，得到最相似的3个模板
#      客服坏情绪：
#         直接全局所有案例查找相似的 话，同时 通过情绪过滤。。
#   话术模板查找：
#       根据推荐点的不同位置，进行话术模板细分，从而进行推荐匹配。
#           客户坏情绪
#               出现的位置：：开头坏情绪  ||  中间普通坏情绪
#           客服坏情绪
#                 模板
#


# 客户坏情绪 客服： 推荐库类似寻找。。
# 开头坏情绪（客服和客户坏情绪都可以处理 ），结尾坏情绪（）；


# 为每一个模板进行 被推荐点搜索
def find_curFile_recommended_points(filename):
    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)
    talkText = []

    # 特殊逻辑，特殊筛选
    customer_talk = []
    service_talk = []
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1 and item[0] == "-1":
            #   开头探测！！！
            print('第一行内容：本文已生成过推荐')
            return
        # 先全部读取到 list中；
        # 保护逻辑！！
        if (len(item) > 2):
            isCustomerService = False
            if (item[2] == "客服"):
                isCustomerService = True
            if (isCustomerService):
                service_talk.append(Sentence(isCustomerService, item[3], item[7]))
            else:
                customer_talk.append(Sentence(isCustomerService, item[3], item[7]))
            talkText.append(Sentence(isCustomerService, item[3], item[7]))
        else:
            print("异常长度的空行")
            for str in item:
                print(str)
    csvFile.close()

    i = 0
    for item in customer_talk:
        if (item.emotion == "pessimistic" and i < 3):
            customer_start_bad_emotion.append(item)
        if (item.emotion == "pessimistic" and i >= len(customer_talk) - 3):
            customer_end_bad_emotion.append(item)
        i = i + 1

    i = 0
    for item in service_talk:
        if (item.emotion == "pessimistic" and i < 3):
            service_start_bad_emotion.append(item)
        if (item.emotion == "pessimistic" and i >= len(service_talk) - 3):
            service_end_bad_emotion.append(item)
        i = i + 1

    for i in range(len(talkText)):
        # print(talkText[i].__str__())
        # 客户坏情绪 客服： 推荐库类似寻找。。 客户坏情绪，客服说话
        # 客户坏情绪，到 服务模板中寻找匹配。。。取前10；
        if (i + 1 < len(talkText) and talkText[i].isCustomerService == False and talkText[i].emotion == "pessimistic"
                and len(talkText[i].line) >= 4 and len(talkText[i + 1].line) >= 4
                and talkText[i + 1].isCustomerService == True):
            emotion_point = "客户:" + talkText[i].line + "客服:" + talkText[
                i + 1].line
            customer_bad_emotion.append([i, emotion_point])
            # print("行号:" + str(i) + " " + emotion_point)

        # 客服坏情绪
        # 到推荐模板 和话术 中进行 相似度匹配。。
        if (talkText[i].isCustomerService == True and len(talkText[i].line) >= 4 and
                talkText[i].emotion == "pessimistic"):
            emotion_point = talkText[i].line
            customerService_bad_emotion.append([i, emotion_point])
            # print("行号:" + str(i) + " " + "客服: " + emotion_point)


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def sentence_vector(sentence):
    punctuation_str = punctuation
    for i in punctuation_str:
        sentence = sentence.replace(i, '')
    sentence = sentence.replace(':', '')
    sentence = sentence.replace(',', '')
    sentence = sentence.replace('.', '')
    words = jieba.lcut(sentence)
    v = np.zeros(64)
    for word in words:
        if (is_Chinese(word) and word != "客户" and word != "客服"):
            try:
                v += model[word]
            except KeyError:
                print("本词无法提取向量：" + word)
    v /= len(words)
    return v


def vector_similarity(potentialSentence, targetS):
    v1, v2 = sentence_vector(potentialSentence), sentence_vector(targetS)
    # print(v1, v2)
    similarity = np.dot(v1, v2) / (norm(v1) * norm(v2))
    return similarity


recommendation_library_file = 'DONE/recommendation/recommendation_library.csv'
speech_skill_file = 'DONE/recommendation/speech_skill.csv'
service_template_file = 'DONE/recommendation/service_template.csv'


def gen_similar_recommendation_points():
    # 结合 是否有 客服 or 客服 开头坏情绪  客户or客服结尾坏情绪 进行  推荐模板 架构生成
    # 放在开头，进行门面扩充！

    #   也可以结合案例评分，进行 是否 推荐服务模板。。。。。。。。

    # service_start_bad_emotion = []
    # service_end_bad_emotion = []

    # customer_start_bad_emotion = []
    # customer_end_bad_emotion = []

    # 读取开头和结尾 客服应对方法：
    recommendation_points = []

    csvFile = open(speech_skill_file, "r")
    reader = csv.reader(csvFile)
    start_speech_skill_pureStrs = []
    end_speech_skill_pureStrs = []
    for item in reader:
        if (item[0] == "3"):
            start_speech_skill_pureStrs.append(item[1])
        elif (item[0] == "4"):
            end_speech_skill_pureStrs.append(item[1])
    csvFile.close()

    # 开头推荐语句：
    start_Flag = 0  # 开头坏情绪 0 无  1 客服 2 客户 3 客服和客户

    end_Flag = 0  # 结尾坏情绪 0 无  1 客服 2 客户 3 客服和客户

    if (len(service_start_bad_emotion) > 0):
        # print("客服开头有坏情绪：")
        start_Flag = 1
    if (len(customer_start_bad_emotion) > 0):
        # print("客户开头有坏情绪：")
        if (start_Flag == 1):
            start_Flag = 3
        else:
            start_Flag = 2
    if (len(service_end_bad_emotion) > 0):
        # print("客服结尾有坏情绪：")
        end_Flag = 1
    if (len(customer_end_bad_emotion) > 0):
        if (end_Flag == 1):
            end_Flag = 3
        else:
            end_Flag = 2
        # print("客户结尾有坏情绪：")

    startANDend_recommended_template = "开头结尾推荐为空"
    if (start_Flag != 0):
        startANDend_recommended_template = get_templateDsec(True, start_Flag) + "\n"
        #     todo 随机挑选几条开头对应；
        randomIndex = []
        while (len(randomIndex) < 3):
            curindex = random.randint(0, len(start_speech_skill_pureStrs) - 1)
            if (curindex not in randomIndex):
                randomIndex.append(curindex)
        for index in randomIndex:
            startANDend_recommended_template = startANDend_recommended_template + start_speech_skill_pureStrs[
                index] + "\n"
        recommendation_points.append(startANDend_recommended_template)
    if (end_Flag != 0):
        startANDend_recommended_template = get_templateDsec(False, end_Flag) + "\n"
        randomIndex = []
        while (len(randomIndex) < 3):
            curindex = random.randint(0, len(end_speech_skill_pureStrs) - 1)
            if (curindex not in randomIndex):
                randomIndex.append(curindex)
        for index in randomIndex:
            startANDend_recommended_template = startANDend_recommended_template + end_speech_skill_pureStrs[
                index] + "\n"
        recommendation_points.append(startANDend_recommended_template)
    # 有客服坏情绪

    # recommendation_points = []
    if (start_Flag == 0 and end_Flag == 0):
        # 若无可推荐点，则如此添加
        if (len(customer_bad_emotion) == 0 and len(customerService_bad_emotion) == 0):
            print("本案例未发现推荐点。")
            recommendation_points.append("本案例尚未分析出推荐点，敬请期待后续升级")
            return recommendation_points

        #   生成客服指导模板：

        print("本案例无开头结尾问题，生成 客服服务模板：")
        # service_template_file

        csvFile = open(service_template_file, "r")
        reader = csv.reader(csvFile)

        service_skill_pattern_describes = []
        service_skill_pattern_one = []
        service_skill_pattern_two = []
        service_skill_pattern_three = []
        for item in reader:
            if (len(item) >= 2):
                if (reader.line_num == 1):
                    # print("构建描述")
                    pattern_describes_list = item[1].split("")
                    for describe_item in pattern_describes_list:
                        cur_describe = describe_item.split(":")[1]
                        service_skill_pattern_describes.append(cur_describe)
                else:
                    # print("构建skills")
                    cur_index = int(item[0].split(".")[1])
                    if (cur_index == 1):
                        service_skill_pattern_one.append(item[1])
                    elif (cur_index == 2):
                        service_skill_pattern_two.append(item[1])
                    elif (cur_index == 3):
                        service_skill_pattern_three.append(item[1])
            else:
                print("service_template 本行不符合 长度要求" + item[0])
        csvFile.close()
        # 开始构建内容
        service_template = "本案例开头和结尾客服情绪和客户情绪稳定；客服可参考下面服务模板进行客户服务：\n"
        recommendation_points.append(service_template)
        # 开始分批构建推荐点：
        service_template = service_skill_pattern_describes[0] + "\n模板如下：\n"

        randomIndex = []
        while (len(randomIndex) < 3):
            curindex = random.randint(0, len(service_skill_pattern_one) - 1)
            if (curindex not in randomIndex):
                randomIndex.append(curindex)
        for index in randomIndex:
            service_template = service_template + service_skill_pattern_one[
                index] + "\n"
        recommendation_points.append(service_template)
        #
        service_template = service_skill_pattern_describes[1] + "\n模板如下：\n"
        service_template = service_template + service_skill_pattern_two[0] + "\n"
        service_template = service_template + service_skill_pattern_two[1] + "\n"
        recommendation_points.append(service_template)
        #
        service_template = service_skill_pattern_describes[2] + "\n模板如下：\n"
        randomIndex = []  # 置空
        while (len(randomIndex) < 3):
            curindex = random.randint(0, len(service_skill_pattern_three) - 1)
            if (curindex not in randomIndex):
                randomIndex.append(curindex)
        for index in randomIndex:
            service_template = service_template + service_skill_pattern_three[
                index] + "\n"
        recommendation_points.append(service_template)

    # 模板推荐： 根据识别出的情绪点进行推荐。
    csvFile = open(recommendation_library_file, "r")
    reader = csv.reader(csvFile)
    # ！！！
    recommendation_library_pureStrs = []
    for item in reader:
        recommendation_library_pureStrs.append(item[4])
    csvFile.close()

    csvFile = open(speech_skill_file, "r")
    reader = csv.reader(csvFile)
    # ！！！！！！
    speech_skill_pureStrs = []
    for item in reader:
        speech_skill_pureStrs.append(item[1])
    csvFile.close()

    customer_badEmotion_goodReply_cases = "客户坏情绪推荐为空"
    if (len(customer_bad_emotion) > 0):
        customer_badEmotion_goodReply_cases = "以下是 当客户出现不良情绪后，依托本案例中的情况，进行优秀的服务相似案例推荐：" + "\n"
        recommendation_points.append(customer_badEmotion_goodReply_cases)
        # 尝试进行匹配：
        # customer_bad_emotion  [i, emotion_point]
        # 客户坏情绪，客服服务，，，模板对话匹配
        for targetItem in customer_bad_emotion:
            curTargetStr = targetItem[1]
            # print("当前匹配情绪点： "+curTargetStr)
            curTargetStr_potential_similarity = []
            for recommend_temp in recommendation_library_pureStrs:
                curTargetStr_potential_similarity.append(
                    [vector_similarity(recommend_temp, curTargetStr), recommend_temp])

            sorted_curTargetStr_potential_similarity = sorted(curTargetStr_potential_similarity, key=lambda x: x[0],
                                                              reverse=True)
            # for item in sorted_curTargetStr_potential_similarity:
            #     print("相似度"+str(item[0])+"内容："+item[1])
            # 只取前 3个：
            customer_badEmotion_goodReply_cases = "针对此段对话：" + curTargetStr + '\n' + "可借鉴以下优秀对话：" + '\n'
            for i in range(2):
                customer_badEmotion_goodReply_cases = customer_badEmotion_goodReply_cases + \
                                                      sorted_curTargetStr_potential_similarity[i][1] + '\n'
            recommendation_points.append(customer_badEmotion_goodReply_cases)

    # 客服坏情绪：模板对话 + 话术库 匹配

    service_badEmotion_goodReply_cases = "客服坏情绪推荐为空"
    if (len(customerService_bad_emotion) > 0):
        service_badEmotion_goodReply_cases = "当客服在服务过程中出现不良情绪时，也可借鉴如下优秀客服模板话术：" + "\n"
        recommendation_points.append(service_badEmotion_goodReply_cases)
        for targetItem in customerService_bad_emotion:  # customerService_bad_emotion.append([i, emotion_point])
            curTargetStr = targetItem[1]
            # print("当前匹配情绪点： " + curTargetStr)
            # 先匹配 推荐的话术
            service_badEmotion_goodReply_cases = "此段对话出现客服不良情绪： 客服：" + curTargetStr + "\n"

            curTargetStr_skill_potential_similarity = []
            for recommend_temp in speech_skill_pureStrs:
                curTargetStr_skill_potential_similarity.append(
                    [vector_similarity(recommend_temp, curTargetStr), recommend_temp])

            sorted_curTargetStr_skill_potential_similarity = sorted(curTargetStr_skill_potential_similarity,
                                                                    key=lambda x: x[0],
                                                                    reverse=True)
            # 看一下 话术模板 的匹配度
            # for item in sorted_curTargetStr_skill_potential_similarity:
            #     print("话术相似度" + str(item[0]) + "内容：" + item[1])
            service_badEmotion_goodReply_cases = service_badEmotion_goodReply_cases + "针本段对话，也可借鉴如下优秀客服模板话术：" + '\n'
            for i in range(3):
                service_badEmotion_goodReply_cases = service_badEmotion_goodReply_cases + \
                                                     sorted_curTargetStr_skill_potential_similarity[i][1] + '\n'

            # ----------------------------------------
            # 再匹配 相似的案例
            curTargetStr_recommend_potential_similarity = []
            for recommend_temp in recommendation_library_pureStrs:
                curTargetStr_recommend_potential_similarity.append(
                    [vector_similarity(recommend_temp, curTargetStr), recommend_temp])

            sorted_curTargetStr_potential_similarity = sorted(curTargetStr_recommend_potential_similarity,
                                                              key=lambda x: x[0],
                                                              reverse=True)
            # 看一下 推荐对话中 的匹配度
            service_badEmotion_goodReply_cases = service_badEmotion_goodReply_cases + "关于本段对话，可借鉴以下优秀对话：" + '\n'

            # for item in sorted_curTargetStr_potential_similarity:
            #     print("模板相似度" + str(item[0]) + "内容：" + item[1])
            service_badEmotion_goodReply_cases = service_badEmotion_goodReply_cases + \
                                                 sorted_curTargetStr_potential_similarity[1][1] + '\n'
            recommendation_points.append(service_badEmotion_goodReply_cases)

    return recommendation_points


start_customer_str = "客户在聊天开头有不良情绪，客服可参考下面客服服务话术："
start_service_str = "客服在聊天开头存在不良情绪，可学习下面客服服务话术："
start_all_str = "当客户在聊天开头就有不良情绪，客服可学习使用下面话术进行服务，客服作为服务方，尽量不要对客户出现负面情绪："

end_customer_str = "客户在聊天结尾仍有不良情绪，客服可参考下面服务话术，进行安抚："
end_service_str = "客服在聊天结尾存在不良情绪，可学习使用下面话术，进行服务："
end_all_str = "当客户在聊天结尾时，仍然抱有不良情绪，客服可学习使用下面话术进行安慰，客服作为服务方，尽量不要对客户出现负面情绪："


def get_templateDsec(isStart, flag):
    if (isStart):
        if (flag == 1):
            return start_customer_str
        elif (flag == 2):
            return start_service_str
        elif (flag == 3):
            return start_all_str
    else:
        if (flag == 1):
            return end_customer_str
        elif (flag == 2):
            return end_service_str
        elif (flag == 3):
            return end_all_str


def insert_recommendation(filename, complete_recommendation_points):
    # 直接生成对应的发送个前端的 json文件。。
    # print("直接生成推荐的json文件")
    # print("正好用来测试前端的推荐部分。。")
    file_path_list = filename.split('/')
    print(filename)
    listLength = len(file_path_list)
    if (listLength < 2):
        print("文件路径不合法：：" + filename)
    dir_name = file_path_list[listLength - 2]
    source_file_name = file_path_list[listLength - 1].split('.')[0]
    curfile_dir_path = os.path.join(to_recommend_root_path, dir_name)

    print(dir_name)
    print(source_file_name)
    print(curfile_dir_path)
    if not os.path.exists(curfile_dir_path):
        os.makedirs(curfile_dir_path)

    target_file_path = os.path.join(curfile_dir_path, source_file_name + ".json")
    print(target_file_path)

    recommendation_obj = {
        "recommendation_points": complete_recommendation_points
    }

    with open(target_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(recommendation_obj, jsonfile, ensure_ascii=False, indent=4)

    # print("完成推荐内容生成")


def do_recommend(file_path):
    global customer_start_bad_emotion, customer_end_bad_emotion, service_start_bad_emotion, service_end_bad_emotion, \
        customer_bad_emotion, customerService_bad_emotion
    customer_start_bad_emotion = []
    customer_end_bad_emotion = []
    service_start_bad_emotion = []
    service_end_bad_emotion = []
    customer_bad_emotion = []
    customerService_bad_emotion = []

    find_curFile_recommended_points(file_path)
    complete_recommendation_points = gen_similar_recommendation_points()
    insert_recommendation(file_path, complete_recommendation_points)


if __name__ == '__main__':
    # 测试被推荐点寻找

    # 这里中文的长度正常了，可能是重新文件，编码改变了

    # 单文件测试的话，放开这些注释，
    # test_filename = "../数据/DONE/speaker_role_text_emotion_csvs/001/173210511250216100524891.csv"

    # test_filename = "../数据/DONE/speaker_role_text_emotion_csvs/001/136611797590130093850586.csv"
    # find_curFile_recommended_points(test_filename)
    # complete_recommendation_points=gen_similar_recommendation_points()
    # for recommendation_point in complete_recommendation_points:
    #     print(recommendation_point)

    # data_root_paths = r'../数据/DONE/speaker_role_text_emotion_csvs'
    # recommendation_root_paths = r'../数据/recommendation'

    # insert_recommendation(test_filename, complete_recommendation_points)

    # 批量跑 所有的 案例生成 推荐的内容
    # data_root_paths = r'../数据/DONE/speaker_role_text_emotion_csvs'
    # recommendation_root_paths = r'../数据/recommendation'
    # 防止上面报错
    # list_dir(file_dir=data_root_paths)
    # for filePath in list_csv:
    #     try:
    #         customer_start_bad_emotion = []
    #         customer_end_bad_emotion = []
    #
    #         service_start_bad_emotion = []
    #         service_end_bad_emotion = []
    #
    #         customer_bad_emotion = []
    #         customerService_bad_emotion = []
    #
    #         find_curFile_recommended_points(filePath)
    #         complete_recommendation_points = gen_similar_recommendation_points()
    #         insert_recommendation(filePath, complete_recommendation_points)
    #     #   todo 每次清空响应的缓存
    #
    #     except Exception:
    #         print("当前文件出错")
    #         print(filePath)
    # 真正的调用


    # 传入的 文件名；
    file_path = "TODO/speaker_role_text_emotion_csvs/172/136611797590130093850586.csv"

    do_recommend(file_path)
