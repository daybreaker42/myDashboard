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

// 새로고침 타이머 관리 함수 수정
const createRefreshTimer = (elementId, intervalMs) => {
    const timerElement = document.getElementById(elementId);
    let timeLeft = intervalMs / 1000;
    let lastUpdate = new Date();

    const updateTimer = () => {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `(${minutes}:${seconds.toString().padStart(2, '0')}) - 마지막 업데이트: ${lastUpdate.toLocaleTimeString()}`;
        timeLeft -= 1;
        if (timeLeft < 0) {
            timeLeft = intervalMs / 1000;
            lastUpdate = new Date();
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

        console.log(data);

        containerEl.innerHTML = data.trends.map(item => {
            // const newsItems = item['ht:news_item'] || [];
            const newsItems = Array.isArray(item['ht:news_item'])
                ? item['ht:news_item']
                : item['ht:news_item']
                    ? [item['ht:news_item']]
                    : [];

            console.log(`newsItems for ${item.title}:`, newsItems);
            return `
                <div class="bg-dark-secondary rounded-lg overflow-hidden">
                    <div class="p-4">
                        <div class="flex items-start gap-4">
                            <img src="${item['ht:picture'] || '/static/assets/no-image.png'}" 
                                 alt="${item.title}" 
                                 class="w-[100px] h-[100px] object-cover rounded">
                            <div class="flex-1">
                                <h3 class="text-lg font-semibold">${item.title}</h3>
                                <p class="text-sm text-gray-400 mb-2">검색량: ${item['ht:approx_traffic']}</p>
                                <button class="text-sm text-blue-400 hover:text-blue-300 transition-colors news-toggle"
                                        data-target="news-${item.title.replace(/\s+/g, '-')}">
                                    <span class="toggle-text" data-type="more">관련 뉴스 ${newsItems.length}개 보기</span>
                                    <span class="toggle-text hidden" data-type="hide">관련 뉴스 접기</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div id="news-${item.title.replace(/\s+/g, '-')}" class="hidden border-t border-gray-700">
                        ${newsItems.map(news => `
                            <a href="${news['ht:news_item_url']}" target="_blank" 
                               class="block p-4 hover:bg-gray-700 transition-colors border-b border-gray-700">
                                <div class="flex gap-4 items-center">
                                    <img src="${news['ht:news_item_picture'] || '/static/assets/no-image.png'}" 
                                         alt="${news['ht:news_item_title']}"
                                         class="w-16 h-16 object-cover rounded">
                                    <div>
                                        <h4 class="font-medium mb-1">${news['ht:news_item_title']}</h4>
                                        <p class="text-sm text-gray-400">${news['ht:news_item_source']}</p>
                                    </div>
                                </div>
                            </a>
                        `).join('')}
                    </div>
                </div>
            `;
        }).join('');

        // 수정: 뉴스 토글 이벤트 리스너 개선
        document.querySelectorAll('.news-toggle').forEach(button => {
            button.addEventListener('click', (e) => {
                const targetId = button.dataset.target;
                const targetEl = document.getElementById(targetId);
                const toggleTexts = button.querySelectorAll('.toggle-text');

                targetEl.classList.toggle('hidden');
                toggleTexts.forEach(span => span.classList.toggle('hidden'));
            });
        });

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
document.addEventListener('DOMContentLoaded', async () => {
    // Chart.js 로딩 대기
    await new Promise((resolve) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = resolve;
        document.head.appendChild(script);
    });

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

    // 새로고침 버튼 이벤트 수정
    document.getElementById('refresh-trends').addEventListener('click', () => {
        const timerEl = document.getElementById('trends-refresh-timer');
        const now = new Date();
        timerEl.textContent = `(5:00) - 마지막 업데이트: ${now.toLocaleTimeString()}`;
        fetchTrends();
    });
});