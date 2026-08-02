// DOM 元素引用
const startDivinationBtn = document.getElementById('start-divination');
const newDivinationBtn = document.getElementById('new-divination');
const retryDivinationBtn = document.getElementById('retry-divination');

const welcomeCard = document.getElementById('welcome-card');
const resultCard = document.getElementById('result-card');
const loadingCard = document.getElementById('loading-card');
const errorCard = document.getElementById('error-card');

const number1Element = document.getElementById('number1');
const number2Element = document.getElementById('number2');
const guaModElement = document.getElementById('gua-index-display');
const guaSymbolElement = document.getElementById('gua-symbol');
const guaNumberTagElement = document.getElementById('gua-number-tag');
const guaNameElement = document.getElementById('gua-name');
const guaDescriptionElement = document.getElementById('gua-description');
const guaInterpretationElement = document.getElementById('gua-interpretation');
const errorMessageElement = document.getElementById('error-message');

// 事件監聽器
startDivinationBtn?.addEventListener('click', performDivination);
newDivinationBtn?.addEventListener('click', performDivination);
retryDivinationBtn?.addEventListener('click', performDivination);

// 鍵盤快捷鍵支援
document.addEventListener('keydown', function(e) {
    // 按 Space 鍵 (空白鍵) 開始或重新起卦
    if (e.code === 'Space' && !e.repeat && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        performDivination();
    }
    // 按 R 鍵重新起卦
    if ((e.code === 'KeyR' || e.key === 'r' || e.key === 'R') && !e.repeat) {
        performDivination();
    }
});

// 模式切換與 DOM 引用
const modeRandomBtn = document.getElementById('mode-random');
const modeCustomBtn = document.getElementById('mode-custom');
const customPanel = document.getElementById('custom-numbers-panel');
const customNum1Input = document.getElementById('custom-num1');
const customNum2Input = document.getElementById('custom-num2');

let currentMode = 'random'; // 'random' 或 'custom'

modeRandomBtn?.addEventListener('click', () => {
    currentMode = 'random';
    modeRandomBtn.classList.add('active');
    modeCustomBtn.classList.remove('active');
    customPanel.classList.add('hidden');
});

modeCustomBtn?.addEventListener('click', () => {
    currentMode = 'custom';
    modeCustomBtn.classList.add('active');
    modeRandomBtn.classList.remove('active');
    customPanel.classList.remove('hidden');
});

// 執行占卜的主要函數
async function performDivination() {
    try {
        let endpoint = '/divination';
        let options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        };

        if (currentMode === 'custom') {
            const num1 = parseInt(customNum1Input?.value || '0', 10);
            const num2 = parseInt(customNum2Input?.value || '0', 10);
            if (isNaN(num1) || num1 < 1 || num1 > 9999 || isNaN(num2) || num2 < 1 || num2 > 9999) {
                showError('請在自訂數字輸入 1 至 9999 之間的有效數字');
                return;
            }
            endpoint = '/interpret';
            options.body = JSON.stringify({ number1: num1, number2: num2 });
        }

        // 顯示載入狀態
        showLoading();
        
        // 延遲至少 800ms 以呈送籌策起卦之儀式感
        const minLoadingPromise = new Promise(resolve => setTimeout(resolve, 800));
        const fetchPromise = fetch(endpoint, options).then(res => res.json());

        const [_, data] = await Promise.all([minLoadingPromise, fetchPromise]);
        
        if (data.success) {
            displayResult(data);
        } else {
            showError(data.error || '起卦過程中發生未知錯誤');
        }
    } catch (error) {
        console.error('起卦請求失敗:', error);
        showError('網路連接失敗，請檢查網路狀態後重試');
    }
}


// 顯示載入狀態
function showLoading() {
    hideAllCards();
    loadingCard.classList.remove('hidden');
    loadingCard.classList.add('fade-in');
}

// 顯示結果
function displayResult(data) {
    // 更新 DOM 元素
    if (number1Element) number1Element.textContent = data.number1;
    if (number2Element) number2Element.textContent = data.number2;
    if (guaModElement) guaModElement.textContent = data.gua_index;
    
    // 卦號標籤
    if (guaNumberTagElement) guaNumberTagElement.textContent = `第 ${data.gua_index + 1} 卦`;
    
    // 易經 Unicode 六爻卦符號 (䷀~䷿)
    if (guaSymbolElement) {
        guaSymbolElement.textContent = data.gua_symbol || '☯';
    }
    
    if (guaNameElement) guaNameElement.textContent = `${data.gua_name}卦`;
    if (guaDescriptionElement) guaDescriptionElement.textContent = data.gua_description;
    if (guaInterpretationElement) guaInterpretationElement.textContent = data.gua_interpretation;
    
    // 顯示結果卡片
    hideAllCards();
    resultCard.classList.remove('hidden');
    resultCard.classList.add('fade-in');
    
    // 執行細緻的文字與數值浮出動畫
    animateResultElements();
}

// 顯示錯誤
function showError(message) {
    if (errorMessageElement) errorMessageElement.textContent = message;
    hideAllCards();
    errorCard.classList.remove('hidden');
    errorCard.classList.add('fade-in');
}

// 隱藏所有卡片
function hideAllCards() {
    welcomeCard?.classList.add('hidden');
    resultCard?.classList.add('hidden');
    loadingCard?.classList.add('hidden');
    errorCard?.classList.add('hidden');
    
    welcomeCard?.classList.remove('fade-in');
    resultCard?.classList.remove('fade-in');
    loadingCard?.classList.remove('fade-in');
    errorCard?.classList.remove('fade-in');
}

// 動態效果
function animateResultElements() {
    const symbol = document.getElementById('gua-symbol');
    if (symbol) {
        symbol.style.opacity = '0';
        symbol.style.transform = 'scale(0.7) rotate(-10deg)';
        
        setTimeout(() => {
            symbol.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            symbol.style.opacity = '1';
            symbol.style.transform = 'scale(1) rotate(0deg)';
        }, 100);
    }
}

// 頁面載入完成後的初始化淡入
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.container');
    if (container) {
        container.style.opacity = '0';
        container.style.transform = 'translateY(16px)';
        
        setTimeout(() => {
            container.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 80);
    }
});
