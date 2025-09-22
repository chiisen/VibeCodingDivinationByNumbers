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
const guaNameElement = document.getElementById('gua-name');
const guaDescriptionElement = document.getElementById('gua-description');
const guaInterpretationElement = document.getElementById('gua-interpretation');
const errorMessageElement = document.getElementById('error-message');

// 事件監聽器
startDivinationBtn.addEventListener('click', performDivination);
newDivinationBtn.addEventListener('click', performDivination);
retryDivinationBtn.addEventListener('click', performDivination);

// 執行占卜的主要函數
async function performDivination() {
    try {
        // 顯示載入狀態
        showLoading();
        
        // 發送請求到後端
        const response = await fetch('/divination', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            // 顯示結果
            displayResult(data);
        } else {
            // 顯示錯誤
            showError(data.error || '占卜過程中發生未知錯誤');
        }
    } catch (error) {
        console.error('占卜請求失敗:', error);
        showError('網路連接失敗，請檢查您的網路連接後重試');
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
    number1Element.textContent = data.number1;
    number2Element.textContent = data.number2;
    guaNameElement.textContent = data.gua_name;
    guaDescriptionElement.textContent = data.gua_description;
    guaInterpretationElement.textContent = data.gua_interpretation;
    
    // 顯示結果卡片
    hideAllCards();
    resultCard.classList.remove('hidden');
    resultCard.classList.add('fade-in');
    
    // 添加數字動畫效果
    animateNumbers();
}

// 顯示錯誤
function showError(message) {
    errorMessageElement.textContent = message;
    hideAllCards();
    errorCard.classList.remove('hidden');
    errorCard.classList.add('fade-in');
}

// 隱藏所有卡片
function hideAllCards() {
    welcomeCard.classList.add('hidden');
    resultCard.classList.add('hidden');
    loadingCard.classList.add('hidden');
    errorCard.classList.add('hidden');
    
    // 移除動畫類
    welcomeCard.classList.remove('fade-in');
    resultCard.classList.remove('fade-in');
    loadingCard.classList.remove('fade-in');
    errorCard.classList.remove('fade-in');
}

// 數字動畫效果
function animateNumbers() {
    const numbers = [number1Element, number2Element];
    
    numbers.forEach((element, index) => {
        // 重置數字
        element.style.opacity = '0';
        element.style.transform = 'scale(0.5)';
        
        // 延遲動畫
        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'scale(1)';
        }, index * 200);
    });
    
    // 卦名動畫
    setTimeout(() => {
        guaNameElement.style.transition = 'all 0.5s ease';
        guaNameElement.style.opacity = '0';
        guaNameElement.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            guaNameElement.style.opacity = '1';
            guaNameElement.style.transform = 'translateY(0)';
        }, 100);
    }, 400);
}

// 頁面載入完成後的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 添加頁面載入動畫
    const container = document.querySelector('.container');
    container.style.opacity = '0';
    container.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        container.style.transition = 'all 0.6s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 100);
    
    // 按鈕點擊效果
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = '';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
});

// 鍵盤快捷鍵支持
document.addEventListener('keydown', function(event) {
    // 按空格鍵或 Enter 鍵開始占卜
    if (event.code === 'Space' || event.code === 'Enter') {
        // 如果當前顯示的是歡迎卡片或錯誤卡片，則開始占卜
        if (!welcomeCard.classList.contains('hidden') || !errorCard.classList.contains('hidden')) {
            event.preventDefault();
            performDivination();
        }
    }
    
    // 按 R 鍵重新占卜
    if (event.code === 'KeyR' && !resultCard.classList.contains('hidden')) {
        performDivination();
    }
});

// 添加觸摸設備支持
if ('ontouchstart' in window) {
    // 為觸摸設備添加額外的樣式類
    document.body.classList.add('touch-device');
    
    // 優化觸摸體驗
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        card.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });
}
