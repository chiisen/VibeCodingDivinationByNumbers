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
    ctx.fillText(t('export.title'), 300, 65);

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
    const derivedConnector = currentLang === 'en' ? '➔ ' : '➔ 之 ';
    ctx.fillText(`${movingText} ${derivedConnector}${derivedName}`, 300, 285);

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
    ctx.fillText(t('export.imageLabel'), 60, 350);

    ctx.fillStyle = '#c2c0b8';
    ctx.font = '16px "Noto Serif TC", serif';
    const descText = guaDescriptionElement?.textContent || '';
    wrapText(ctx, descText, 60, 385, 480, 26);

    // 占斷啟示
    ctx.fillStyle = '#c83e3d';
    ctx.font = 'bold 18px "Noto Serif TC", serif';
    ctx.fillText(t('export.interpLabel'), 60, 480);

    ctx.fillStyle = '#e6e4df';
    ctx.font = '16px "Noto Serif TC", serif';
    const interpText = guaInterpretationElement?.textContent || '';
    wrapText(ctx, interpText, 60, 515, 480, 26);

    // 頁尾落款
    ctx.textAlign = 'center';
    ctx.fillStyle = '#8c8980';
    ctx.font = '14px "Noto Serif TC", serif';
    ctx.fillText(t('export.footer'), 300, 690);

    // 下載圖片
    const link = document.createElement('a');
    link.download = `${t('export.filenamePrefix')}_${guaName}.png`;
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

// 結果面板之「↺ 重新起卦 (R)」視覺按鈕 (Issue #13)
const restartDivinationBtn = document.getElementById('restart-divination');
restartDivinationBtn?.addEventListener('click', performDivination);

