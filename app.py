from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

# 易經六十四卦資料
YIJING_GUA = {
    0: {"name": "乾", "description": "天行健，君子以自強不息", "interpretation": "大吉大利，積極進取，適合開創新局"},
    1: {"name": "坤", "description": "地勢坤，君子以厚德載物", "interpretation": "順應自然，以柔克剛，適合穩健發展"},
    2: {"name": "屯", "description": "雲雷屯，君子以經綸", "interpretation": "初生艱難，需要耐心和毅力"},
    3: {"name": "蒙", "description": "山下出泉，蒙，君子以果行育德", "interpretation": "啟蒙階段，需要學習和指導"},
    4: {"name": "需", "description": "雲上於天，需，君子以飲食宴樂", "interpretation": "等待時機，不可急躁"},
    5: {"name": "訟", "description": "天與水違行，訟，君子以作事謀始", "interpretation": "避免爭訟，以和為貴"},
    6: {"name": "師", "description": "地中有水，師，君子以容民畜眾", "interpretation": "團結一致，眾志成城"},
    7: {"name": "比", "description": "水在地上，比，君子以建萬國，親諸侯", "interpretation": "親近他人，建立良好關係"},
    8: {"name": "小畜", "description": "風行天上，小畜，君子以懿文德", "interpretation": "小有積蓄，穩步發展"},
    9: {"name": "履", "description": "天上澤下，履，君子以辨上下，定民志", "interpretation": "謹慎行事，遵守禮法"},
    10: {"name": "泰", "description": "天地交，泰，君子以輔相天地之宜", "interpretation": "通泰吉祥，萬事順遂"},
    11: {"name": "否", "description": "天地不交，否，君子以儉德辟難", "interpretation": "時運不濟，需要韜光養晦"},
    12: {"name": "同人", "description": "天與火，同人，君子以類族辨物", "interpretation": "團結合作，志同道合"},
    13: {"name": "大有", "description": "火在天上，大有，君子以遏惡揚善", "interpretation": "大有收穫，保持謙虛"},
    14: {"name": "謙", "description": "地中有山，謙，君子以裒多益寡", "interpretation": "謙遜為美，虛懷若谷"},
    15: {"name": "豫", "description": "雷出地奮，豫，君子以作樂崇德", "interpretation": "心情愉悅，適合慶祝"},
    16: {"name": "隨", "description": "澤中有雷，隨，君子以嚮晦入宴息", "interpretation": "隨順自然，適時而動"},
    17: {"name": "蠱", "description": "山下有風，蠱，君子以振民育德", "interpretation": "除舊佈新，改革創新"},
    18: {"name": "臨", "description": "澤上有地，臨，君子以教思無窮", "interpretation": "面臨挑戰，需要智慧"},
    19: {"name": "觀", "description": "風行地上，觀，君子以省方，觀民設教", "interpretation": "觀察思考，學習成長"},
    20: {"name": "噬嗑", "description": "雷電，噬嗑，先王以明罰敕法", "interpretation": "解決困難，需要決斷"},
    21: {"name": "賁", "description": "山下有火，賁，君子以明庶政，無敢折獄", "interpretation": "文飾美化，注重外表"},
    22: {"name": "剝", "description": "山附於地，剝，君子以厚下安宅", "interpretation": "逐漸衰落，需要謹慎"},
    23: {"name": "復", "description": "雷在地中，復，君子以至日閉關", "interpretation": "重新開始，循環往復"},
    24: {"name": "無妄", "description": "天下雷行，無妄，先王以茂對時，育萬物", "interpretation": "真實不虛，自然而行"},
    25: {"name": "大畜", "description": "天在山中，大畜，君子以多識前言往行", "interpretation": "大有所畜，積累智慧"},
    26: {"name": "頤", "description": "山下有雷，頤，君子以慎言語，節飲食", "interpretation": "修養身心，節制欲望"},
    27: {"name": "大過", "description": "澤滅木，大過，君子以獨立不懼", "interpretation": "過度行事，需要調整"},
    28: {"name": "坎", "description": "水洊至，習坎，君子以常德行，習教事", "interpretation": "困難重重，需要堅持"},
    29: {"name": "離", "description": "明兩作，離，君子以繼明照於四方", "interpretation": "光明照耀，智慧啟迪"},
    30: {"name": "咸", "description": "山上有澤，咸，君子以虛受人", "interpretation": "感應相應，心靈相通"},
    31: {"name": "恆", "description": "雷風，恆，君子以立不易方", "interpretation": "恆久不變，持之以恆"},
    32: {"name": "遯", "description": "天下有山，遯，君子以遠小人，不惡而嚴", "interpretation": "隱退避讓，遠離小人"},
    33: {"name": "大壯", "description": "雷在天上，大壯，君子以非禮弗履", "interpretation": "力量強大，但需守禮"},
    34: {"name": "晉", "description": "明出地上，晉，君子以自昭明德", "interpretation": "進步發展，光明正大"},
    35: {"name": "明夷", "description": "明入地中，明夷，君子以蒞眾，用晦而明", "interpretation": "光明受損，需要韜光養晦"},
    36: {"name": "家人", "description": "風自火出，家人，君子以言有物，而行有恆", "interpretation": "家庭和睦，言行一致"},
    37: {"name": "睽", "description": "上火下澤，睽，君子以同而異", "interpretation": "意見分歧，需要調和"},
    38: {"name": "蹇", "description": "山上有水，蹇，君子以反身修德", "interpretation": "道路艱難，需要反省"},
    39: {"name": "解", "description": "雷雨作，解，君子以赦過宥罪", "interpretation": "困難解除，寬恕包容"},
    40: {"name": "損", "description": "山下有澤，損，君子以懲忿窒欲", "interpretation": "減少損失，控制情緒"},
    41: {"name": "益", "description": "風雷，益，君子以見善則遷，有過則改", "interpretation": "增益成長，改過遷善"},
    42: {"name": "夬", "description": "澤上於天，夬，君子以施祿及下，居德則忌", "interpretation": "決斷果斷，但需謹慎"},
    43: {"name": "姤", "description": "天下有風，姤，君子以施命誥四方", "interpretation": "相遇機緣，但需選擇"},
    44: {"name": "萃", "description": "澤上於地，萃，君子以除戎器，戒不虞", "interpretation": "聚集力量，防患未然"},
    45: {"name": "升", "description": "地中升木，升，君子以順德，積小以高大", "interpretation": "上升發展，循序漸進"},
    46: {"name": "困", "description": "澤無水，困，君子以致命遂志", "interpretation": "困頓艱難，堅守志向"},
    47: {"name": "井", "description": "木上有水，井，君子以勞民勸相", "interpretation": "井水不竭，助人為樂"},
    48: {"name": "革", "description": "澤中有火，革，君子以治歷明時", "interpretation": "變革創新，順應時勢"},
    49: {"name": "鼎", "description": "木上有火，鼎，君子以正位凝命", "interpretation": "穩重持重，正位凝命"},
    50: {"name": "震", "description": "洊雷，震，君子以恐懼修省", "interpretation": "雷聲震動，驚醒反省"},
    51: {"name": "艮", "description": "兼山，艮，君子以思不出其位", "interpretation": "靜止不動，安守本分"},
    52: {"name": "漸", "description": "山上有木，漸，君子以居賢德善俗", "interpretation": "循序漸進，培養品德"},
    53: {"name": "歸妹", "description": "雷澤歸妹，君子以永終知敝", "interpretation": "歸宿問題，需要謹慎"},
    54: {"name": "豐", "description": "雷電皆至，豐，君子以折獄致刑", "interpretation": "豐盛富裕，但需公正"},
    55: {"name": "旅", "description": "山上有火，旅，君子以明慎用刑，而不留獄", "interpretation": "漂泊不定，需要謹慎"},
    56: {"name": "巽", "description": "隨風，巽，君子以申命行事", "interpretation": "順風而行，執行命令"},
    57: {"name": "兌", "description": "麗澤，兌，君子以朋友講習", "interpretation": "喜悅交流，學習進步"},
    58: {"name": "渙", "description": "風行水上，渙，君子以享於帝立廟", "interpretation": "渙散分散，需要團結"},
    59: {"name": "節", "description": "澤上有水，節，君子以制數度，議德行", "interpretation": "節制約束，適度而行"},
    60: {"name": "中孚", "description": "風澤中孚，君子以議獄緩死", "interpretation": "誠信中正，寬恕包容"},
    61: {"name": "小過", "description": "山上有雷，小過，君子以行過乎恭", "interpretation": "小有過失，需要謹慎"},
    62: {"name": "既濟", "description": "水在火上，既濟，君子以思患而豫防之", "interpretation": "事業已成，防患未然"},
    63: {"name": "未濟", "description": "火在水上，未濟，君子以慎辨物居方", "interpretation": "事業未成，繼續努力"}
}

