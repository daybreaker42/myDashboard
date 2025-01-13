async function fetchMarketData() {
    const loadingEl = document.getElementById('markets-loading');
    const errorEl = document.getElementById('markets-error');
    const containerEl = document.getElementById('markets-container');

    try {
        const response = await fetch('http://localhost:30000/api/stocks?full=true');
        const data = await response.json();

        containerEl.innerHTML = Object.entries(data).map(([symbol, info]) => `
            <div class="bg-dark-secondary p-6 rounded-lg">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-2xl font-bold">${getStockName(symbol)}</h2>
                    <p class="text-2xl font-mono ${info.change_percent >= 0 ? 'text-green-500' : 'text-red-500'}">
                        ${info.current_price.toFixed(2)}
                        (${info.change_percent >= 0 ? '+' : ''}${info.change_percent.toFixed(2)}%)
                    </p>
                </div>
                <div class="h-96">
                    <canvas id="chart-${symbol}"></canvas>
                </div>
            </div>
        `).join('');

        // 차트 생성
        Object.entries(data).forEach(([symbol, info]) => {
            const ctx = document.getElementById(`chart-${symbol}`).getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array(info.history.length).fill('').map((_, i) => {
                        const date = new Date();
                        date.setDate(date.getDate() - (info.history.length - i - 1));
                        return date.toLocaleDateString();
                    }),
                    datasets: [{
                        label: getStockName(symbol),
                        data: info.history,
                        borderColor: info.change_percent >= 0 ? '#4CAF50' : '#EF4444',
                        tension: 0.1,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: true }
                    },
                    scales: {
                        x: {
                            grid: { color: '#333' },
                            ticks: { color: '#999' }
                        },
                        y: {
                            grid: { color: '#333' },
                            ticks: { color: '#999' }
                        }
                    }
                }
            });
        });

        loadingEl.classList.add('hidden');
        containerEl.classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        loadingEl.classList.add('hidden');
        errorEl.classList.remove('hidden');
    }
}

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

document.addEventListener('DOMContentLoaded', fetchMarketData);