// 鍵盤快捷鍵支援
document.addEventListener('keydown', function(e) {
    const isTyping = document.activeElement && document.activeElement.tagName === 'INPUT';
    // 按 Space 鍵 (空白鍵) 開始或重新起卦
    if (e.code === 'Space' && !e.repeat && !isTyping) {
        e.preventDefault();
        performDivination();
    }
    // 按 R 鍵重新起卦 (與「↺ 重新起卦 (R)」按鈕行為一致)
    if ((e.code === 'KeyR' || e.key === 'r' || e.key === 'R') && !e.repeat && !isTyping) {
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

// ===== 國際化 i18n (Issue #16) =====
const LANG_STORAGE_KEY = 'yijing_lang';

// 目前顯示中的數字，供切換語系時以相同數字重新解讀
let lastResultNumbers = null;

const I18N = {
    zh: {
        'doc.title': '易經數理占卜 | 探索天人合一之智慧',
        'header.badge': '周易靈數 ‧ 誠心求卦',
        'header.title': '易經數理占卜',
        'header.subtitle': '數由心生 ‧ 卦由數成 ‧ 探索天人合一之智慧',
        'welcome.title': '起卦儀式',
        'welcome.intro': '易有太極，是生兩儀。請平心靜氣，默想心中所求之事。<br>點擊下方起卦按鈕，系統將感應數列，為您求得天地相對應之六十四卦大象。',
        'mode.random': '🎲 隨機天成',
        'mode.custom': '✍️ 心感自訂數',
        'form.upperLabel': '上數 (1-9999)',
        'form.lowerLabel': '下數 (1-9999)',
        'form.upperPlaceholder': '例如: 8',
        'form.lowerPlaceholder': '例如: 21',
        'action.start': '誠心起卦',
        'action.startHotkey': '快捷鍵：按下 [ Space 空白鍵 ] 開始',
        'action.restart': '重新起卦 (R)',
        'action.restartHotkey': '亦可直接按下 [ R ] 鍵重新起卦',
        'result.tag': '卦象占斷',
        'result.title': '天人相應 ‧ 卦象顯現',
        'result.copy': '📋 複製卦辭',
        'result.export': '🖼️ 導出圖卡',
        'result.again': '↺ 再求一卦',
        'numbers.upper': '上數 (天爻)',
        'numbers.lower': '下數 (地爻)',
        'numbers.modulo': '求模演卦',
        'gua.primaryTag': '本卦 (主象)',
        'gua.derivedTag': '之卦 (變象)',
        'gua.judgmentHeader': '朱熹變占判法',
        'gua.imageHeader': '卦象大象傳',
        'gua.interpretationHeader': '占斷啟示',
        'gua.primaryLabel': '主解：',
        'gua.secondaryLabel': '輔解：',
        'loading.text': '籌策演算中 ‧ 靜心聽卦...',
        'loading.subtext': '太極動而生陽，動極而靜，靜而生陰',
        'error.title': '起卦中斷',
        'error.defaultMessage': '網絡或感應發生異常，請重試。',
        'error.retry': '重新感應',
        'error.invalidCustom': '請在自訂數字輸入 1 至 9999 之間的有效數字',
        'error.network': '網路連接失敗，請檢查網路狀態後重試',
        'error.unknown': '起卦過程中發生未知錯誤',
        'info.title': '☯ 關於數理易經占卜',
        'info.body': '《易經·繫辭上》曰：「大衍之數五十，其用四十有九... 參伍以變，錯綜其數。」易經數理占卜乃藉由隨機生成的數理總和對應易經六十四卦，反映當下心境與吉凶消長之機。',
        'info.disclaimer': '<strong>註：</strong>本系統基於中華傳統經典易經文化設計，旨在啟迪思維與修養身心，請理性參考。',
        'history.title': '歷次起卦紀錄',
        'history.clear': '清空紀錄',
        'history.empty': '尚無起卦歷史紀錄',
        'footer.copyright': '© 2026 易經數理占卜 ‧ 傳承經典文化',
        'copy.header': '【易經數理占卜 ‧ 靈符卦象】',
        'copy.primary': '本卦：',
        'copy.derived': '之卦：',
        'export.title': '周易靈數 ‧ 天人合一',
        'export.footer': '易經數理占卜 ‧ 典藏靈符',
        'export.imageLabel': '📜 卦象大象傳：',
        'export.interpLabel': '💡 占斷啟示：',
        'export.filenamePrefix': '易經占卜',
        'sound.onTitle': '音效已開啟（點擊靜音）',
        'sound.offTitle': '音效已靜音（點擊開啟）'
    },
    en: {
        'doc.title': 'I Ching Numerology | The Wisdom of Heaven and Humanity as One',
        'header.badge': 'Zhouyi Numerology · A Sincere Inquiry',
        'header.title': 'I Ching Numerology Divination',
        'header.subtitle': 'Numbers arise from the heart · Hexagrams form from numbers · Explore the wisdom of Heaven and Humanity as one',
        'welcome.title': 'The Ritual of Casting',
        'welcome.intro': 'There is Taiji, which gives rise to the two modes. Calm your mind and hold your question quietly.<br>Click the button below to cast; the system will sense the numbers and reveal the hexagram of Heaven and Earth.',
        'mode.random': '🎲 Random Cast',
        'mode.custom': '✍️ Custom Numbers',
        'form.upperLabel': 'Upper number (1-9999)',
        'form.lowerLabel': 'Lower number (1-9999)',
        'form.upperPlaceholder': 'e.g. 8',
        'form.lowerPlaceholder': 'e.g. 21',
        'action.start': 'Cast the Hexagram',
        'action.startHotkey': 'Hotkey: press [ Space ] to begin',
        'action.restart': 'Cast Again (R)',
        'action.restartHotkey': 'You may also press [ R ] to cast again',
        'result.tag': 'Hexagram Reading',
        'result.title': 'Heaven and Humanity Respond · The Hexagram Appears',
        'result.copy': '📋 Copy Text',
        'result.export': '🖼️ Export Image',
        'result.again': '↺ Ask Again',
        'numbers.upper': 'Upper (Heaven)',
        'numbers.lower': 'Lower (Earth)',
        'numbers.modulo': 'Modulo',
        'gua.primaryTag': 'Primary Hexagram',
        'gua.derivedTag': 'Derived Hexagram',
        'gua.judgmentHeader': "Zhu Xi's Changing-Line Rule",
        'gua.imageHeader': 'The Image (Da Xiang)',
        'gua.interpretationHeader': 'Interpretation',
        'gua.primaryLabel': 'Primary: ',
        'gua.secondaryLabel': 'Supporting: ',
        'loading.text': 'Casting the stalks · Listen quietly...',
        'loading.subtext': 'The Taiji moves and yang is born; at the extreme of motion comes stillness, and yin is born',
        'error.title': 'Casting Interrupted',
        'error.defaultMessage': 'A network or sensing error occurred. Please try again.',
        'error.retry': 'Try Again',
        'error.invalidCustom': 'Please enter valid numbers between 1 and 9999',
        'error.network': 'Network request failed. Please check your connection and try again.',
        'error.unknown': 'An unknown error occurred while casting',
        'info.title': '☯ About I Ching Numerology',
        'info.body': 'The Great Treatise says: "The number of the Great Expansion is fifty, of which forty-nine are used... Three and five are used for change, and the numbers are interlaced." I Ching numerology maps the sum of randomly generated numbers to the sixty-four hexagrams, reflecting the mood of the moment and the rise and fall of fortune.',
        'info.disclaimer': '<strong>Note:</strong> This system is designed around traditional Chinese I Ching culture. It aims to inspire reflection and to cultivate body and mind; please consult it with reason.',
        'history.title': 'Divination History',
        'history.clear': 'Clear',
        'history.empty': 'No divination history yet',
        'footer.copyright': '© 2026 I Ching Numerology · Preserving Classic Culture',
        'copy.header': '【I Ching Numerology · Hexagram】',
        'copy.primary': 'Primary hexagram: ',
        'copy.derived': 'Derived hexagram: ',
        'export.title': 'Zhouyi Numerology · Heaven and Humanity as One',
        'export.footer': 'I Ching Numerology · Treasured Talisman',
        'export.imageLabel': '📜 The Image:',
        'export.interpLabel': '💡 Interpretation:',
        'export.filenamePrefix': 'IChing',
        'sound.onTitle': 'Sound on (click to mute)',
        'sound.offTitle': 'Sound muted (click to enable)'
    }
};

let currentLang = 'zh';
try {
    const storedLang = localStorage.getItem(LANG_STORAGE_KEY);
    if (storedLang === 'en' || storedLang === 'zh') currentLang = storedLang;
} catch (e) {
    console.log('讀取語系設定失敗:', e);
}

// 依當前語系取得翻譯文字
function t(key) {
    const table = I18N[currentLang] || I18N.zh;
    return table[key] || I18N.zh[key] || key;
}

// 套用靜態元素之 i18n 標記
function applyStaticTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const value = t(el.getAttribute('data-i18n'));
        if (value) el.textContent = value;
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
        const value = t(el.getAttribute('data-i18n-html'));
        if (value) el.innerHTML = value;
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const value = t(el.getAttribute('data-i18n-placeholder'));
        if (value) el.setAttribute('placeholder', value);
    });
}