@app.route('/')
def index():
    """首頁路由"""
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate_numbers():
    """生成兩個隨機數字"""
    try:
        # 生成兩個 1-100 的隨機數字
        number1 = random.randint(1, 100)
        number2 = random.randint(1, 100)
        
        return jsonify({
            'success': True,
            'number1': number1,
            'number2': number2
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/interpret', methods=['POST'])
def interpret_numbers():
    """根據兩個數字進行易經解讀"""
    try:
        data = request.get_json()
        number1 = data.get('number1')
        number2 = data.get('number2')
        
        if number1 is None or number2 is None:
            return jsonify({
                'success': False,
                'error': '缺少數字參數'
            }), 400
        
        # 計算卦象索引：兩個數字的總和模 64
        gua_index = (number1 + number2) % 64
        
        # 獲取對應的卦象信息
        gua_info = YIJING_GUA[gua_index]
        
        return jsonify({
            'success': True,
            'number1': number1,
            'number2': number2,
            'gua_index': gua_index,
            'gua_name': gua_info['name'],
            'gua_description': gua_info['description'],
            'gua_interpretation': gua_info['interpretation']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/divination', methods=['POST'])
def divination():
    """一次性完成占卜：生成數字並解讀"""
    try:
        # 生成兩個隨機數字
        number1 = random.randint(1, 100)
        number2 = random.randint(1, 100)
        
        # 計算卦象索引
        gua_index = (number1 + number2) % 64
        gua_info = YIJING_GUA[gua_index]
        
        return jsonify({
            'success': True,
            'number1': number1,
            'number2': number2,
            'gua_index': gua_index,
            'gua_name': gua_info['name'],
            'gua_description': gua_info['description'],
            'gua_interpretation': gua_info['interpretation']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
