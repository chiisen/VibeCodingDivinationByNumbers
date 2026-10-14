from flask import Flask, render_template, request, jsonify
import random
import json
import os
import subprocess
import time
import logging
from typing import Dict, Any, Tuple, Optional

# 配置結構化日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("yijing_app")

app = Flask(__name__)


APP_VERSION = "1.1.0"
START_TIME = time.time()

def validate_number_param(val: Any, param_name: str, min_val: int = 1, max_val: int = 9999) -> Tuple[Optional[int], Optional[str]]:
    """驗證與轉型數字參數，確保型別安全與 Fail-Fast 錯誤防護"""
    if val is None:
        return None, f"缺少 '{param_name}' 參數"
    try:
        num = int(val)
        if num < min_val or num > max_val:
            return None, f"'{param_name}' 必須介於 {min_val} 至 {max_val} 之間"
        return num, None
    except (ValueError, TypeError):
        return None, f"'{param_name}' 必須為有效整數"


def validate_lang_param(val: Any) -> Tuple[Optional[str], Optional[str]]:
    """驗證語系參數，僅支援 zh / en，未指定時預設繁體中文 (i18n, Issue #16)"""
    if val is None or val == '':
        return 'zh', None
    lang = str(val).lower()
    if lang not in SUPPORTED_LANGS:
        return None, f"'lang' 僅支援 {' / '.join(SUPPORTED_LANGS)}"
    return lang, None


def resolve_request_lang(data: Optional[Dict[str, Any]] = None) -> Tuple[Optional[str], Optional[str]]:
    """由查詢字串 (?lang=en) 或 JSON body 解析語系參數 (i18n, Issue #16)"""
    raw = request.args.get('lang')
    if raw is None and isinstance(data, dict):
        raw = data.get('lang')
    return validate_lang_param(raw)


def get_git_commit() -> Optional[str]:

    """獲取當前 Git short commit hash"""
    try:
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL)
        return commit.decode('utf-8').strip()
    except Exception:
        return None

def get_version_info():
    """獲取完整版本資訊"""
    commit = get_git_commit()
    if commit:
        return f"v{APP_VERSION} ({commit})"
    return f"v{APP_VERSION}"

@app.route('/')
def index():
    """首頁路由"""
    return render_template('index.html', version=get_version_info(), app_version=APP_VERSION, git_commit=get_git_commit())


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

