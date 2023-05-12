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

    # 透過座標，找尋項目右邊相對應的值 (key: value, 姓名: XXX)
    for i in range(len(ocr_result)):
        if is_item_classified_list[i]:
            continue

        # 找右邊相對應的 item
        key, value, value_index = __find_right_item(i, ocr_result, is_item_classified_list)
        if (key != None):
            is_item_classified_list[i] = True
            is_item_classified_list[value_index] = True
            key_full_name_list = __find_key_full_name(value_index, ocr_result, is_item_classified_list)

            # 將 key 字串組合
            for i in range(0, len(key_full_name_list), 2):
                key += key_full_name_list[i]
                is_item_classified_list[i + 1] = True

            classify_dic[key] = value
            continue

        # 尋找姓名
        if __is_person_name(ocr_result[i][1][0]):
            is_item_classified_list[i] = True
            classify_dic["姓名"] = ocr_result[i][1][0]
            continue

        if __is_ID_number(ocr_result[i][1][0]):
             is_item_classified_list[i] = True
             classify_dic["身分證字號"] = ocr_result[i][1][0]
             continue

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
        - key: 項目     # 姓名
        - value:  對應值      # 王小明
        - value_index:  對應值位置    # 0
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
    '''
    找到項目完整字串列表 (key: value 找到 full_key)

    Args:
        - value_index: 對應值位置 (key)
        - ocr_result: paddleOCR 辨識結果(4層array，原本為5層)
        - is_item_classified_list: 已分配項目陣列

    Return:
        - key_full_name_list: 項目完整字串、位置列表   # [身分證, 0, 统一编號, 2]
    '''
    result_list = []

    value_left_top_corner_y = ocr_result[value_index][0][0][1]
    value_left_down_corner_x = ocr_result[value_index][0][3][0]
    value_left_down_corner_y = ocr_result[value_index][0][3][1]

    for item_index in range(len(ocr_result)):
        if ((item_index == value_index) or (is_item_classified_list[item_index])):
            continue

        # 位在 value 左邊 20 pixels 以內，同時 其右上角點的y軸 界在 value 的左上角及左下角之間，則分配在一起
        if (0 <= value_left_down_corner_x - ocr_result[item_index][0][1][0] <= 20 and
                value_left_top_corner_y <= ocr_result[item_index][0][1][1] <= value_left_down_corner_y):
            result_list.append(ocr_result[item_index][1][0])
            result_list.append(item_index)
    return result_list

# 辨識姓名
def __is_person_name(str):
    '''
    辨識字串是否為姓名

    Args:
        - str: 辨識字串

    Return:
        - True: 是姓名
        - False: 不是姓名
    '''
    name_regex = '[陳|林|黃|張|李|王|吳|劉|蔡|楊|許|鄭|謝|洪|郭|邱|曾|廖|賴|徐|周|葉|蘇|莊|呂|江|何|蕭|羅|高|潘|簡|朱|鍾|游|彭|詹|胡|施|沈|余|盧|梁|趙|顏|柯|翁|魏|孫|戴|范|方|宋|鄧|杜|傅|侯|曹|薛|丁|卓|阮|馬|董|温|唐|藍|石|蔣|古|紀|姚|連|馮|歐|程|湯|黄|田|康|姜|白|汪|鄒|尤|巫|鐘|黎|涂|龔|嚴|韓|袁|金|童|陸|夏|柳|凃|邵|錢|伍|倪|溫|于|譚|駱|熊|任|甘|秦|顧|毛|章|史|官|萬|俞|雷|粘|饒|張簡|闕|凌|崔|尹|孔|歐陽|辛|武|辜|陶|易|段|龍|韋|葛|池|孟|褚|殷|麥|賀|賈|莫|文|管|關|向|包|丘|梅|范姜|華|利|裴|樊|房|全|佘|左|花|魯|安|鮑|郝|穆|塗|邢|蒲|成|谷|常|閻|練|盛|鄔|耿|聶|符|申|祝|繆|陽|解|曲|岳|齊|籃|應|單|舒|畢|喬|龎|翟|牛|鄞|留|季|覃|卜|項|凃|喻|商|滕|焦|車|買|虞|苗|戚|牟|雲|巴|力|艾|樂|臧|司|樓|費|屈|宗|幸|衛|尚|靳|祁|諶|桂|沙|欒|宮|路|刁|時|龐|瞿][\u4e00-\u9fa5]{1,3}$'
    return re.search(name_regex, str)

