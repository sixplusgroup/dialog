import csv
import os

recommendation_root_path = 'DONE/recommendation'
recommendation_library_path = 'DONE/recommendation/recommendation_library.csv'
negative_recommendation_library_path = 'DONE/recommendation/negative_recommendation_library.csv'
data_root_paths = 'TODO/speaker_role_text_emotion_csvs'
recommendation_points = []
emotion_points = []
negative_emotion_points = []
list_csv = []


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


def gene_recommendation_points(filename):
    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)
    talkText = []
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1 and item[0] == "-1":
            print("已进行过推荐点生成")
            return
        # 先全部读取到 list中；
        if (len(item) > 2):
            isCustomerService = False
            if (item[2] == "客服"):
                isCustomerService = True
            talkText.append(Sentence(isCustomerService, item[3], item[7]))
        else:
            print("异常长度的空行")
            for line in item:
                print(line)
    for i in range(len(talkText)):
        # print(talkText[i].__str__())
        # 反面教材
        if (i + 1 < len(talkText) and talkText[i].isCustomerService == True and len(talkText[i].line) >= 3 and len(
                talkText[i + 1].line) >= 3 and talkText[i + 1].emotion == "pessimistic" and talkText[
            i + 1].isCustomerService == False):
            emotion_point = "客服:" + talkText[i].line + "客户:" + talkText[
                i + 1].line
            fileInfo = getFileInfoByFilename(filename)
            negative_emotion_points.append([0, fileInfo[0], fileInfo[1], str(i), emotion_point])
            # print filename + "  行号:" + str(i) + " " + emotion_point
        # 正向情况  中文一个字 长度为3 进行过滤
        if (i + 1 < len(talkText) and talkText[i].isCustomerService == True and len(talkText[i].line) >= 3 and
                talkText[
                    i + 1].emotion == "optimistic" and len(talkText[i + 1].line) >= 3 and talkText[
                    i + 1].isCustomerService == False):
            emotion_point = "客服:" + talkText[i].line + "客户:" + talkText[
                i + 1].line
            fileInfo = getFileInfoByFilename(filename)
            emotion_points.append([1, fileInfo[0], fileInfo[1], str(i), emotion_point])
            print(filename + "  行号:" + str(i) + " " + emotion_point)
        # 交互模板
        if (i + 2 < len(talkText) and talkText[i].emotion == "pessimistic" and talkText[
            i].isCustomerService == False and
                talkText[i + 1].isCustomerService == True and talkText[i + 2].isCustomerService == False and talkText[
                    i + 2].emotion != "pessimistic"):
            # 找到了标定点：
            recommendation_point = "客户:" + talkText[i].line + "客服:" + talkText[i + 1].line + "客户:" + talkText[
                i + 2].line
            fileInfo = getFileInfoByFilename(filename)
            recommendation_points.append([2, fileInfo[0], fileInfo[1], str(i), recommendation_point])
    # 开头插入空行 -1 已生成 有推荐点，-2 无推荐点
    csvFile.close()
    # 将 推荐模板，填充进推荐库中。


# ../数据/DONE/speaker_role_text_emotion_csvs/001/131481949120228113002048.csv
def getFileInfoByFilename(fullFilename):
    file_path_list = fullFilename.split('/')
    print(fullFilename)
    listLength = len(file_path_list)
    if (listLength < 2):
        print("文件路径不合法：：" + fullFilename)
    CSSid = file_path_list[listLength - 2]

    filename = file_path_list[listLength - 1].split(".")[0]
    fileInfo = []
    fileInfo.append(CSSid)
    fileInfo.append(filename)
    return fileInfo


def list_dir(file_dir):
    # list_csv = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        # 判断是文件夹还是文件
        if os.path.isfile(path):
            # print("{0} : is file!".format(cur_file))
            dir_files = os.path.join(file_dir, cur_file)
        # 判断是否存在.csv文件，如果存在则获取路径信息写入到list_csv列表中
        if os.path.splitext(path)[1] == '.csv':
            csv_file = os.path.join(file_dir, cur_file)
            # print(os.path.join(file_dir, cur_file))
            # print(csv_file)
            list_csv.append(csv_file)
        if os.path.isdir(path):
            # print("{0} : is dir".format(cur_file))
            # print(os.path.join(file_dir, cur_file))
            list_dir(path)
    return list_csv


def build_recommendation_library():
    global recommendation_points, emotion_points, negative_emotion_points, list_csv
    recommendation_points = []
    emotion_points = []
    negative_emotion_points = []
    list_csv = []

    if not os.path.exists(recommendation_root_path):
        os.makedirs(recommendation_root_path)
    if not os.path.exists(recommendation_library_path):
        f = open(recommendation_library_path, 'w')
        f.close()
    if not os.path.exists(negative_recommendation_library_path):
        f = open(negative_recommendation_library_path, 'w')
        f.close()

    #  跑所有的已有库文件生成csv文件
    list_dir(file_dir=data_root_paths)

    for filePath in list_csv:
        gene_recommendation_points(filePath)

    # 如果是单文件调用的话直接用下面的句子
    # filePath = "../数据/DONE/speaker_role_text_emotion_csvs/001/136611797590130093850586.csv"
    # gene_recommendation_points(filePath)

    # 插入到推荐库
    recommendation_library_file = open(recommendation_library_path, "a")
    writer = csv.writer(recommendation_library_file)
    for recommendation_point in recommendation_points:
        writer.writerow(recommendation_point)
    for recommendation_point in emotion_points:
        writer.writerow(recommendation_point)
    # for recommendation_point in negative_emotion_points:
    #     writer.writerow(recommendation_point)
    recommendation_library_file.close()

    # 生成，非优秀案例库，以备用。
    negative_recommendation_library_file = open(negative_recommendation_library_path, "a")
    writer = csv.writer(negative_recommendation_library_file)
    for recommendation_point in negative_emotion_points:
        writer.writerow(recommendation_point)
    negative_recommendation_library_file.close()


if __name__ == '__main__':
    build_recommendation_library()
