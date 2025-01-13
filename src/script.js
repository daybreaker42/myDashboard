const rootDiv = document.getElementById('root');

// async function fetchGTrendData() {
//     const response = await fetch('https://trends.google.co.kr/trending/rss?geo=KR');
//     // XML 응답을 텍스트로 받아옴
//     const xmlText = await response.text();
//     // DOMParser를 사용하여 XML 파싱
//     const parser = new DOMParser();
//     const xmlDoc = parser.parseFromString(xmlText, "text/xml");
//     // XML에서 필요한 데이터 추출 예시
//     const items = Array.from(xmlDoc.getElementsByTagName('item')).map(item => ({
//         title: item.getElementsByTagName('title')[0]?.textContent,
//         description: item.getElementsByTagName('description')[0]?.textContent
//     }));
//     return items;
// }

// rootDiv.innerText = 'Loading...';
// fetchGTrendData().then(data => {
//     // 데이터를 보기 좋게 표시
//     rootDiv.innerHTML = data.map(item =>
//         `<div>
//             <h3>${item.title}</h3>
//             <p>${item.description}</p>
//          </div>`
//     ).join('');
// }).catch(err => {
//     rootDiv.innerText = 'Error: ' + err;
// });

// 시계 관련 함수
const updateClocks = () => {
    const clockContainer = document.getElementById('clock-container');
    const timezones = JSON.parse(localStorage.getItem('timezones')) || [
        { name: '서울', offset: 9 },
        { name: '뉴욕', offset: -5 },
        { name: '런던', offset: 0 }
    ];

    clockContainer.innerHTML = timezones.map(tz => {
        const now = new Date();
        const utc = now.getTime() + (now.getTimezoneOffset() * 60000);
        const tzTime = new Date(utc + (3600000 * tz.offset));

        return `
            <div class="p-4 bg-dark-secondary rounded-lg">
                <h3 class="text-xl mb-2">${tz.name} (GMT${tz.offset >= 0 ? '+' : ''}${tz.offset})</h3>
                <p class="text-2xl font-mono">${tzTime.toLocaleString('ko-KR')}</p>
            </div>
        `;
    }).join('');
};

// 새로고침 타이머 관리 함수
const createRefreshTimer = (elementId, intervalMs) => {
    const timerElement = document.getElementById(elementId);
    let timeLeft = intervalMs / 1000;

    const updateTimer = () => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `(${minutes}:${seconds.toString().padStart(2, '0')})`;
        timeLeft -= 1;
        if (timeLeft < 0) {
            timeLeft = intervalMs / 1000;
        }
    };

    updateTimer();
    return setInterval(updateTimer, 1000);
};

// Google Trends 데이터 가져오기
const fetchTrends = async () => {
    const loadingEl = document.getElementById('trends-loading');
    const errorEl = document.getElementById('trends-error');
    const containerEl = document.getElementById('trends-container');

    try {
        loadingEl.classList.remove('hidden');
        errorEl.classList.add('hidden');
        containerEl.classList.add('hidden');

        const response = await fetch('http://localhost:30000/api/trends');
        const data = await response.json();

        containerEl.innerHTML = data.trends.map(item => `
            <div class="p-4 bg-dark-secondary rounded-lg">
                <h3 class="text-xl mb-2">${item.title}</h3>
                ${item['ht:picture'] ? `
                    <img src="${item['ht:picture']}" alt="${item.title}" 
                         class="object-cover rounded mb-2">
                ` : ''}
                <p class="text-sm text-gray-400">검색량: ${item['ht:approx_traffic']}</p>
            </div>
        `).join('');

        loadingEl.classList.add('hidden');
        containerEl.classList.remove('hidden');
    } catch (error) {
        console.error('Error fetching trends:', error);
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
    }
};

// 주식 데이터 가져오기
const fetchStocks = async () => {
    const loadingEl = document.getElementById('stocks-loading');
    const errorEl = document.getElementById('stocks-error');
    const containerEl = document.getElementById('stocks-container');

    try {
        loadingEl.classList.remove('hidden');
        errorEl.classList.add('hidden');
        containerEl.classList.add('hidden');

        const response = await fetch('http://localhost:30000/api/stocks');
        const data = await response.json();

        containerEl.innerHTML = Object.entries(data).map(([symbol, info]) => `
            <div class="p-4 bg-dark-secondary rounded-lg">
                <h3 class="text-xl mb-2">${getStockName(symbol)}</h3>
                <p class="text-2xl font-mono ${info.change_percent >= 0 ? 'text-green-500' : 'text-red-500'}">
                    ${info.current_price.toFixed(2)}
                    (${info.change_percent >= 0 ? '+' : ''}${info.change_percent.toFixed(2)}%)
                </p>
                <canvas id="chart-${symbol}" class="w-full h-32 mt-2"></canvas>
            </div>
        `).join('');

        // 차트 그리기
        Object.entries(data).forEach(([symbol, info]) => {
            const ctx = document.getElementById(`chart-${symbol}`).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [...Array(info.history.length).keys()],
                    datasets: [{
                        data: info.history,
                        borderColor: '#4CAF50',
                        tension: 0.1
                    }]
                },
                options: {
                    plugins: { legend: { display: false } },
                    scales: { x: { display: false }, y: { display: false } }
                }
            });
        });

        loadingEl.classList.add('hidden');
        containerEl.classList.remove('hidden');
    } catch (error) {
        console.error('Error fetching stocks:', error);
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
    }
};

// 주식 심볼을 이름으로 변환
const getStockName = (symbol) => {
    const names = {
        '^IXIC': '나스닥',
        '^GSPC': 'S&P 500',
        '^DJI': '다우존스',
        '^VIX': 'VIX',
        '^FVX': '미국 5년물',
        '^TNX': '미국 10년물',
        '^TYX': '미국 30년물'
    };
    return names[symbol] || symbol;
};

// 초기화 및 이벤트 리스너
document.addEventListener('DOMContentLoaded', () => {
    // Chart.js CDN 추가
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    document.head.appendChild(script);

    // 초기 데이터 로드
    updateClocks();
    fetchTrends();
    fetchStocks();

    // 주기적 업데이트
    setInterval(updateClocks, 1000);
    setInterval(fetchTrends, 300000);  // 5분마다
    setInterval(fetchStocks, 300000);  // 5분마다

    // 새로고침 타이머 시작
    const REFRESH_INTERVAL = 300000; // 5분
    createRefreshTimer('trends-refresh-timer', REFRESH_INTERVAL);
    createRefreshTimer('stocks-refresh-timer', REFRESH_INTERVAL);

    // 데이터 자동 새로고침 설정
    setInterval(() => {
        fetchTrends();
        fetchStocks();
    }, REFRESH_INTERVAL);

    // 새로고침 버튼 이벤트
    document.getElementById('refresh-trends').addEventListener('click', () => {
        const timerEl = document.getElementById('trends-refresh-timer');
        timerEl.textContent = '(5:00)';
        fetchTrends();
    });
});