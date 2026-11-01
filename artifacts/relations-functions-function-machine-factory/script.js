const levels = [
    // BUILD MODE - Basics
    { mode: 'build', level: 1, inputs: [1, 2, 3, 4], outputs: [3, 4, 5, 6], gears: ['+1', '+2', '+3', '-1'], numSlots: 1 },
    { mode: 'build', level: 2, inputs: [2, 4, 6, 8], outputs: [4, 8, 12, 16], gears: ['*2', '/2', '*3', '+2'], numSlots: 1 },
    { mode: 'build', level: 3, inputs: [1, 2, 3, 4], outputs: [5, 7, 9, 11], gears: ['*2', '+3', '-1', '*3', '+2'], numSlots: 2 },
    
    // GUESS MODE - Single Step
    { mode: 'guess', level: 4, inputs: [1, 3, 5, 7], outputs: [4, 6, 8, 10], lockedGears: ['+3'], numSlots: 1 },
    { mode: 'guess', level: 5, inputs: [2, 4, 5, 10], outputs: [6, 12, 15, 30], lockedGears: ['*3'], numSlots: 1 },
    
    // BUILD MODE - Harder / Negatives
    { mode: 'build', level: 6, inputs: [2, 4, 6], outputs: [1, 2, 3], gears: ['/2', '-1', '+1', '*2'], numSlots: 1 },
    { mode: 'build', level: 7, inputs: [1, 3, 5], outputs: [1, 9, 17], gears: ['*4', '-3', '*3', '+2', '/2'], numSlots: 2 },
    
    // GUESS MODE - Two Step
    { mode: 'guess', level: 8, inputs: [2, 4, 6], outputs: [7, 11, 15], lockedGears: ['*2', '+3'], numSlots: 2 },
    
    // BUILD MODE - 3 Options
    { mode: 'build', level: 9, inputs: [1, 2, 3], outputs: [4, 9, 14], gears: ['*5', '-1', '+2', '*4', '-2'], numSlots: 2 },
    
    // GUESS MODE - Tricky Reversal
    { mode: 'guess', level: 10, inputs: [5, 10, 15], outputs: [2, 3, 4], lockedGears: ['/5', '+1'], numSlots: 2 }
];

let currentLevelIndex = 0;
let draggedGear = null;

const dataBody = document.getElementById('data-body');
const inventoryContainer = document.getElementById('gear-inventory');
const machineSlots = document.getElementById('machine-slots');
const testBtn = document.getElementById('test-btn');
const nextBtn = document.getElementById('next-btn');
const feedback = document.getElementById('feedback-message');
const levelDisplay = document.getElementById('level-display');
const modeDisplay = document.getElementById('mode-display');
const machineInstruction = document.getElementById('machine-instruction');
const inventoryInstruction = document.getElementById('inventory-instruction');

function loadLevel(index) {
    const levelData = levels[index];
    levelDisplay.textContent = levelData.level;
    modeDisplay.textContent = levelData.mode === 'build' ? 'Build Mode' : 'Reverse Engineering (Guess)';
    
    // Reset UI
    dataBody.innerHTML = '';
    inventoryContainer.innerHTML = '';
    machineSlots.innerHTML = '';
    feedback.textContent = '';
    feedback.className = 'feedback';
    nextBtn.classList.add('hidden');
    testBtn.classList.remove('hidden');

    if (levelData.mode === 'build') {
        machineInstruction.textContent = "Insert Gears Here";
        inventoryInstruction.textContent = "Drag and drop gears into the machine.";
        
        // Populate Build Table
        levelData.inputs.forEach((input, i) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${input}</td><td>${levelData.outputs[i]}</td><td id="output-${i}">-</td>`;
            dataBody.appendChild(tr);
        });

        // Populate Gears
        levelData.gears.forEach(gearVal => {
            const gear = document.createElement('div');
            gear.className = 'gear';
            gear.textContent = gearVal;
            gear.draggable = true;
            gear.addEventListener('dragstart', handleDragStart);
            gear.addEventListener('dragend', handleDragEnd);
            inventoryContainer.appendChild(gear);
        });

        // Populate Empty Slots
        for (let i = 0; i < levelData.numSlots; i++) {
            const slot = document.createElement('div');
            slot.className = 'slot';
            slot.dataset.index = i;
            slot.addEventListener('dragover', handleDragOver);
            slot.addEventListener('dragleave', handleDragLeave);
            slot.addEventListener('drop', handleDrop);
            machineSlots.appendChild(slot);
        }
    } else {
        // Guess Mode
        machineInstruction.textContent = "Locked Machine Gears";
        inventoryInstruction.textContent = "Machine is sealed. Work backwards to find the inputs!";
        
        // Populate Guess Table
        levelData.outputs.forEach((output, i) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="number" class="input-guess" id="guess-${i}" placeholder="?"></td>
                <td>${output}</td>
                <td id="output-${i}">-</td>
            `;
            dataBody.appendChild(tr);
        });

        // Populate Locked Slots
        levelData.lockedGears.forEach(gearVal => {
            const slot = document.createElement('div');
            slot.className = 'slot';
            const gear = document.createElement('div');
            gear.className = 'gear locked';
            gear.textContent = gearVal;
            slot.appendChild(gear);
            machineSlots.appendChild(slot);
        });
    }
}