# 易經六十四卦英文對照資料 (i18n, Issue #16)
YIJING_GUA_EN = {
    0: {"name": "Qian · The Creative", "description": "Heaven in its motion: the noble one strives ceaselessly", "interpretation": "Great fortune; advance with vigor; a good time to break new ground"},
    1: {"name": "Kun · The Receptive", "description": "The condition of the earth: the noble one carries all things with broad virtue", "interpretation": "Follow nature; overcome hardness with softness; steady development"},
    2: {"name": "Zhun · Difficulty at the Beginning", "description": "Clouds and thunder: the noble one brings order out of confusion", "interpretation": "Hardship at the beginning; patience and perseverance are needed"},
    3: {"name": "Meng · Youthful Folly", "description": "A spring below the mountain: the noble one nurtures virtue through resolute action", "interpretation": "A stage of learning; guidance and teaching are needed"},
    4: {"name": "Xu · Waiting", "description": "Clouds rise above heaven: the noble one feasts and takes joy", "interpretation": "Wait for the right moment; do not be impatient"},
    5: {"name": "Song · Conflict", "description": "Heaven and water move apart: the noble one plans carefully at the outset", "interpretation": "Avoid litigation; harmony is precious"},
    6: {"name": "Shi · The Army", "description": "Water within the earth: the noble one embraces and nurtures the people", "interpretation": "Unite as one; many wills make a strong city"},
    7: {"name": "Bi · Holding Together", "description": "Water upon the earth: the noble one builds alliances with the lords", "interpretation": "Draw close to others; build good relationships"},
    8: {"name": "Xiao Chu · Small Taming", "description": "Wind above heaven: the noble one cultivates refined virtue", "interpretation": "Small accumulations; advance steadily"},
    9: {"name": "Lu · Treading", "description": "Heaven above, the marsh below: the noble one distinguishes rank and settles the will of the people", "interpretation": "Act with care; observe propriety"},
    10: {"name": "Tai · Peace", "description": "Heaven and earth in union: the noble one completes the work of heaven and earth", "interpretation": "Great peace; all things prosper"},
    11: {"name": "Pi · Standstill", "description": "Heaven and earth do not meet: the noble one retreats in frugal virtue", "interpretation": "Unfavorable times; bide your time in concealment"},
    12: {"name": "Tong Ren · Fellowship with Men", "description": "Heaven with fire: the noble one distinguishes things by kind", "interpretation": "Unity and cooperation; like-minded companions"},
    13: {"name": "Da You · Possession in Great Measure", "description": "Fire above heaven: the noble one suppresses evil and promotes good", "interpretation": "Great gains; remain humble"},
    14: {"name": "Qian · Modesty", "description": "A mountain within the earth: the noble one reduces excess and augments the modest", "interpretation": "Modesty is beauty; keep a humble heart"},
    15: {"name": "Yu · Enthusiasm", "description": "Thunder comes forth from the earth: the noble one makes music and honors virtue", "interpretation": "A joyful mood; a time for celebration"},
    16: {"name": "Sui · Following", "description": "Thunder within the marsh: the noble one rests when night falls", "interpretation": "Follow nature; move with the times"},
    17: {"name": "Gu · Work on the Decayed", "description": "Wind below the mountain: the noble one stirs the people and nurtures virtue", "interpretation": "Sweep away the old; reform and renew"},
    18: {"name": "Lin · Approach", "description": "Earth above the marsh: the noble one teaches with tireless thought", "interpretation": "Facing a challenge; wisdom is required"},
    19: {"name": "Guan · Contemplation", "description": "Wind over the earth: the noble one surveys the realm and sets up teaching", "interpretation": "Observe and reflect; learn and grow"},
    20: {"name": "Shi He · Biting Through", "description": "Thunder and lightning: the former kings clarified punishments and statutes", "interpretation": "Overcome difficulties; decisiveness is needed"},
    21: {"name": "Bi · Grace", "description": "Fire below the mountain: the noble one illuminates governance, daring not to judge", "interpretation": "Adornment and refinement; attend to appearances"},
    22: {"name": "Bo · Splitting Apart", "description": "The mountain rests upon the earth: the noble one secures the foundation", "interpretation": "Gradual decline; be cautious"},
    23: {"name": "Fu · Return", "description": "Thunder within the earth: the noble one closes the passes at the solstice", "interpretation": "Begin anew; the cycle returns"},
    24: {"name": "Wu Wang · Innocence", "description": "Thunder moves under heaven: the former kings nurtured all things in season", "interpretation": "Truthful and uncontrived; act naturally"},
    25: {"name": "Da Xu · The Taming Power of the Great", "description": "Heaven within the mountain: the noble one learns the words and deeds of the past", "interpretation": "Great accumulation; store up wisdom"},
    26: {"name": "Yi · The Corners of the Mouth", "description": "Thunder below the mountain: the noble one is careful in speech and temperate in eating", "interpretation": "Cultivate body and mind; restrain desire"},
    27: {"name": "Da Guo · Preponderance of the Great", "description": "The marsh submerges the wood: the noble one stands alone without fear", "interpretation": "Excess in action; adjustment is needed"},
    28: {"name": "Kan · The Abysmal Water", "description": "Water flows on and on: the noble one practices constancy of virtue", "interpretation": "Repeated hardship; perseverance is required"},
    29: {"name": "Li · The Clinging Fire", "description": "Brightness doubled: the noble one continues the light over the four quarters", "interpretation": "Brightness shines; wisdom is awakened"},
    30: {"name": "Xian · Influence", "description": "A marsh on the mountain: the noble one receives others with emptiness", "interpretation": "Mutual response; hearts in accord"},
    31: {"name": "Heng · Duration", "description": "Thunder and wind: the noble one stands firm and does not change direction", "interpretation": "Enduring constancy; persevere"},
    32: {"name": "Dun · Retreat", "description": "Heaven above the mountain: the noble one keeps distance from the petty without rancor", "interpretation": "Withdraw and yield; stay clear of the petty"},
    33: {"name": "Da Zhuang · The Power of the Great", "description": "Thunder above heaven: the noble one does not tread what is not proper", "interpretation": "Great strength, but propriety must be kept"},
    34: {"name": "Jin · Progress", "description": "The sun rises above the earth: the noble one makes bright his virtue", "interpretation": "Advance and develop; open and upright"},
    35: {"name": "Ming Yi · Darkening of the Light", "description": "Light enters the earth: the noble one governs the people by veiling his brightness", "interpretation": "The light is wounded; conceal your brilliance"},
    36: {"name": "Jia Ren · The Family", "description": "Wind comes forth from fire: the noble one speaks with substance and acts with constancy", "interpretation": "Domestic harmony; words and deeds as one"},
    37: {"name": "Kui · Opposition", "description": "Fire above, the marsh below: the noble one unites through difference", "interpretation": "Divergent views; reconciliation is needed"},
    38: {"name": "Jian · Obstruction", "description": "Water on the mountain: the noble one turns inward and cultivates virtue", "interpretation": "The road is hard; self-examination is needed"},
    39: {"name": "Jie · Deliverance", "description": "Thunder and rain: the noble one pardons faults and forgives offenses", "interpretation": "Difficulties dissolve; forgive and embrace"},
    40: {"name": "Sun · Decrease", "description": "A marsh below the mountain: the noble one curbs anger and restrains desire", "interpretation": "Reduce losses; master the emotions"},
    41: {"name": "Yi · Increase", "description": "Wind and thunder: the noble one moves toward good and corrects faults", "interpretation": "Growth and gain; reform your faults"},
    42: {"name": "Guai · Breakthrough", "description": "The marsh rises to heaven: the noble one bestows favors below", "interpretation": "Resolute decision, yet with caution"},
    43: {"name": "Gou · Coming to Meet", "description": "Wind under heaven: the noble one proclaims commands to the four quarters", "interpretation": "An encounter of chance; choose wisely"},
    44: {"name": "Cui · Gathering Together", "description": "A marsh over the earth: the noble one prepares weapons and guards against the unforeseen", "interpretation": "Gather strength; prepare for the unexpected"},
    45: {"name": "Sheng · Pushing Upward", "description": "Wood grows within the earth: the noble one accumulates the small to reach the high", "interpretation": "Rise and develop; advance step by step"},
    46: {"name": "Kun · Oppression", "description": "The marsh has no water: the noble one stakes his life on his will", "interpretation": "Hardship and want; hold fast to your aim"},
    47: {"name": "Jing · The Well", "description": "Water above wood: the noble one labors for the people and encourages mutual aid", "interpretation": "The well never runs dry; joy in helping others"},
    48: {"name": "Ge · Revolution", "description": "Fire within the marsh: the noble one orders the calendar and clarifies the seasons", "interpretation": "Transform and renew; follow the times"},
    49: {"name": "Ding · The Cauldron", "description": "Fire above wood: the noble one steadies his place and consolidates his mandate", "interpretation": "Steadiness and weight; hold your position"},
    50: {"name": "Zhen · The Arousing Thunder", "description": "Thunder repeated: the noble one examines himself in fear and trembling", "interpretation": "Thunder shakes; awaken and reflect"},
    51: {"name": "Gen · Keeping Still, Mountain", "description": "Mountains joined: the noble one does not let his thoughts stray from his place", "interpretation": "Be still; keep to your own place"},
    52: {"name": "Jian · Development", "description": "Wood on the mountain: the noble one dwells in virtue and improves custom", "interpretation": "Advance gradually; cultivate character"},
    53: {"name": "Gui Mei · The Marrying Maiden", "description": "Thunder over the marsh: the noble one knows the decay of endings", "interpretation": "A question of belonging; be cautious"},
    54: {"name": "Feng · Abundance", "description": "Thunder and lightning both arrive: the noble one decides cases and carries out punishments", "interpretation": "Abundance and wealth, but justice is needed"},
    55: {"name": "Lu · The Wanderer", "description": "Fire on the mountain: the noble one is clear and careful in punishment", "interpretation": "Adrift and unsettled; be cautious"},
    56: {"name": "Xun · The Gentle Wind", "description": "Wind following wind: the noble one spreads commands and carries out affairs", "interpretation": "Move with the wind; carry out your orders"},
    57: {"name": "Dui · The Joyous Lake", "description": "Joined marshes: the noble one joins friends in discussion and practice", "interpretation": "Joyful exchange; learning and progress"},
    58: {"name": "Huan · Dispersion", "description": "Wind over water: the noble one offers sacrifice to the Lord and establishes temples", "interpretation": "Scattering and dispersal; unity is needed"},
    59: {"name": "Jie · Limitation", "description": "Water above the marsh: the noble one sets measure and discusses virtue", "interpretation": "Restraint and moderation; proceed in due measure"},
    60: {"name": "Zhong Fu · Inner Truth", "description": "Wind over the marsh: the noble one deliberates on cases and delays execution", "interpretation": "Sincerity and centeredness; forgive and embrace"},
    61: {"name": "Xiao Guo · Preponderance of the Small", "description": "Thunder on the mountain: the noble one exceeds in reverence", "interpretation": "Small faults; be cautious"},
    62: {"name": "Ji Ji · After Completion", "description": "Water above fire: the noble one thinks of calamity and guards against it", "interpretation": "The work is done; guard against trouble"},
    63: {"name": "Wei Ji · Before Completion", "description": "Fire above water: the noble one carefully distinguishes things and places them", "interpretation": "The work is not yet done; keep striving"}
}