// 卦序標籤：第 N 卦 / Hexagram N
function formatHexagramNumber(guaIndex) {
    const n = (guaIndex ?? 0) + 1;
    return currentLang === 'en' ? `Hexagram ${n}` : `第 ${n} 卦`;
}

// 卦名標籤：乾卦 / Qian · The Creative
function formatGuaName(guaName) {
    if (!guaName) return '--';
    return currentLang === 'en' ? guaName : `${guaName}卦`;
}

// 動爻標籤 (支援多爻變)
function formatMovingLabel(movingNames, movingCount) {
    const names = movingNames.length ? movingNames : [''];
    if (currentLang === 'en') {
        const joined = names.join(', ');
        return movingCount > 1
            ? `Moving lines: ${joined} (${movingCount} moving lines)`
            : `Moving lines: ${joined}`;
    }
    const joined = names.join('、');
    return movingCount > 1
        ? `動爻：${joined}（${movingCount} 爻變）`
        : `動爻：${joined}`;
}

const langToggleBtn = document.getElementById('lang-toggle');

function applyLanguage(lang, options = {}) {
    currentLang = (lang === 'en') ? 'en' : 'zh';
    try {
        localStorage.setItem(LANG_STORAGE_KEY, currentLang);
    } catch (e) {
        console.log('儲存語系設定失敗:', e);
    }
    document.documentElement.lang = currentLang === 'en' ? 'en' : 'zh-TW';
    document.title = t('doc.title');
    if (langToggleBtn) {
        langToggleBtn.textContent = currentLang === 'en' ? '中' : 'EN';
        langToggleBtn.title = currentLang === 'en' ? '切換語系 / Switch language' : 'Switch language / 切換語系';
    }
    applyStaticTranslations();
    applySoundState();
    renderHistory();
    if (options.refreshResult) refreshResultLanguage();
}

langToggleBtn?.addEventListener('click', () => {
    applyLanguage(currentLang === 'en' ? 'zh' : 'en', { refreshResult: true });
});

// 切換語系後，以相同數字重新取得該語系之卦象內容 (不重複寫入歷史紀錄)
async function refreshResultLanguage() {
    if (!lastResultNumbers) return;
    try {
        const response = await fetch('/interpret', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                number1: lastResultNumbers.number1,
                number2: lastResultNumbers.number2,
                lang: currentLang
            })
        });
        const data = await response.json();
        if (data.success) displayResult({ ...data, skipHistory: true });
    } catch (error) {
        console.error('語系切換重新解讀失敗:', error);
    }
}

// 音效開關與 LocalStorage 持久化 (Issue #15)
const SOUND_STORAGE_KEY = 'yijing_sound_enabled';
const soundToggleBtn = document.getElementById('sound-toggle');