// Drag and Drop Logic (Build Mode)
function handleDragStart(e) {
    draggedGear = this;
    setTimeout(() => this.style.display = 'none', 0);
}

function handleDragEnd(e) {
    this.style.display = 'flex';
    draggedGear = null;
}

function handleDragOver(e) {
    e.preventDefault();
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    this.classList.remove('drag-over');
    if (draggedGear) {
        if (this.children.length > 0) {
            inventoryContainer.appendChild(this.children[0]);
        }
        this.appendChild(draggedGear);
    }
}

inventoryContainer.addEventListener('dragover', e => e.preventDefault());
inventoryContainer.addEventListener('drop', function(e) {
    if (draggedGear) {
        this.appendChild(draggedGear);
    }
});

// Math Engine
function applyOperation(value, operationStr) {
    const operator = operationStr[0];
    const operand = parseFloat(operationStr.substring(1));
    
    switch (operator) {
        case '+': return value + operand;
        case '-': return value - operand;
        case '*': return value * operand;
        case '/': return value / operand;
        default: return value;
    }
}

testBtn.addEventListener('click', () => {
    const levelData = levels[currentLevelIndex];
    let allCorrect = true;

    if (levelData.mode === 'build') {
        const slots = document.querySelectorAll('.slot');
        const operations = Array.from(slots).map(slot => {
            return slot.children.length > 0 ? slot.children[0].textContent : null;
        });

        if (operations.includes(null)) {
            feedback.textContent = 'Please fill all machine slots!';
            feedback.className = 'feedback error';
            return;
        }

        levelData.inputs.forEach((input, i) => {
            let currentValue = input;
            operations.forEach(op => { currentValue = applyOperation(currentValue, op); });
            const outputCell = document.getElementById(`output-${i}`);
            outputCell.textContent = currentValue;

            if (currentValue !== levelData.outputs[i]) {
                allCorrect = false;
                outputCell.style.color = '#e74c3c';
            } else {
                outputCell.style.color = '#2ecc71';
            }
        });
    } else {
        // Guess mode logic
        const operations = levelData.lockedGears;
        
        // Validation check for empty inputs
        const emptyInputs = Array.from(document.querySelectorAll('.input-guess')).some(inp => inp.value === '');
        if (emptyInputs) {
            feedback.textContent = 'Please fill out all missing inputs!';
            feedback.className = 'feedback error';
            return;
        }

        levelData.outputs.forEach((targetOutput, i) => {
            const guessInput = document.getElementById(`guess-${i}`).value;
            let currentValue = parseFloat(guessInput);
            
            operations.forEach(op => { currentValue = applyOperation(currentValue, op); });
            
            const outputCell = document.getElementById(`output-${i}`);
            outputCell.textContent = currentValue;

            if (currentValue !== targetOutput) {
                allCorrect = false;
                outputCell.style.color = '#e74c3c';
            } else {
                outputCell.style.color = '#2ecc71';
            }
        });
    }

    if (allCorrect) {
        feedback.textContent = 'Success! Correct logic applied.';
        feedback.className = 'feedback success';
        testBtn.classList.add('hidden');
        
        if (currentLevelIndex < levels.length - 1) {
            nextBtn.classList.remove('hidden');
        } else {
            feedback.textContent = 'Congratulations! You beat all 10 levels!';
        }
    } else {
        feedback.textContent = levelData.mode === 'build' ? 'Machine malfunction! Outputs do not match.' : 'Incorrect inputs! Outputs do not match the targets.';
        feedback.className = 'feedback error';
    }
});

nextBtn.addEventListener('click', () => {
    currentLevelIndex++;
    loadLevel(currentLevelIndex);
});

// Initialize game
loadLevel(0);