# 支援語系 (i18n, Issue #16)
SUPPORTED_LANGS = ('zh', 'en')

YAO_NAMES_EN = ['Initial line', 'Second line', 'Third line', 'Fourth line', 'Fifth line', 'Top line']


def get_gua_info(gua_index: int, lang: str = 'zh') -> Dict[str, str]:
    """依語系取得卦象資料 (支援 zh / en)"""
    return (YIJING_GUA_EN if lang == 'en' else YIJING_GUA)[gua_index]



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

YAO_NAMES = ['初爻', '二爻', '三爻', '四爻', '五爻', '上爻']

# 朱熹《易學啟蒙》變占法則：依動爻數量判定主要判辭來源
# 每項為 (中文法則名, 中文判辭說明, English rule name, English rule text)
JUDGMENT_RULES: Dict[int, Tuple[str, str, str, str]] = {
    0: ("六爻皆靜", "以本卦卦辭為占",
        "All lines still", "Judge by the Judgment of the primary hexagram"),
    1: ("一爻變", "以本卦該動爻之爻辭為占",
        "One moving line", "Judge by the line text of that moving line in the primary hexagram"),
    2: ("二爻變", "以本卦兩動爻之爻辭為占，以上爻為主",
        "Two moving lines", "Judge by the two moving lines of the primary hexagram, the upper one governing"),
    3: ("三爻變", "以本卦與之卦卦辭合占，以本卦為貞（主）、之卦為悔（輔）",
        "Three moving lines", "Judge by both Judgments: the primary hexagram as zhen (leading), the derived as hui (supporting)"),
    4: ("四爻變", "以之卦中兩不變爻之爻辭為占，以下爻為主",
        "Four moving lines", "Judge by the two unmoved lines of the derived hexagram, the lower one governing"),
    5: ("五爻變", "以之卦中唯一不變爻之爻辭為占",
        "Five moving lines", "Judge by the single unmoved line of the derived hexagram"),
    6: ("六爻變", "乾卦以用九、坤卦以用六為占，其餘以之卦卦辭為占",
        "Six moving lines", "For Qian use Nine, for Kun use Six; otherwise judge by the Judgment of the derived hexagram"),
}