let soundEnabled = true;
try {
    soundEnabled = localStorage.getItem(SOUND_STORAGE_KEY) !== 'false';
} catch (e) {
    console.log('讀取音效設定失敗:', e);
}

function applySoundState() {
    if (!soundToggleBtn) return;
    soundToggleBtn.textContent = soundEnabled ? '🔊' : '🔇';
    soundToggleBtn.setAttribute('aria-pressed', String(soundEnabled));
    soundToggleBtn.classList.toggle('muted', !soundEnabled);
    soundToggleBtn.title = soundEnabled ? t('sound.onTitle') : t('sound.offTitle');
}

soundToggleBtn?.addEventListener('click', () => {
    soundEnabled = !soundEnabled;
    try {
        localStorage.setItem(SOUND_STORAGE_KEY, String(soundEnabled));
    } catch (e) {
        console.log('儲存音效設定失敗:', e);
    }
    applySoundState();
});

// Web Audio API 原生古磬起卦音效 (432Hz)
function playZenChimeSound() {
    if (!soundEnabled) return;
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        
        osc.type = 'sine';
        osc.frequency.setValueAtTime(432, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(108, ctx.currentTime + 1.8);
        
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 2.0);
        
        osc.connect(gain);
        gain.connect(ctx.destination);
        
        osc.start();
        osc.stop(ctx.currentTime + 2.0);
    } catch (e) {
        console.log('Audio Context Error:', e);
    }
}

// 複製卦辭
const copyTextBtn = document.getElementById('copy-text-btn');
copyTextBtn?.addEventListener('click', () => {
    const guaName = guaNameElement?.textContent || '';
    const movingText = document.getElementById('moving-yao-badge')?.textContent || '';
    const derivedName = document.getElementById('derived-gua-name')?.textContent || '';
    const desc = guaDescriptionElement?.textContent || '';
    const interp = guaInterpretationElement?.textContent || '';
    const judgmentRule = document.getElementById('judgment-rule')?.textContent || '';
    const judgmentText = document.getElementById('judgment-text')?.textContent || '';
    const judgmentPrimary = document.getElementById('judgment-primary')?.textContent || '';
    const colon = currentLang === 'en' ? ': ' : '：';

    const textToCopy = `${t('copy.header')}\n${t('copy.primary')}${guaName}\n${movingText} ${currentLang === 'en' ? '➔ ' : '➔ 之 '}${derivedName}\n\n🀄 ${t('gua.judgmentHeader')}${colon}${judgmentRule} · ${judgmentText}\n${t('gua.primaryLabel')}${judgmentPrimary}\n\n${t('export.imageLabel')}\n${desc}\n\n${t('export.interpLabel')}\n${interp}`;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        const span = copyTextBtn.querySelector('span');
        if (span) {
            const original = span.textContent;
            span.textContent = currentLang === 'en' ? '✅ Copied' : '✅ 已複製卦辭';
            setTimeout(() => { span.textContent = original; }, 2000);
        }
    }).catch(err => {
        console.error('複製失敗:', err);
    });
});

