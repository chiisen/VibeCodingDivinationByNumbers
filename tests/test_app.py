import pytest
from app import (
    app,
    YIJING_GUA,
    YIJING_GUA_EN,
    APP_VERSION,
    calculate_moving_yaos,
    calculate_derived_index,
    judge_moving_yaos,
    build_divination_payload,
)

@pytest.fixture
def client():
    """建立 Flask 測試客戶端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """測試首頁 200 載入"""
    response = client.get('/')
    assert response.status_code == 200
    assert '易經數理占卜' in response.data.decode('utf-8')

def test_version_api(client):
    """測試版本號查詢 API"""
    response = client.get('/api/version')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['version'] == APP_VERSION
    assert 'git_commit' in data
    assert 'full_version' in data

def test_generate_numbers_api(client):
    """測試隨機數字生成 API"""
    response = client.get('/generate')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 1 <= data['number1'] <= 100
    assert 1 <= data['number2'] <= 100

def test_divination_api(client):
    """測試一次性起卦 API 與 64 卦對應邏輯"""
    response = client.post('/divination')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'number1' in data
    assert 'number2' in data
    
    # 驗證卦數模數邏輯: (num1 + num2) % 64
    expected_index = (data['number1'] + data['number2']) % 64
    assert data['gua_index'] == expected_index
    assert data['gua_name'] == YIJING_GUA[expected_index]['name']
    
    # 驗證易經 Unicode 六爻卦符 (䷀~䷿)
    assert 'gua_symbol' in data
    assert len(data['gua_symbol']) == 1
    assert ord(data['gua_symbol']) == (0x4DC0 + expected_index)
    
    # 驗證動爻與之卦 (變卦) 演算
    assert 'moving_yao_num' in data
    assert 1 <= data['moving_yao_num'] <= 6
    assert 'derived_gua_name' in data
    assert 'derived_gua_symbol' in data


def test_interpret_api_valid(client):
    """測試提供指定數字之卦象解讀 API"""
    payload = {'number1': 21, 'number2': 47}
    response = client.post('/interpret', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    
    expected_index = (21 + 47) % 64  # 68 % 64 = 4
    assert data['success'] is True
    assert data['gua_index'] == expected_index
    assert data['gua_name'] == YIJING_GUA[expected_index]['name']
    assert data['gua_symbol'] == chr(0x4DC0 + expected_index)

def test_interpret_api_missing_parameters(client):
    """測試缺少參數時之 HTTP 400 邊界錯誤處理"""
    # 缺少 number2 參數
    payload = {'number1': 10}
    response = client.post('/interpret', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "缺少 'number2' 參數" in data['error']

def test_interpret_api_invalid_types(client):
    """測試傳入非數字/無效字串時之 Fail-Fast 400 錯誤防護"""
    payload = {'number1': 'invalid_string', 'number2': 47}
    response = client.post('/interpret', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "'number1' 必須為有效整數" in data['error']

def test_interpret_api_out_of_range(client):
    """測試傳入超出範圍 1-9999 數字時之 HTTP 400 錯誤處理"""
    payload = {'number1': 0, 'number2': 50}
    response = client.post('/interpret', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "必須介於 1 至 9999 之間" in data['error']

def test_health_check_api(client):
    """測試健康檢查端點 /health"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'version' in data
    assert 'uptime_seconds' in data
    assert data['uptime_seconds'] >= 0