def calculate_moving_yaos(number1: int, number2: int) -> list:
    """推演動爻位置集合 (1-6)：上數定首動爻，下數定動爻數量 (1-6 爻)"""
    count = (number2 - 1) % 6 + 1
    start_idx = (number1 - 1) % 6
    return sorted({(start_idx + i) % 6 + 1 for i in range(count)})


def calculate_derived_index(gua_index: int, moving_yaos) -> int:
    """以所有動爻之 XOR 位元遮罩演算之卦 (變卦) 索引"""
    mask = 0
    for position in moving_yaos:
        mask |= 1 << (int(position) - 1)
    return gua_index ^ mask


def judge_moving_yaos(moving_yaos, gua_index: int, derived_index: int, lang: str = 'zh') -> Dict[str, Any]:
    """依朱熹《易學啟蒙》變占法則，判定本次占卜之主要判辭依據 (支援 zh / en)"""
    positions = sorted({int(p) for p in moving_yaos})
    count = len(positions)
    if count not in JUDGMENT_RULES:
        raise ValueError(f"動爻數量必須介於 0 至 6 之間，收到 {count}")

    is_en = (lang == 'en')
    rule = JUDGMENT_RULES[count]
    rule_name, rule_text = (rule[2], rule[3]) if is_en else (rule[0], rule[1])

    gua_name = get_gua_info(gua_index, lang)['name']
    derived_name = get_gua_info(derived_index, lang)['name']
    yao_names = YAO_NAMES_EN if is_en else YAO_NAMES

    if is_en:
        primary_ref = f'primary hexagram "{gua_name}"'
        derived_ref = f'derived hexagram "{derived_name}"'
        judgment_word = ' · Judgment'
        main_tag, aux_tag = ' (governing)', ' (supporting)'
        zhen_tag, hui_tag = ' (zhen / leading)', ' (hui / supporting)'
    else:
        primary_ref = f"本卦《{gua_name}》"
        derived_ref = f"之卦《{derived_name}》"
        judgment_word = '卦辭'
        main_tag, aux_tag = '（主）', '（輔）'
        zhen_tag, hui_tag = '（貞／主）', '（悔／輔）'

    def line_ref(position: int) -> str:
        return f' · {yao_names[position - 1]} statement' if is_en else f'{yao_names[position - 1]}爻辭'

    primary_source: Optional[str] = None
    secondary_source: Optional[str] = None

    if count == 0:
        primary_source = f"{primary_ref}{judgment_word}"
    elif count == 1:
        primary_source = f"{primary_ref}{line_ref(positions[0])}"
    elif count == 2:
        primary_source = f"{primary_ref}{line_ref(positions[-1])}{main_tag}"
        secondary_source = f"{primary_ref}{line_ref(positions[-2])}{aux_tag}"
    elif count == 3:
        primary_source = f"{primary_ref}{judgment_word}{zhen_tag}"
        secondary_source = f"{derived_ref}{judgment_word}{hui_tag}"
    elif count == 4:
        unchanged = [p for p in range(1, 7) if p not in positions]
        primary_source = f"{derived_ref}{line_ref(unchanged[0])}{main_tag}"
        secondary_source = f"{derived_ref}{line_ref(unchanged[1])}{aux_tag}"
    elif count == 5:
        unchanged = [p for p in range(1, 7) if p not in positions]
        primary_source = f"{derived_ref}{line_ref(unchanged[0])}"
    else:
        if gua_index == 0:
            primary_source = ('Qian: Use Nine — "There appears a flight of dragons without heads. Good fortune."'
                              if is_en else '乾卦 用九：「見群龍無首，吉」')
        elif gua_index == 1:
            primary_source = ('Kun: Use Six — "Favorable to be steadfast forever."'
                              if is_en else '坤卦 用六：「利永貞」')
        else:
            primary_source = f"{derived_ref}{judgment_word}"

    return {
        'moving_count': count,
        'judgment_rule': rule_name,
        'judgment_text': rule_text,
        'judgment_primary': primary_source,
        'judgment_secondary': secondary_source,
    }


