const levels = [
    { level: 1, type: 'y', a: 10, b: 2, x: 5, target: 320, briefing: "Initial cluster detected. 10 infected individuals. The virus doubles every day (b=2). Calculate the total projected cases (y) on day 5." },
    { level: 2, type: 'y', a: 50, b: 1.5, x: 4, target: 253.125, briefing: "New strain found. 50 current cases, growing by 50% daily (b=1.5). Find the expected cases (y) after 4 days. (Enter exact decimal)." },
    { level: 3, type: 'a', b: 3, x: 4, y: 810, target: 10, briefing: "Contact tracing protocol initiated. We have 810 cases on day 4. The transmission multiplier (b) is 3. Calculate Patient Zero cluster size (a)." },
    { level: 4, type: 'a', b: 1.2, x: 3, y: 1728, target: 1000, briefing: "Hospital records show 1728 cases on day 3. Growth rate is 1.2. Work backward to find how many initial cases (a) there were on day 0." },
    { level: 5, type: 'b', a: 100, x: 2, y: 400, target: 2, briefing: "We started with 100 cases. Exactly 2 days later, we have 400. What is the daily growth multiplier (b)?" },
    { level: 6, type: 'b', a: 500, x: 3, y: 4000, target: 2, briefing: "Outbreak is expanding rapidly. 500 cases grew to 4000 in just 3 days. Find the transmission rate (b)." },
    { level: 7, type: 'x', a: 5, b: 4, y: 1280, target: 4, briefing: "Critical Alert: Hospitals will be overrun at 1280 cases. We have 5 cases now, quadrupling daily (b=4). How many days (x) to prepare?" },
    { level: 8, type: 'x', a: 200, b: 0.5, y: 25, target: 3, briefing: "Vaccine deployed! Cases are now halving (b=0.5) daily. From 200 current cases, how many days (x) until we reach the safe threshold of 25 cases?" },
    { level: 9, type: 'y', a: 10000, b: 0.8, x: 3, target: 5120, briefing: "Strict lockdown in effect. The decay multiplier is 0.8. Starting with 10,000 cases, calculate the total active cases (y) remaining on day 3." },
    { level: 10, type: 'a', b: 0.1, x: 2, y: 5, target: 500, briefing: "Eradication is imminent. Only 5 cases remain on day 2 of the new protocol. The decay rate is 0.1. What was the exact case count at lockdown start (a)?" }
];

let currentLevelIndex = 0;
let outbreakChart;
let typeWriterTimeout;

function initChart() {
    const ctx = document.getElementById('outbreakChart').getContext('2d');
    Chart.defaults.color = '#0f0';
    Chart.defaults.font.family = "'Courier New', Courier, monospace";
    Chart.defaults.borderColor = 'rgba(0, 255, 0, 0.2)';

    outbreakChart = new Chart(ctx, {
        type: 'line',
        data: { 
            labels: [0, 1, 2, 3, 4, 5], 
            datasets: [{ 
                label: 'Projected Infected Population', 
                data: [0, 0, 0, 0, 0, 0], 
                borderColor: '#0f0', 
                backgroundColor: 'rgba(0, 255, 0, 0.1)', 
                borderWidth: 2, 
                pointBackgroundColor: '#0f0',
                pointBorderColor: '#fff',
                pointRadius: 3,
                pointHoverRadius: 6,
                fill: true, 
                tension: 0.4 
            }] 
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            scales: { 
                y: { beginAtZero: true, title: { display: true, text: 'Total Cases (y)' } }, 
                x: { title: { display: true, text: 'Time in Days (x)' } } 
            }, 
            plugins: { 
                legend: { display: false },
                tooltip: { backgroundColor: 'rgba(0, 10, 0, 0.9)', titleColor: '#0f0', bodyColor: '#0f0', borderColor: '#0f0', borderWidth: 1 }
            } 
        }
    });
}

