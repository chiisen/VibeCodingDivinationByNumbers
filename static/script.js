// DOM 元素引用
const startDivinationBtn = document.getElementById('start-divination');
const newDivinationBtn = document.getElementById('new-divination');
const retryDivinationBtn = document.getElementById('retry-divination');
const exportCardBtn = document.getElementById('export-card-btn');

exportCardBtn?.addEventListener('click', generateDivinationImage);

// 導出開運圖卡 (Canvas 繪製)
function generateDivinationImage() {
    const canvas = document.createElement('canvas');
    canvas.width = 600;
    canvas.height = 750;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 繪製玄墨背景
    ctx.fillStyle = '#111215';
    ctx.fillRect(0, 0, 600, 750);

    // 繪製古金雙邊框
    ctx.strokeStyle = '#d4af37';
    ctx.lineWidth = 2;
    ctx.strokeRect(20, 20, 560, 710);

    ctx.strokeStyle = 'rgba(212, 175, 55, 0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(26, 26, 548, 698);

    // 標題與印章
    ctx.fillStyle = '#d4af37';
    ctx.font = '22px "Noto Serif TC", serif';
    ctx.textAlign = 'center';
    ctx.fillText('周易靈數 ‧ 天人合一', 300, 65);

    // 卦符號
    const symbol = guaSymbolElement?.textContent || '䷀';
    ctx.font = '90px sans-serif';
    ctx.fillStyle = '#d4af37';
    ctx.fillText(symbol, 300, 180);

    // 卦名
    const guaName = guaNameElement?.textContent || '乾卦';
    ctx.font = 'bold 36px "Noto Serif TC", serif';
    ctx.fillStyle = '#f0eee9';
    ctx.fillText(guaName, 300, 240);

    // 動爻與之卦
    const movingText = document.getElementById('moving-yao-badge')?.textContent || '';
    const derivedName = document.getElementById('derived-gua-name')?.textContent || '';
    ctx.font = '18px "Noto Serif TC", serif';
    ctx.fillStyle = '#c83e3d';
    ctx.fillText(`${movingText} ➔ 之 ${derivedName}`, 300, 285);

    // 分隔線
    ctx.strokeStyle = 'rgba(212, 175, 55, 0.3)';
    ctx.beginPath();
    ctx.moveTo(80, 310);
    ctx.lineTo(520, 310);
    ctx.stroke();

    // 象傳內容
    ctx.fillStyle = '#f3e5ab';
    ctx.font = 'bold 18px "Noto Serif TC", serif';
    ctx.textAlign = 'left';
    ctx.fillText('📜 卦象大象傳：', 60, 350);

    ctx.fillStyle = '#c2c0b8';
    ctx.font = '16px "Noto Serif TC", serif';
    const descText = guaDescriptionElement?.textContent || '';
    wrapText(ctx, descText, 60, 385, 480, 26);

    // 占斷啟示
    ctx.fillStyle = '#c83e3d';
    ctx.font = 'bold 18px "Noto Serif TC", serif';
    ctx.fillText('💡 占斷啟示：', 60, 480);

    ctx.fillStyle = '#e6e4df';
    ctx.font = '16px "Noto Serif TC", serif';
    const interpText = guaInterpretationElement?.textContent || '';
    wrapText(ctx, interpText, 60, 515, 480, 26);

    // 頁尾落款
    ctx.textAlign = 'center';
    ctx.fillStyle = '#8c8980';
    ctx.font = '14px "Noto Serif TC", serif';
    ctx.fillText('易經數理占卜 ‧ 典藏靈符', 300, 690);

    // 下載圖片
    const link = document.createElement('a');
    link.download = `易經占卜_${guaName}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    let words = text.split('');
    let line = '';
    for (let n = 0; n < words.length; n++) {
        let testLine = line + words[n];
        let metrics = ctx.measureText(testLine);
        let testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            ctx.fillText(line, x, y);
            line = words[n];
            y += lineHeight;
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line, x, y);
}


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
    
    // 本卦
    if (guaNumberTagElement) guaNumberTagElement.textContent = `第 ${data.gua_index + 1} 卦`;
    if (guaSymbolElement) guaSymbolElement.textContent = data.gua_symbol || '☯';
    if (guaNameElement) guaNameElement.textContent = `${data.gua_name}卦`;
    
    // 動爻與之卦 (變卦)
    const movingYaoBadge = document.getElementById('moving-yao-badge');
    const derivedGuaSymbol = document.getElementById('derived-gua-symbol');
    const derivedGuaTag = document.getElementById('derived-gua-number-tag');
    const derivedGuaName = document.getElementById('derived-gua-name');
    
    if (movingYaoBadge) movingYaoBadge.textContent = `動爻：${data.moving_yao_name || '動爻'}`;
    if (derivedGuaSymbol) derivedGuaSymbol.textContent = data.derived_gua_symbol || '☯';
    if (derivedGuaTag) derivedGuaTag.textContent = `第 ${(data.derived_gua_index ?? 0) + 1} 卦`;
    if (derivedGuaName) derivedGuaName.textContent = `${data.derived_gua_name || '--'}卦`;
    
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