// 執行占卜的主要函數
async function performDivination() {
    try {
        // 播放古磬音效
        playZenChimeSound();

        let endpoint = '/divination';

        let options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        };

        if (currentMode === 'custom') {
            const num1 = parseInt(customNum1Input?.value || '0', 10);
            const num2 = parseInt(customNum2Input?.value || '0', 10);
            if (isNaN(num1) || num1 < 1 || num1 > 9999 || isNaN(num2) || num2 < 1 || num2 > 9999) {
                showError(t('error.invalidCustom'));
                return;
            }
            endpoint = '/interpret';
            options.body = JSON.stringify({ number1: num1, number2: num2, lang: currentLang });
        } else {
            endpoint = `/divination?lang=${currentLang}`;
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
            showError(data.error || t('error.unknown'));
        }
    } catch (error) {
        console.error('起卦請求失敗:', error);
        showError(t('error.network'));
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

    // 記錄本次數字，供切換語系時重新解讀 (Issue #16)
    if (data.number1 && data.number2) {
        lastResultNumbers = { number1: data.number1, number2: data.number2 };
    }

    // 本卦
    if (guaNumberTagElement) guaNumberTagElement.textContent = formatHexagramNumber(data.gua_index);
    if (guaSymbolElement) guaSymbolElement.textContent = data.gua_symbol || '☯';
    if (guaNameElement) guaNameElement.textContent = formatGuaName(data.gua_name);

    // 動爻與之卦 (變卦)：支援多爻變 (Issue #14)
    const movingYaoBadge = document.getElementById('moving-yao-badge');
    const derivedGuaSymbol = document.getElementById('derived-gua-symbol');
    const derivedGuaTag = document.getElementById('derived-gua-number-tag');
    const derivedGuaName = document.getElementById('derived-gua-name');

    const movingNames = Array.isArray(data.moving_yao_names) && data.moving_yao_names.length
        ? data.moving_yao_names
        : (data.moving_yao_name ? [data.moving_yao_name] : []);
    const movingCount = data.moving_yao_count || movingNames.length;

    if (movingYaoBadge) movingYaoBadge.textContent = formatMovingLabel(movingNames, movingCount);
    if (derivedGuaSymbol) derivedGuaSymbol.textContent = data.derived_gua_symbol || '☯';
    if (derivedGuaTag) derivedGuaTag.textContent = formatHexagramNumber(data.derived_gua_index ?? 0);
    if (derivedGuaName) derivedGuaName.textContent = formatGuaName(data.derived_gua_name);

    // 朱熹變占判法 (Issue #14)
    const judgmentRuleElement = document.getElementById('judgment-rule');
    const judgmentTextElement = document.getElementById('judgment-text');
    const judgmentPrimaryElement = document.getElementById('judgment-primary');
    const judgmentSecondaryElement = document.getElementById('judgment-secondary');
    const judgmentSecondaryRow = document.getElementById('judgment-secondary-row');

    if (judgmentRuleElement) judgmentRuleElement.textContent = data.judgment_rule || '--';
    if (judgmentTextElement) judgmentTextElement.textContent = data.judgment_text || '';
    if (judgmentPrimaryElement) judgmentPrimaryElement.textContent = data.judgment_primary || '--';
    if (judgmentSecondaryElement) judgmentSecondaryElement.textContent = data.judgment_secondary || '';
    if (judgmentSecondaryRow) judgmentSecondaryRow.classList.toggle('hidden', !data.judgment_secondary);
    
    if (guaDescriptionElement) guaDescriptionElement.textContent = data.gua_description;
    if (guaInterpretationElement) guaInterpretationElement.textContent = data.gua_interpretation;
    
    // 顯示結果卡片
    hideAllCards();
    resultCard.classList.remove('hidden');
    resultCard.classList.add('fade-in');
    
    // 執行細緻的文字與數值浮出動畫
    animateResultElements();

    // 寫入歷史紀錄 (僅當包含全量 data 時；語系切換重新解讀不重複寫入)
    if (data.gua_name && !data.is_history_view && !data.skipHistory) {
        saveToHistory({
            ...data,
            timestamp: new Date().toLocaleDateString() + ' ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        });
    }
}

// LocalStorage 歷史紀錄管理
const STORAGE_KEY = 'yijing_divination_history';
const historyListElement = document.getElementById('history-list');
const clearHistoryBtn = document.getElementById('clear-history-btn');

function saveToHistory(record) {
    let history = getHistory();
    // 避免重複寫入同一筆
    if (history.length > 0 && history[0].gua_index === record.gua_index && history[0].number1 === record.number1) {
        return;
    }
    history.unshift(record);
    if (history.length > 10) history = history.slice(0, 10);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    renderHistory();
}

function getHistory() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        return [];
    }
}

function renderHistory() {
    if (!historyListElement) return;
    const history = getHistory();
    if (history.length === 0) {
        historyListElement.innerHTML = `<p class="empty-history-text">${t('history.empty')}</p>`;
        return;
    }

    const separator = currentLang === 'en' ? ', ' : '、';
    historyListElement.innerHTML = history.map((item, idx) => `
        <div class="history-item" data-idx="${idx}">
            <div class="history-main-info">
                <span class="history-symbol">${item.gua_symbol || '☯'}</span>
                <span class="history-names">${formatGuaName(item.gua_name)} (${(item.moving_yao_names || [item.moving_yao_name || '']).join(separator)} ➔ ${formatGuaName(item.derived_gua_name)})</span>
            </div>
            <span class="history-time">${item.timestamp}</span>
        </div>
    `).join('');

    historyListElement.querySelectorAll('.history-item').forEach(el => {
        el.addEventListener('click', () => {
            const idx = parseInt(el.getAttribute('data-idx') || '0', 10);
            const selected = history[idx];
            if (selected) displayResult({ ...selected, is_history_view: true });
        });
    });
}

clearHistoryBtn?.addEventListener('click', () => {
    localStorage.removeItem(STORAGE_KEY);
    renderHistory();
});



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

    // 頁面載入時套用語系 (i18n) 與歷史紀錄、音效開關狀態
    applyLanguage(currentLang);

    // Service Worker PWA 離線註冊

    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js').catch(err => {
            console.log('SW registration failed:', err);
        });
    }
});

