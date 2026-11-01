const levels = [
    // 1. Build
    { mode: 'build', level: 1, expr: "x(x + 2)", top: ['x', '2'], left: ['x'], area: "x² + 2x", inv: ['x²', '2x', '3'], req: ['x²', '2x'] },
    // 2. Build
    { mode: 'build', level: 2, expr: "(x + 1)(x + 3)", top: ['x', '3'], left: ['x', '1'], area: "x² + 4x + 3", inv: ['x²', '3x', '1x', '3', '2'], req: ['x²', '3x', '1x', '3'] },
    // 3. Factor
    { mode: 'factor', level: 3, area: "x² + 5x + 6", lockedRows: [['x²', '3x'], ['2x', '6']], topAns: ['x', '3'], leftAns: ['x', '2'] },
    // 4. Build Negatives
    { mode: 'build', level: 4, expr: "(x - 2)(x + 4)", top: ['x', '4'], left: ['x', '-2'], area: "x² + 2x - 8", inv: ['x²', '4x', '-2x', '-8', '8'], req: ['x²', '4x', '-2x', '-8'] },
    // 5. Factor Negatives
    { mode: 'factor', level: 5, area: "x² - x - 6", lockedRows: [['x²', '2x'], ['-3x', '-6']], topAns: ['x', '2'], leftAns: ['x', '-3'] },
    // 6. Perimeter Intro
    { mode: 'perimeter', level: 6, area: "x² + 3x + 2", lockedRows: [['x²', '2x'], ['1x', '2']], top: ['x', '2'], left: ['x', '1'], perimAns: "4x + 6" },
    // 7. Factor Difference of squares
    { mode: 'factor', level: 7, area: "x² - 25", lockedRows: [['x²', '5x'], ['-5x', '-25']], topAns: ['x', '5'], leftAns: ['x', '-5'] },
    // 8. Build Coeff
    { mode: 'build', level: 8, expr: "(2x + 1)(x + 3)", top: ['x', '3'], left: ['2x', '1'], area: "2x² + 7x + 3", inv: ['2x²', '6x', '1x', '3', '7x'], req: ['2x²', '6x', '1x', '3'] },
    // 9. Factor Coeff
    { mode: 'factor', level: 9, area: "3x² + 5x + 2", lockedRows: [['3x²', '2x'], ['3x', '2']], topAns: ['x', '1'], leftAns: ['3x', '2'] },
    // 10. Perimeter Coeff
    { mode: 'perimeter', level: 10, area: "2x² + 7x + 3", lockedRows: [['2x²', '6x'], ['1x', '3']], top: ['x', '3'], left: ['2x', '1'], perimAns: "6x + 8" }
];

let currentLevelIndex = 0;
let draggedPlot = null;

const reqContainer = document.getElementById('requirements-container');
const invContainer = document.getElementById('plot-inventory');
const gardenArea = document.getElementById('garden-area');
const topHeaders = document.getElementById('grid-headers-top');
const leftHeaders = document.getElementById('grid-headers-left');
const testBtn = document.getElementById('test-btn');
const nextBtn = document.getElementById('next-btn');
const feedback = document.getElementById('feedback-message');
const levelDisplay = document.getElementById('level-display');
const modeDisplay = document.getElementById('mode-display');
const invInstruction = document.getElementById('inventory-instruction');

// Helper to determine plot styling
function getPlotType(val) {
    if (val.includes('²')) return 'x2';
    if (val.includes('x')) return 'x';
    return '1';
}

function createPlotElement(val, locked = false, isInv = false) {
    const plot = document.createElement('div');
    const type = getPlotType(val);
    plot.className = `plot plot-${type}`;
    if (isInv) plot.classList.add('inv-plot');
    if (val.includes('-')) plot.classList.add('plot-neg');
    if (locked) plot.classList.add('locked');
    
    plot.textContent = val;
    plot.dataset.val = val;
    
    if (!locked) {
        plot.draggable = true;
        plot.addEventListener('dragstart', handleDragStart);
        plot.addEventListener('dragend', handleDragEnd);
    }
    return plot;
}

