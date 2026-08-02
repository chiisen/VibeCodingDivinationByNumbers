import pytest
from app import app, YIJING_GUA, APP_VERSION

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



