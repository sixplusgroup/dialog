# -*- coding: UTF-8

import csv
import os


class Sentence:

    def __init__(self, isCustomerService, emotion):
        self.isCustomerService = isCustomerService
        self.emotion = emotion
        self.fusion_emotion = emotion

    def __str__(self):  # 定义打印对象时打印的字符串

        return " ".join(str(item) for item in (
            self.isCustomerService, self.emotion, self.fusion_emotion))

    def set_fusion_emotion(self, emotion):
        self.fusion_emotion = emotion


def get_soundEmotion(soundEmotion):
    res = "";
    if (soundEmotion == "angry" or soundEmotion == "sad"):
        res = "pessimistic";
    elif (soundEmotion == "happy"):
        res = "optimistic";
    else:
        res = "neutral";
    return res;


def fusion_emotion(soundEmotion, textEmotion):
    resEmotion = "";
    if (textEmotion == "pessimistic"):
        resEmotion = "pessimistic";
    elif (textEmotion == "neutral"):
        resEmotion = soundEmotion;
    elif (textEmotion == "optimistic"):
        if (soundEmotion == "pessimistic"):
            resEmotion = "pessimistic";
        else:
            resEmotion = "optimistic";
    return resEmotion;


def gen_fusion_emotion(character, audio_emotions, text_emotions, length):
    talkText = [];
    for i in range(length):
        # 先全部读取到 list中；
        isCustomerService = False;
        if character[i] == "客服":
            isCustomerService = True;
        soundEmotion = get_soundEmotion(audio_emotions[i])
        textEmotion = text_emotions[i].split(' ')[0]
        talkText.append(Sentence(isCustomerService, fusion_emotion(soundEmotion, textEmotion)))

    i = 0;
    while (i < length - 1):
        cur_flag_isCustomerService = talkText[i].isCustomerService;
        for j in range(i + 1, len(talkText)):
            if (talkText[j].isCustomerService != cur_flag_isCustomerService):
                break;
        #       i-j-1 是一段 or 1个
        if (j - 1 == i):
            # 可以这样调用，
            # talkText[i].set_fusion_emotion(get_single_fusion_emotion(talkText[i].emotion));
            talkText[i].set_fusion_emotion(talkText[i].emotion)
        else:
            fusioned_emotion = "neutral"
            for k in range(i, j):
                if (talkText[k].emotion != "neutral"):
                    fusioned_emotion = talkText[k].emotion;
                    break
            for k in range(i, j):
                talkText[k].set_fusion_emotion(fusioned_emotion);
        i = j;

    return [(_.emotion, _.fusion_emotion) for _ in talkText]