def build_divination_payload(number1: int, number2: int, lang: str = 'zh') -> Dict[str, Any]:
    """依兩數建構完整卦象回應資料 (本卦 ➔ 多爻變 ➔ 之卦 ➔ 變占判法，支援 zh / en)"""
    gua_index = (number1 + number2) % 64
    gua_info = get_gua_info(gua_index, lang)

    moving_yaos = calculate_moving_yaos(number1, number2)
    derived_index = calculate_derived_index(gua_index, moving_yaos)
    derived_info = get_gua_info(derived_index, lang)
    judgment = judge_moving_yaos(moving_yaos, gua_index, derived_index, lang)
    yao_names = YAO_NAMES_EN if lang == 'en' else YAO_NAMES

    return {
        'success': True,
        'lang': lang,
        'number1': number1,
        'number2': number2,
        'gua_index': gua_index,
        'gua_name': gua_info['name'],
        'gua_symbol': chr(0x4DC0 + gua_index),
        'gua_description': gua_info['description'],
        'gua_interpretation': gua_info['interpretation'],
        'moving_yao_num': moving_yaos[0],
        'moving_yao_name': yao_names[moving_yaos[0] - 1],
        'moving_yaos': moving_yaos,
        'moving_yao_names': [yao_names[p - 1] for p in moving_yaos],
        'moving_yao_count': len(moving_yaos),
        'judgment_rule': judgment['judgment_rule'],
        'judgment_text': judgment['judgment_text'],
        'judgment_primary': judgment['judgment_primary'],
        'judgment_secondary': judgment['judgment_secondary'],
        'derived_gua_index': derived_index,
        'derived_gua_name': derived_info['name'],
        'derived_gua_symbol': chr(0x4DC0 + derived_index),
    }