def test_index_has_restart_button(client):
    """測試結果面板具備明確的「↺ 重新起卦 (R)」視覺按鈕 (Issue #13)"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'id="restart-divination"' in html
    assert '重新起卦' in html

def test_script_binds_restart_button_and_hotkey(client):
    """測試 script.js 同時綁定重新起卦按鈕與 [ R ] 快捷鍵 (Issue #13)"""
    response = client.get('/static/script.js')
    assert response.status_code == 200
    js = response.data.decode('utf-8')
    assert "getElementById('restart-divination')" in js
    assert 'KeyR' in js

def test_calculate_moving_yaos_single_yao():
    """測試一爻變時，動爻位置仍由「上數」決定 (保持既有語意)"""
    assert calculate_moving_yaos(1, 1) == [1]
    assert calculate_moving_yaos(7, 1) == [1]
    assert calculate_moving_yaos(6, 1) == [6]

def test_calculate_moving_yaos_multiple_yaos():
    """測試「下數」決定動爻數量 (1-6 爻)，且位置不重複、均落於 1-6"""
    for number2 in range(1, 101):
        yaos = calculate_moving_yaos(21, number2)
        assert len(yaos) == (number2 - 1) % 6 + 1
        assert len(set(yaos)) == len(yaos)
        assert all(1 <= p <= 6 for p in yaos)

def test_calculate_derived_index_multi_yao():
    """測試以所有動爻之 XOR 位元遮罩演算之卦 (變卦)"""
    assert calculate_derived_index(4, [1]) == 5
    assert calculate_derived_index(0, [1, 2]) == 3
    assert calculate_derived_index(63, [1, 2, 3, 4, 5, 6]) == 0

def test_judge_moving_yaos_zhu_xi_rules():
    """測試朱熹《易學啟蒙》變占法則之判辭來源判定"""
    # 六爻皆靜
    assert judge_moving_yaos([], 4, 4)['judgment_rule'] == '六爻皆靜'
    # 一爻變：以本卦該動爻爻辭為占
    one = judge_moving_yaos([1], 4, 5)
    assert one['judgment_rule'] == '一爻變'
    assert one['judgment_primary'] == '本卦《需》初爻爻辭'
    assert one['judgment_secondary'] is None
    # 二爻變：以本卦兩動爻爻辭為占，以上爻為主
    two = judge_moving_yaos([1, 5], 4, 5)
    assert two['judgment_rule'] == '二爻變'
    assert two['judgment_primary'] == '本卦《需》五爻爻辭（主）'
    assert two['judgment_secondary'] == '本卦《需》初爻爻辭（輔）'
    # 三爻變：本卦為貞（主）、之卦為悔（輔）
    three = judge_moving_yaos([1, 2, 3], 4, 7)
    assert three['judgment_rule'] == '三爻變'
    assert three['judgment_primary'] == '本卦《需》卦辭（貞／主）'
    assert three['judgment_secondary'] == '之卦《比》卦辭（悔／輔）'
    # 四爻變：以之卦兩不變爻之爻辭為占，以下爻為主
    four = judge_moving_yaos([1, 2, 3, 4], 4, 7)
    assert four['judgment_rule'] == '四爻變'
    assert four['judgment_primary'] == '之卦《比》五爻爻辭（主）'
    assert four['judgment_secondary'] == '之卦《比》上爻爻辭（輔）'
    # 五爻變：以之卦唯一不變爻之爻辭為占
    five = judge_moving_yaos([1, 2, 3, 4, 5], 4, 7)
    assert five['judgment_rule'] == '五爻變'
    assert five['judgment_primary'] == '之卦《比》上爻爻辭'
    assert five['judgment_secondary'] is None
    # 六爻變：乾用九、坤用六，其餘以之卦卦辭為占
    assert '用九' in judge_moving_yaos([1, 2, 3, 4, 5, 6], 0, 63)['judgment_primary']
    assert '用六' in judge_moving_yaos([1, 2, 3, 4, 5, 6], 1, 62)['judgment_primary']
    assert judge_moving_yaos([1, 2, 3, 4, 5, 6], 4, 59)['judgment_primary'] == '之卦《節》卦辭'

def test_divination_api_multi_yao_payload(client):
    """測試起卦 API 回傳多爻變與朱熹變占判法欄位 (Issue #14)"""
    response = client.post('/divination')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

    assert isinstance(data['moving_yaos'], list)
    assert data['moving_yao_count'] == len(data['moving_yaos'])
    assert data['moving_yao_count'] == (data['number2'] - 1) % 6 + 1
    assert len(data['moving_yao_names']) == data['moving_yao_count']
    assert data['judgment_rule'] in (
        '一爻變', '二爻變', '三爻變', '四爻變', '五爻變', '六爻變'
    )
    assert data['judgment_text']
    assert data['judgment_primary']

    # 之卦須等於所有動爻 XOR 位元遮罩之演算結果
    expected_derived = calculate_derived_index(data['gua_index'], data['moving_yaos'])
    assert data['derived_gua_index'] == expected_derived
    assert data['derived_gua_name'] == YIJING_GUA[expected_derived]['name']

def test_index_has_judgment_panel(client):
    """測試結果面板具備「朱熹變占判法」呈現區塊 (Issue #14)"""
    html = client.get('/').data.decode('utf-8')
    assert 'id="judgment-rule"' in html
    assert 'id="judgment-primary"' in html
    assert '朱熹' in html

def test_index_has_sound_toggle(client):
    """測試 UI 右上角具備音效切換按鈕 (Issue #15)"""
    html = client.get('/').data.decode('utf-8')
    assert 'id="sound-toggle"' in html
    assert 'top-controls' in html

def test_script_persists_sound_state(client):
    """測試 script.js 以 LocalStorage 持久化音效狀態，並於靜音時不播放音效 (Issue #15)"""
    js = client.get('/static/script.js').data.decode('utf-8')
    assert "yijing_sound_enabled" in js
    assert "localStorage.setItem(SOUND_STORAGE_KEY" in js
    assert "localStorage.getItem(SOUND_STORAGE_KEY)" in js
    # 靜音時須提前返回，不建立 AudioContext
    assert 'if (!soundEnabled) return;' in js

def test_english_gua_database_completeness():
    """測試 64 卦英文對照資料庫完整且與中文資料索引一致 (Issue #16)"""
    assert len(YIJING_GUA) == 64
    assert len(YIJING_GUA_EN) == 64
    assert set(YIJING_GUA.keys()) == set(YIJING_GUA_EN.keys())
    for idx, info in YIJING_GUA_EN.items():
        for field in ('name', 'description', 'interpretation'):
            assert info[field].strip(), f"英文資料 index {idx} 缺少 {field}"
        assert info['name'] != YIJING_GUA[idx]['name']

def test_divination_payload_lang_en():
    """測試英文語系之完整回應內容 (Issue #16)"""
    payload = build_divination_payload(8, 5, lang='en')
    assert payload['lang'] == 'en'
    assert payload['gua_name'] == YIJING_GUA_EN[13]['name']
    assert payload['gua_description'] == YIJING_GUA_EN[13]['description']
    assert payload['gua_interpretation'] == YIJING_GUA_EN[13]['interpretation']
    assert payload['derived_gua_name'] == YIJING_GUA_EN[51]['name']
    assert payload['moving_yao_count'] == 5
    assert all('line' in name.lower() for name in payload['moving_yao_names'])
    assert payload['judgment_rule'] == 'Five moving lines'
    assert 'derived hexagram' in payload['judgment_primary']
    # 英文判辭來源須避免 "Second line line text" 疊字，並以分隔符連接 (Issue #16)
    assert 'line text' not in payload['judgment_primary']
    assert 'statement' in payload['judgment_primary']

def test_default_lang_is_traditional_chinese():
    """測試未指定語系時，維持繁體中文預設行為 (Issue #16)"""
    payload = build_divination_payload(8, 5)
    assert payload['lang'] == 'zh'
    assert payload['gua_name'] == YIJING_GUA[13]['name']
    assert payload['judgment_rule'] == '五爻變'

def test_interpret_api_lang_query(client):
    """測試 /interpret 支援 ?lang=en 查詢參數 (Issue #16)"""
    response = client.post('/interpret?lang=en', json={'number1': 21, 'number2': 47})
    assert response.status_code == 200
    data = response.get_json()
    assert data['lang'] == 'en'
    assert data['gua_index'] == 4
    assert data['gua_name'] == YIJING_GUA_EN[4]['name']

def test_interpret_api_lang_body(client):
    """測試 /interpret 支援 JSON body 指定 lang (Issue #16)"""
    response = client.post('/interpret', json={'number1': 21, 'number2': 47, 'lang': 'en'})
    assert response.status_code == 200
    assert response.get_json()['lang'] == 'en'

def test_divination_api_lang_en(client):
    """測試 /divination 支援英文語系 (Issue #16)"""
    response = client.post('/divination?lang=en')
    assert response.status_code == 200
    data = response.get_json()
    assert data['lang'] == 'en'
    assert data['gua_name'] == YIJING_GUA_EN[data['gua_index']]['name']
    assert data['derived_gua_name'] == YIJING_GUA_EN[data['derived_gua_index']]['name']

def test_invalid_lang_returns_400(client):
    """測試不支援語系之 Fail-Fast 400 錯誤處理 (Issue #16)"""
    response = client.post('/interpret', json={'number1': 21, 'number2': 47, 'lang': 'jp'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "'lang'" in data['error']

def test_index_has_language_toggle(client):
    """測試 UI 具備語系切換按鈕與 i18n 標記 (Issue #16)"""
    html = client.get('/').data.decode('utf-8')
    assert 'id="lang-toggle"' in html
    assert 'data-i18n="header.title"' in html

def test_script_has_i18n_dictionary(client):
    """測試 script.js 內含 i18n 字典、語系持久化與套用函式 (Issue #16)"""
    js = client.get('/static/script.js').data.decode('utf-8')
    assert 'yijing_lang' in js
    assert 'const I18N' in js
    assert 'applyLanguage' in js
    assert "'en'" in js

def test_script_sound_toggle_title_is_localized(client):
    """測試音效開關提示文字隨語系切換，不殘留硬編碼中文 (Issue #16)"""
    js = client.get('/static/script.js').data.decode('utf-8')
    assert "'sound.onTitle'" in js
    assert "'sound.offTitle'" in js
    assert "soundToggleBtn.title = soundEnabled ? t('sound.onTitle') : t('sound.offTitle');" in js




