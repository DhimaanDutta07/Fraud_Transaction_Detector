let userEmail = localStorage.getItem('email');
let userBalance = parseFloat(localStorage.getItem('balance')) || 0;

const balanceDisplay = document.getElementById('balance');
const transactionForm = document.getElementById('transactionForm');
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');

window.addEventListener('load', () => {
    if (!userEmail) {
        window.location.href = '/';
        return;
    }
    updateBalanceDisplay();
});

function updateBalanceDisplay() {
    balanceDisplay.textContent = '$' + userBalance.toFixed(2);
}

transactionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const amount = parseFloat(document.getElementById('amount').value);
    
    if (amount <= 0) {
        showModal('error', 'Invalid Amount', 'Please enter a valid amount');
        return;
    }
    
    showProcessing();
    
    try {
        const response = await fetch('/fraud/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: userEmail,
                amount: amount
            })
        });
        
        const data = await response.json();
        
        setTimeout(() => {
            if (data.status === 'approved') {
                userBalance = data.balance;
                localStorage.setItem('balance', userBalance);
                updateBalanceDisplay();
                showModal('approved', 'Transaction Approved ✓', 
                    `Amount: $${amount.toFixed(2)}\nConfidence: ${data.confidence}%\nNew Balance: $${data.balance.toFixed(2)}`);
            } else {
                showModal('rejected', 'Transaction Rejected ✗', 
                    `${data.message}\nConfidence: ${data.confidence}%`);
            }
            document.getElementById('amount').value = '';
        }, 1500);
        
    } catch (error) {
        showModal('error', 'Error', 'An error occurred during transaction');
    }
});

function showProcessing() {
    modal.classList.add('active');
    modalContent.innerHTML = `
        <div class="spinner"></div>
        <h2>Processing...</h2>
        <p>Analyzing transaction...</p>
    `;
}

function showModal(type, title, message) {
    modal.classList.add('active');
    
    let icon = '';
    if (type === 'approved') {
        icon = '<div class="approved-icon">✓</div>';
    } else if (type === 'rejected') {
        icon = '<div class="rejected-icon">✗</div>';
    }
    
    modalContent.innerHTML = `
        ${icon}
        <h2>${title}</h2>
        <p>${message.replace(/\n/g, '<br>')}</p>
        <button class="close-btn" onclick="closeModal()">Close</button>
    `;
}

function closeModal() {
    modal.classList.remove('active');
}

function logout() {
    localStorage.removeItem('email');
    localStorage.removeItem('balance');
    window.location.href = '/';
}