function updateChart(a, b, maxX) {
    const labels = []; const data = [];
    const displayDays = Math.max(5, maxX + 1);
    for(let i = 0; i <= displayDays; i++) {
        labels.push('Day ' + i);
        data.push(a * Math.pow(b, i));
    }
    outbreakChart.data.labels = labels;
    outbreakChart.data.datasets[0].data = data;
    outbreakChart.update();
}

function typeWriter(text, i) {
    if (i === 0) document.getElementById('briefing-text').innerHTML = '';
    if (i < text.length) {
        document.getElementById('briefing-text').innerHTML += text.charAt(i);
        typeWriterTimeout = setTimeout(() => typeWriter(text, i + 1), 20);
    }
}

function loadLevel() {
    const lvl = levels[currentLevelIndex];
    document.getElementById('level-display').innerText = lvl.level;
    clearTimeout(typeWriterTimeout);
    typeWriter(lvl.briefing, 0);
    
    const container = document.getElementById('inputs-container');
    container.innerHTML = '';
    
    const variables = [
        { key: 'a', label: 'Initial Cases (a)' },
        { key: 'b', label: 'Growth Multiplier (b)' },
        { key: 'x', label: 'Time in Days (x)' },
        { key: 'y', label: 'Total Cases (y)' }
    ];
    
    variables.forEach(v => {
        const row = document.createElement('div'); row.className = 'input-row';
        const labelEl = document.createElement('span'); labelEl.innerText = v.label + ':';
        row.appendChild(labelEl);
        
        if (lvl.type === v.key) {
            const inputEl = document.createElement('input');
            inputEl.type = 'number'; inputEl.id = 'input-solve'; inputEl.step = 'any'; inputEl.placeholder = '?';
            inputEl.addEventListener('keypress', function (e) { if (e.key === 'Enter') document.getElementById('submit-btn').click(); });
            row.appendChild(inputEl);
        } else {
            const valEl = document.createElement('span'); valEl.innerText = lvl[v.key]; valEl.style.color = '#fff';
            row.appendChild(valEl);
        }
        container.appendChild(row);
    });

    document.getElementById('feedback').innerText = '';
    document.getElementById('feedback').className = '';
    document.getElementById('next-btn').classList.add('hidden');
    document.getElementById('submit-btn').classList.remove('hidden');
    
    setTimeout(() => {
        const input = document.getElementById('input-solve');
        if(input) input.focus();
    }, 100);
    
    outbreakChart.data.datasets[0].data = [];
    outbreakChart.update();
}

document.getElementById('submit-btn').addEventListener('click', () => {
    const lvl = levels[currentLevelIndex];
    const inputEl = document.getElementById('input-solve');
    const guess = parseFloat(inputEl.value);
    
    if (isNaN(guess)) {
        document.getElementById('feedback').innerText = '>> ERROR: INVALID INPUT DETECTED.';
        document.getElementById('feedback').className = 'error';
        return;
    }

    if (Math.abs(guess - lvl.target) < 0.001) {
        document.getElementById('feedback').innerText = '>> CALCULATION CONFIRMED. UPDATING...';
        document.getElementById('feedback').className = 'success';
        document.getElementById('submit-btn').classList.add('hidden');
        
        if (currentLevelIndex < levels.length - 1) {
            document.getElementById('next-btn').classList.remove('hidden');
        } else {
            document.getElementById('next-btn').classList.remove('hidden');
            document.getElementById('next-btn').innerText = 'SIMULATION COMPLETE';
            document.getElementById('next-btn').disabled = true;
            document.getElementById('feedback').innerText = '>> ALL THREATS NEUTRALIZED.';
        }
        
        const a = lvl.type === 'a' ? guess : lvl.a;
        const b = lvl.type === 'b' ? guess : lvl.b;
        const x = lvl.type === 'x' ? guess : lvl.x;
        updateChart(a, b, x);
    } else {
        document.getElementById('feedback').innerText = '>> ERROR: INCORRECT PROJECTION.';
        document.getElementById('feedback').className = 'error';
    }
});

document.getElementById('next-btn').addEventListener('click', () => {
    currentLevelIndex++;
    loadLevel();
});

window.onload = () => { initChart(); loadLevel(); };
