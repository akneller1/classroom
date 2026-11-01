const levels = [
    { level: 1, type: 'coord', t: {x: 4, y: 5}, ans: {x:4, y:5}, briefing: "Captain! We spotted a shipwreck 🚢. Look at the grid and enter its exact (X, Y) coordinates." },
    { level: 2, type: 'coord', t: {x: -6, y: 3}, ans: {x:-6, y:3}, briefing: "Another wreck 🚢 in the deep trench! Find its (X, Y) coordinates." },
    { level: 3, type: 'dist', s: {x: -3, y: -2}, t: {x: 5, y: -2}, ans: 8, briefing: "The submarine 🛥️ is at (-3, -2) and a chest 💎 is at (5, -2). How far away is it? (Count the grid lines!)" },
    { level: 4, type: 'dist', s: {x: 4, y: 5}, t: {x: 4, y: -4}, ans: 9, briefing: "The submarine 🛥️ is at (4, 5) and the treasure 💎 is straight down at (4, -4). What is the vertical distance?" },
    { level: 5, type: 'dist', s: {x: 0, y: 0}, t: {x: 3, y: 4}, ans: 5, briefing: "Diagonal trip! The sub is at (0,0) and the chest is at (3,4). Use the Pythagorean Theorem (<span class='math-font'>a² + b² = c²</span>) to find the distance." },
    { level: 6, type: 'dist', s: {x: -4, y: -1}, t: {x: 8, y: 4}, ans: 13, briefing: "Diagonal again! The sub is at (-4, -1) and the wreck is at (8, 4). Calculate the horizontal and vertical sides of the triangle first, then find the distance." },
    { level: 7, type: 'midpoint', s: {x: -6, y: 2}, t: {x: 2, y: 6}, ans: {x: -2, y: 4}, briefing: "Two pirate ships 🏴‍☠️ sank! The treasure 💎 spilled exactly halfway between them. Find the Midpoint (X, Y)." },
    { level: 8, type: 'midpoint', s: {x: -5, y: -5}, t: {x: 3, y: -1}, ans: {x: -1, y: -3}, briefing: "More midpoint practice! Ship A at (-5, -5), Ship B at (3, -1). Find the coordinates (X, Y) of the midpoint." },
    { level: 9, type: 'dist', s: {x: 1, y: 2}, t: {x: 9, y: 8}, ans: 10, briefing: "A treasure map shows a path from (1, 2) to (9, 8). Use the distance formula to find out exactly how far the sub must travel!" },
    { level: 10, type: 'dist', s: {x: -8, y: -7}, t: {x: 7, y: 1}, ans: 17, briefing: "Ultimate Salvage! A Kraken 🐙 is guarding the final chest. Sub at (-8, -7), Kraken at (7, 1). Find the exact diagonal distance!" }
];

let currentLevelIndex = 0;
const canvas = document.getElementById('oceanCanvas');
const ctx = canvas.getContext('2d');
const GRID_UNITS = 20; // -10 to +10

function sX(x) { return (canvas.width / 2) + (x * (canvas.width / GRID_UNITS)); }
function sY(y) { return (canvas.height / 2) - (y * (canvas.height / GRID_UNITS)); }

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Grid Lines
    ctx.lineWidth = 1;
    for (let i = -10; i <= 10; i++) {
        ctx.strokeStyle = (i === 0) ? '#00f5d4' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = (i === 0) ? 3 : 1;
        
        // Vertical
        ctx.beginPath(); ctx.moveTo(sX(i), 0); ctx.lineTo(sX(i), canvas.height); ctx.stroke();
        // Horizontal
        ctx.beginPath(); ctx.moveTo(0, sY(i)); ctx.lineTo(canvas.width, sY(i)); ctx.stroke();
    }
    
    // Labels
    ctx.fillStyle = '#90e0ef';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (let i = -10; i <= 10; i++) {
        if (i !== 0) {
            ctx.fillText(i, sX(i), sY(0) + 15);
            ctx.fillText(i, sX(0) - 15, sY(i));
        }
    }
    // Origin
    ctx.fillText('0', sX(0) - 10, sY(0) + 15);
}