function loadLevel(index) {
    const data = levels[index];
    levelDisplay.textContent = data.level;
    
    reqContainer.innerHTML = '';
    invContainer.innerHTML = '';
    gardenArea.innerHTML = '';
    topHeaders.innerHTML = '';
    leftHeaders.innerHTML = '';
    feedback.textContent = '';
    feedback.className = 'feedback';
    nextBtn.classList.add('hidden');
    testBtn.classList.remove('hidden');

    // Define Grid Size mapping
    const sizeMap = { 'x': '100px', '2x': '100px', '3x': '100px', '1': '60px', '2': '60px', '3': '60px', '4': '60px', '5': '60px', '-2': '60px', '-3': '60px', '-5': '60px' };
    function getSize(val) { return val.includes('x') ? '120px' : '70px'; } // Simplified sizing

    if (data.mode === 'build') {
        modeDisplay.textContent = 'Build Mode (Multiply)';
        invInstruction.textContent = "Drag blocks into the grid to form the area.";
        testBtn.textContent = "Inspect Area";

        reqContainer.innerHTML = `
            <div class="requirement-box">
                <h3>Target Dimensions:</h3><div class="req-term">${data.expr}</div>
                <h3>Expected Area:</h3><div class="req-term">${data.area}</div>
            </div>`;

        // Render Headers & set Grid CSS
        let cols = data.top.map(getSize).join(' ');
        let rows = data.left.map(getSize).join(' ');
        gardenArea.style.gridTemplateColumns = cols;
        gardenArea.style.gridTemplateRows = rows;

        data.top.forEach(h => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.width = getSize(h); el.textContent = h;
            topHeaders.appendChild(el);
        });
        data.left.forEach(h => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.height = getSize(h); el.textContent = h;
            leftHeaders.appendChild(el);
        });

        data.inv.forEach(v => invContainer.appendChild(createPlotElement(v, false, true)));

        // Create empty drop zones
        const totalCells = data.top.length * data.left.length;
        for (let i = 0; i < totalCells; i++) {
            const slot = document.createElement('div'); slot.className = 'drop-zone';
            slot.addEventListener('dragover', handleDragOver); slot.addEventListener('dragleave', handleDragLeave); slot.addEventListener('drop', handleDrop);
            gardenArea.appendChild(slot);
        }

    } else if (data.mode === 'factor') {
        modeDisplay.textContent = 'Survey Mode (Factor)';
        invInstruction.textContent = "Determine the outside dimensions (factors).";
        testBtn.textContent = "Check Factors";
        
        reqContainer.innerHTML = `
            <div class="requirement-box">
                <h3>Total Area Provided:</h3><div class="req-term">${data.area}</div>
                <small style="color: #bdc3c7;">Type the correct terms into the outside header boxes to factor the polynomial.</small>
            </div>`;
            
        let cols = data.topAns.map(getSize).join(' ');
        let rows = data.leftAns.map(getSize).join(' ');
        gardenArea.style.gridTemplateColumns = cols;
        gardenArea.style.gridTemplateRows = rows;

        data.topAns.forEach((h, i) => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.width = getSize(h);
            el.innerHTML = `<input type="text" class="header-input" id="top-ans-${i}" placeholder="?">`;
            topHeaders.appendChild(el);
        });
        data.leftAns.forEach((h, i) => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.height = getSize(h);
            el.innerHTML = `<input type="text" class="header-input" id="left-ans-${i}" placeholder="?">`;
            leftHeaders.appendChild(el);
        });

        // Fill grid with locked plots
        data.lockedRows.forEach(row => {
            row.forEach(val => {
                const slot = document.createElement('div'); slot.className = 'drop-zone';
                slot.appendChild(createPlotElement(val, true, false));
                gardenArea.appendChild(slot);
            });
        });
        
    } else if (data.mode === 'perimeter') {
        modeDisplay.textContent = 'Perimeter Mode';
        invInstruction.textContent = "Calculate the perimeter of the entire garden.";
        testBtn.textContent = "Submit Perimeter";
        
        reqContainer.innerHTML = `
            <div class="requirement-box">
                <h3>Calculate Perimeter:</h3>
                <input type="text" class="perimeter-input" id="perim-ans" placeholder="e.g. 4x + 6">
                <small style="color: #bdc3c7; display:block; margin-top:5px;">Add all outside edges together.</small>
            </div>`;
            
        let cols = data.top.map(getSize).join(' ');
        let rows = data.left.map(getSize).join(' ');
        gardenArea.style.gridTemplateColumns = cols;
        gardenArea.style.gridTemplateRows = rows;

        data.top.forEach(h => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.width = getSize(h); el.textContent = h;
            topHeaders.appendChild(el);
        });
        data.left.forEach(h => {
            const el = document.createElement('div'); el.className = 'header-cell'; el.style.height = getSize(h); el.textContent = h;
            leftHeaders.appendChild(el);
        });

        // Fill grid with locked plots
        data.lockedRows.forEach(row => {
            row.forEach(val => {
                const slot = document.createElement('div'); slot.className = 'drop-zone';
                slot.appendChild(createPlotElement(val, true, false));
                gardenArea.appendChild(slot);
            });
        });
    }
}