@app.route('/interpret', methods=['POST'])
def interpret_numbers():
    """根據兩個數字進行易經解讀 (含本卦、多爻變與之卦演算，支援 zh / en)"""
    try:
        data = request.get_json() or {}
        raw1 = data.get('number1')
        raw2 = data.get('number2')

        lang, lang_err = resolve_request_lang(data)
        if lang_err:
            return jsonify({'success': False, 'error': lang_err}), 400

        num1, err1 = validate_number_param(raw1, 'number1')
        if err1:
            return jsonify({'success': False, 'error': err1}), 400

        num2, err2 = validate_number_param(raw2, 'number2')
        if err2:
            return jsonify({'success': False, 'error': err2}), 400

        return jsonify(build_divination_payload(num1, num2, lang))
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/divination', methods=['POST'])
def divination():
    """一次性完成占卜：生成數字並解讀 (含本卦、多爻變與之卦，支援 zh / en)"""
    try:
        data = request.get_json(silent=True) or {}

        lang, lang_err = resolve_request_lang(data)
        if lang_err:
            return jsonify({'success': False, 'error': lang_err}), 400

        number1 = random.randint(1, 100)
        number2 = random.randint(1, 100)

        return jsonify(build_divination_payload(number1, number2, lang))
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/version', methods=['GET'])
def get_version():
    """獲取版本號與 Git commit 資訊"""
    return jsonify({
        'success': True,
        'version': APP_VERSION,
        'git_commit': get_git_commit(),
        'full_version': get_version_info()
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點，提供系統存活狀態與運作指標"""
    uptime_seconds = round(time.time() - START_TIME, 2)
    return jsonify({
        'status': 'ok',
        'version': APP_VERSION,
        'git_commit': get_git_commit(),
        'uptime_seconds': uptime_seconds
    })


import socket


def find_available_port(start_port=5001, max_tries=50):
    """取得可用的通訊埠：預設優先嘗試 5001，若被佔用則順延尋找 5002, 5003..."""
    for p in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', p))
                return p
            except OSError:
                continue
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

if __name__ == '__main__':
    env_port = os.environ.get('PORT')
    if env_port and env_port.isdigit():
        port = int(env_port)
    else:
        # 優先嘗試使用 5001，若佔用則自動順延尋找空閒 Port
        port = find_available_port(5001)

    print(f"\nServer starting on: http://127.0.0.1:{port}\n")
    app.run(debug=True, host='0.0.0.0', port=port)