function drawLevelElements(animatedProgress = 0, isCorrect = false) {
    drawGrid();
    const lvl = levels[currentLevelIndex];
    ctx.font = '36px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    if (lvl.type === 'coord') {
        ctx.fillText('🚢', sX(lvl.t.x), sY(lvl.t.y));
        if (isCorrect) {
            // Drop an anchor emoji on success
            ctx.fillText('⚓', sX(lvl.t.x), sY(lvl.t.y) - (20 * (1-animatedProgress)));
        }
    } 
    else if (lvl.type === 'dist') {
        const targetEmoji = (lvl.level === 10) ? '🐙' : '💎';
        ctx.fillText(targetEmoji, sX(lvl.t.x), sY(lvl.t.y));
        
        if (isCorrect) {
            // Animate submarine moving
            const currX = lvl.s.x + (lvl.t.x - lvl.s.x) * animatedProgress;
            const currY = lvl.s.y + (lvl.t.y - lvl.s.y) * animatedProgress;
            
            // Draw path line
            ctx.beginPath();
            ctx.moveTo(sX(lvl.s.x), sY(lvl.s.y));
            ctx.lineTo(sX(currX), sY(currY));
            ctx.strokeStyle = '#ff9f1c'; ctx.lineWidth = 4; ctx.setLineDash([8, 8]);
            ctx.stroke(); ctx.setLineDash([]);
            
            ctx.fillText('🛥️', sX(currX), sY(currY));
        } else {
            ctx.fillText('🛥️', sX(lvl.s.x), sY(lvl.s.y));
        }
    }
    else if (lvl.type === 'midpoint') {
        ctx.fillText('🏴‍☠️', sX(lvl.s.x), sY(lvl.s.y));
        ctx.fillText('🏴‍☠️', sX(lvl.t.x), sY(lvl.t.y));
        
        // Draw dotted line between them
        ctx.beginPath(); ctx.moveTo(sX(lvl.s.x), sY(lvl.s.y)); ctx.lineTo(sX(lvl.t.x), sY(lvl.t.y));
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)'; ctx.lineWidth = 2; ctx.setLineDash([5, 5]);
        ctx.stroke(); ctx.setLineDash([]);
        
        if (isCorrect) {
            // Animate treasure appearing at midpoint
            ctx.globalAlpha = animatedProgress;
            ctx.fillText('💎', sX(lvl.ans.x), sY(lvl.ans.y));
            ctx.globalAlpha = 1.0;
        }
    }
}

function loadLevel() {
    const lvl = levels[currentLevelIndex];
    document.getElementById('level-display').innerText = lvl.level;
    document.getElementById('briefing-text').innerHTML = lvl.briefing;
    
    const container = document.getElementById('inputs-container');
    container.innerHTML = '';
    
    if (lvl.type === 'coord' || lvl.type === 'midpoint') {
        container.innerHTML = `
            <div class="input-row"><span>X-Coordinate:</span><input type="number" id="in-x" placeholder="X"></div>
            <div class="input-row"><span>Y-Coordinate:</span><input type="number" id="in-y" placeholder="Y"></div>
        `;
    } else if (lvl.type === 'dist') {
        container.innerHTML = `
            <div class="input-row"><span>Total Distance:</span><input type="number" id="in-dist" placeholder="Dist"></div>
        `;
    }
    
    // Add Enter key support
    const inputs = container.querySelectorAll('input');
    inputs.forEach(inp => {
        inp.addEventListener('keypress', e => { if (e.key === 'Enter') document.getElementById('submit-btn').click(); });
    });
    
    if(inputs.length > 0) setTimeout(() => inputs[0].focus(), 100);

    document.getElementById('feedback').innerText = '';
    document.getElementById('feedback').className = '';
    document.getElementById('next-btn').classList.add('hidden');
    document.getElementById('submit-btn').classList.remove('hidden');
    
    drawLevelElements(0, false);
}

document.getElementById('submit-btn').addEventListener('click', () => {
    const lvl = levels[currentLevelIndex];
    let isCorrect = false;
    
    if (lvl.type === 'coord' || lvl.type === 'midpoint') {
        const x = parseFloat(document.getElementById('in-x').value);
        const y = parseFloat(document.getElementById('in-y').value);
        if (x === lvl.ans.x && y === lvl.ans.y) isCorrect = true;
    } else if (lvl.type === 'dist') {
        const dist = parseFloat(document.getElementById('in-dist').value);
        if (dist === lvl.ans) isCorrect = true;
    }
    
    if (isCorrect) {
        document.getElementById('feedback').innerText = "✅ SPOT ON! SALVAGE SUCCESSFUL!";
        document.getElementById('feedback').className = 'success';
        document.getElementById('submit-btn').classList.add('hidden');
        
        // Animation Loop
        let progress = 0;
        function animate() {
            progress += 0.03;
            drawLevelElements(Math.min(progress, 1), true);
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                if (currentLevelIndex < levels.length - 1) {
                    document.getElementById('next-btn').classList.remove('hidden');
                } else {
                    document.getElementById('feedback').innerText = "🏆 ALL TREASURES RECOVERED! PERFECT SCORE!";
                }
            }
        }
        animate();
        
    } else {
        document.getElementById('feedback').innerText = "❌ MISS! RECALCULATE YOUR MATH!";
        document.getElementById('feedback').className = 'error';
    }
});

document.getElementById('next-btn').addEventListener('click', () => {
    currentLevelIndex++;
    loadLevel();
});

window.onload = loadLevel;