// Drag & Drop
function handleDragStart(e) { draggedPlot = this; setTimeout(() => this.style.display = 'none', 0); }
function handleDragEnd(e) { this.style.display = 'flex'; draggedPlot = null; }
function handleDragOver(e) { e.preventDefault(); this.classList.add('drag-over'); }
function handleDragLeave(e) { this.classList.remove('drag-over'); }
function handleDrop(e) {
    e.preventDefault(); this.classList.remove('drag-over');
    if (draggedPlot) {
        if (this.children.length > 0) invContainer.appendChild(this.children[0]);
        draggedPlot.classList.remove('inv-plot');
        this.appendChild(draggedPlot);
    }
}
invContainer.addEventListener('dragover', e => e.preventDefault());
invContainer.addEventListener('drop', function(e) {
    if (draggedPlot) { draggedPlot.classList.add('inv-plot'); this.appendChild(draggedPlot); }
});

testBtn.addEventListener('click', () => {
    const data = levels[currentLevelIndex];
    let correct = true;

    if (data.mode === 'build') {
        const slots = document.querySelectorAll('.drop-zone');
        let placed = Array.from(slots).map(s => s.children.length > 0 ? s.children[0].dataset.val : null);
        if (placed.includes(null)) {
            feedback.textContent = "Fill the whole grid!"; feedback.className = 'feedback error'; return;
        }
        let placedSorted = [...placed].sort();
        let reqSorted = [...data.req].sort();
        correct = JSON.stringify(placedSorted) === JSON.stringify(reqSorted);
        
    } else if (data.mode === 'factor') {
        // Allow swapped binomials (row vs col) if perfectly symmetric, but to keep it simple we check exactly
        const tAns = data.topAns.map((_, i) => document.getElementById(`top-ans-${i}`).value.trim().replace(/\s/g,''));
        const lAns = data.leftAns.map((_, i) => document.getElementById(`left-ans-${i}`).value.trim().replace(/\s/g,''));
        
        const reqTop = data.topAns.map(a => a.replace(/\s/g,''));
        const reqLeft = data.leftAns.map(a => a.replace(/\s/g,''));
        
        // Option 1: Top = reqTop, Left = reqLeft
        const match1 = JSON.stringify(tAns) === JSON.stringify(reqTop) && JSON.stringify(lAns) === JSON.stringify(reqLeft);
        // Option 2: Top = reqLeft, Left = reqTop (assuming square grid)
        const match2 = JSON.stringify(tAns) === JSON.stringify(reqLeft) && JSON.stringify(lAns) === JSON.stringify(reqTop);
        
        correct = match1 || match2;
        
    } else if (data.mode === 'perimeter') {
        const ans = document.getElementById('perim-ans').value.trim().replace(/\s/g,'');
        const req = data.perimAns.replace(/\s/g,'');
        correct = ans === req;
    }

    if (correct) {
        feedback.textContent = "Correct! Well done.";
        feedback.className = 'feedback success';
        testBtn.classList.add('hidden');
        if (currentLevelIndex < levels.length - 1) nextBtn.classList.remove('hidden');
        else feedback.textContent = "Master Gardener! All levels complete.";
    } else {
        feedback.textContent = "Incorrect. Try again!";
        feedback.className = 'feedback error';
    }
});

nextBtn.addEventListener('click', () => { currentLevelIndex++; loadLevel(currentLevelIndex); });
loadLevel(0);
