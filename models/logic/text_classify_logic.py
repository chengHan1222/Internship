import math
import re


def text_classify_logic(ocr_result):
    '''
    針對 OCR 辨識結果，進行文字分類

    Args:
        - ocr_result: paddleOCR 辨識結果(4層array，原本為5層)

    Return:
        - classify_dic: 文字信息匹配 dictionary   # {"姓名":"XXX", "身分證字號":"A123456789"}
    '''
    # 文字信息匹配
    classify_dic = {}

    # 已分配項目陣列
    is_item_classified_list = []
    for i in range(len(ocr_result)):
        is_item_classified_list.append(False)

    # 辨識姓名
    name = ""
    name_distance = 1980

    # 辨識身分證字號
    ID_number_regex = r'^[A-Z]{1}[1-2]{1}[0-9]{8}$'

    # 透過座標，找尋項目右邊相對應的值 (key: value, 姓名: XXX)
    for i in range(len(ocr_result)):
        if is_item_classified_list[i]:
            continue
        
        # 找右邊相對應的 item
        key, value, value_index = __find_right_item(i, ocr_result, is_item_classified_list)
        if (key != None):
            is_item_classified_list[i] = True
            is_item_classified_list[value_index] = True
            key_full_name = __find_key_full_name(value_index, ocr_result, is_item_classified_list)
            
            # 將 key 字串組合
            for i in range(0, len(key_full_name), 2):
                key += key_full_name[i]
                is_item_classified_list[i + 1] = True

            classify_dic[key] = value

        # if len(ocr_result[i][1][0]) == 3:
        #     left_top_corner_x  = ocr_result[i][0][0][0]
        #     left_top_corner_y = ocr_result[i][0][0][1]

        #     distance = math.sqrt(left_top_corner_x**2 + left_top_corner_y**2)
        #     if (distance < name_distance):
        #         name_distance = distance
        #         name = ocr_result[i][1][0]

        # if re.findall(ID_number_regex, ocr_result[i][1][0]):
        #     classify_dic["身分證字號"] = ocr_result[i][1][0]

    # classify_dic["姓名"] = name
    return classify_dic

# 找右邊相對應的 value
def __find_right_item(item_index, ocr_result, is_item_classified_list):
    '''
    找到項目右邊最靠近的文字 (key: value 找到 value)

    Args:
        - item_index: 項目位置 (key)
        - ocr_result: paddleOCR 辨識結果(4層array，原本為5層)
        - is_item_classified_list: 已分配項目陣列

    Return:
        - classify_dic: 分類後 dictionary   # {"姓名":"XXX", "身分證字號":"A123456789"}
    '''
    # 項目右上點位置
    item_right_top_corner_x = ocr_result[item_index][0][1][0]
    item_right_top_corner_y = ocr_result[item_index][0][1][1]

    for next_item_index in range(len(ocr_result)):
        if ((item_index == next_item_index) or (is_item_classified_list[next_item_index])):
            continue
            
        # 位在項目右邊 20 pixels 以內，同時 y軸相差 10 pixels 以內，則分配在一起
        if (0 <= ocr_result[next_item_index][0][0][0] - item_right_top_corner_x <= 20 
            and abs(ocr_result[next_item_index][0][0][1] - item_right_top_corner_y) <= 20):
            return ocr_result[item_index][1][0], ocr_result[next_item_index][1][0], next_item_index
    return None, None, None

# 透過 value 的 Y軸(左上、左下)，找到項目完整名稱
def __find_key_full_name(value_index, ocr_result, is_item_classified_list):
    result = []

    value_left_top_corner_y = ocr_result[value_index][0][0][1]
    value_left_down_corner_x = ocr_result[value_index][0][3][0]
    value_left_down_corner_y = ocr_result[value_index][0][3][1]

    for item_index in range(len(ocr_result)):
        if ((item_index == value_index) or (is_item_classified_list[item_index])):
            continue

        # 位在 value 左邊 20 pixels 以內，同時 其右上角點的y軸 界在 value 的左上角及左下角之間，則分配在一起
        if (0 <= value_left_down_corner_x - ocr_result[item_index][0][1][0] <= 20 and
            value_left_top_corner_y <= ocr_result[item_index][0][1][1] <= value_left_down_corner_y):
            result.append(ocr_result[item_index][1][0])
            result.append(item_index)
    return result



if __name__ == "__main__":
    ocr_result = [[[[186.0, 49.0], [677.0, 49.0], [677.0, 138.0], [186.0, 138.0]], ('中華民國技術士證', 0.7252095341682434)], 
                  [[[20.0, 179.0], [160.0, 183.0], [159.0, 218.0], [19.0, 214.0]], ('身分證', 0.6735596656799316)], 
                  [[[172.0, 202.0], [385.0, 202.0], [385.0, 236.0], [172.0, 236.0]], ('E125151692', 0.9046633839607239)], 
                  [[[19.0, 224.0], [159.0, 224.0], [159.0, 255.0], [19.0, 255.0]], ('统一编號', 0.8357518911361694)], 
                  [[[26.0, 289.0], [160.0, 289.0], [160.0, 317.0], [26.0, 317.0]], ('出生日期', 0.9387126564979553)], 
                  [[[172.0, 281.0], [523.0, 275.0], [523.0, 320.0], [173.0, 326.0]], ('民國85年06月26日', 0.9239855408668518)], 
                  [[[22.0, 347.0], [160.0, 352.0], [159.0, 383.0], [21.0, 378.0]], ('技術士證', 0.9631977081298828)], 
                  [[[174.0, 359.0], [376.0, 364.0], [375.0, 402.0], [173.0, 397.0]], ('062-018046', 0.9462512135505676)], 
                  [[[18.0, 387.0], [160.0, 390.0], [159.0, 425.0], [18.0, 422.0]], ('總编號', 0.7739713191986084)], 
                  [[[171.0, 446.0], [571.0, 453.0], [570.0, 491.0], [171.0, 484.0]], ('移動式起重機操作一', 0.9073466062545776)], 
                  [[[27.0, 459.0], [151.0, 459.0], [151.0, 491.0], [27.0, 491.0]], ('類(填', 0.6324031352996826)], 
                  [[[783.0, 462.0], [917.0, 466.0], [916.0, 510.0], [781.0, 506.0]], ('蔡欣祐', 0.9361932873725891)], 
                  [[[174.0, 496.0], [393.0, 501.0], [392.0, 544.0], [173.0, 539.0]], ('伸臂可伸缩', 0.9856359362602234)], 
                  [[[22.0, 509.0], [143.0, 509.0], [143.0, 543.0], [22.0, 543.0]], ('名', 0.9989275336265564)], 
                  [[[786.0, 513.0], [909.0, 516.0], [908.0, 557.0], [785.0, 554.0]], ('罩一级', 0.8342120051383972)], 
                  [[[698.0, 527.0], [776.0, 527.0], [776.0, 559.0], [698.0, 559.0]], ('级别', 0.9833779335021973)], 
                  [[[899.0, 687.0], [1051.0, 690.0], [1050.0, 716.0], [899.0, 713.0]], ('努動部發', 0.5823800563812256)]]

    ocr_result_list = ['中華民國技術士登', '身分證', 'E125151692', '統一編號', '出生日期', '民國85年06月26日', '技術士證', '062-018046', '總編號', '移動式起重機操作', '頰(填', '蔡欣祐', '伸臂可伸縮', '名', '軍一級', '級別', '囍', '民國108年11月18日，製發日期', '生效日期', '民國108年11月18日', '努動部發']

    print(text_classify_logic(ocr_result))