# 辨識身分證字號
def __is_ID_number(str):
    '''
    辨識字串是否為身分證字號

    Args:
        - str: 辨識字串

    Return:
        - True: 是身分證字號
        - False: 不是身分證字號
    '''
    ID_number_regex = '^[A-Z]{1}[1-2]{1}[0-9]{8}$'
    return re.search(ID_number_regex, str)


if __name__ == "__main__":
    ocr_result = [[[[186.0, 49.0], [677.0, 49.0], [677.0, 138.0], [186.0, 138.0]], ('中華民國技術士證', 0.7252095341682434)],
                  [[[20.0, 179.0], [160.0, 183.0], [159.0, 218.0],
                      [19.0, 214.0]], ('身分證', 0.6735596656799316)],
                  [[[172.0, 202.0], [385.0, 202.0], [385.0, 236.0], [
                      172.0, 236.0]], ('E125151692', 0.9046633839607239)],
                  [[[19.0, 224.0], [159.0, 224.0], [159.0, 255.0], [
                      19.0, 255.0]], ('统一编號', 0.8357518911361694)],
                  [[[26.0, 289.0], [160.0, 289.0], [160.0, 317.0], [
                      26.0, 317.0]], ('出生日期', 0.9387126564979553)],
                  [[[172.0, 281.0], [523.0, 275.0], [523.0, 320.0], [
                      173.0, 326.0]], ('民國85年06月26日', 0.9239855408668518)],
                  [[[22.0, 347.0], [160.0, 352.0], [159.0, 383.0], [
                      21.0, 378.0]], ('技術士證', 0.9631977081298828)],
                  [[[174.0, 359.0], [376.0, 364.0], [375.0, 402.0], [
                      173.0, 397.0]], ('062-018046', 0.9462512135505676)],
                  [[[18.0, 387.0], [160.0, 390.0], [159.0, 425.0],
                      [18.0, 422.0]], ('總编號', 0.7739713191986084)],
                  [[[171.0, 446.0], [571.0, 453.0], [570.0, 491.0], [
                      171.0, 484.0]], ('移動式起重機操作一', 0.9073466062545776)],
                  [[[27.0, 459.0], [151.0, 459.0], [151.0, 491.0],
                      [27.0, 491.0]], ('類(填', 0.6324031352996826)],
                  [[[783.0, 462.0], [917.0, 466.0], [916.0, 510.0],
                      [781.0, 506.0]], ('蔡欣祐', 0.9361932873725891)],
                  [[[174.0, 496.0], [393.0, 501.0], [392.0, 544.0], [
                      173.0, 539.0]], ('伸臂可伸缩', 0.9856359362602234)],
                  [[[22.0, 509.0], [143.0, 509.0], [143.0, 543.0],
                      [22.0, 543.0]], ('名', 0.9989275336265564)],
                  [[[786.0, 513.0], [909.0, 516.0], [908.0, 557.0],
                      [785.0, 554.0]], ('罩一级', 0.8342120051383972)],
                  [[[698.0, 527.0], [776.0, 527.0], [776.0, 559.0],
                      [698.0, 559.0]], ('级别', 0.9833779335021973)],
                  [[[899.0, 687.0], [1051.0, 690.0], [1050.0, 716.0], [899.0, 713.0]], ('努動部發', 0.5823800563812256)]]

    ocr_result_list = ['中華民國技術士登', '身分證', 'E125151692', '統一編號', '出生日期', '民國85年06月26日', '技術士證', '062-018046', '總編號',
                       '移動式起重機操作', '頰(填', '蔡欣祐', '伸臂可伸縮', '名', '軍一級', '級別', '囍', '民國108年11月18日，製發日期', '生效日期', '民國108年11月18日', '努動部發']

    print(text_classify_logic(ocr_result))

