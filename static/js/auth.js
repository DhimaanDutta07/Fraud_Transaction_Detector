const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const messageDiv = document.getElementById('message');

if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                localStorage.setItem('email', data.email);
                localStorage.setItem('balance', data.balance);
                window.location.href = '/dashboard';
            } else {
                showMessage(data.error || 'Login failed', 'error');
            }
        } catch (error) {
            showMessage('An error occurred', 'error');
        }
    });
}

if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                showMessage('Registration successful! Redirecting to login...', 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            } else {
                showMessage(data.error || 'Registration failed', 'error');
            }
        } catch (error) {
            showMessage('An error occurred', 'error');
        }
    });
}

function showMessage(msg, type) {
    if (messageDiv) {
        messageDiv.textContent = msg;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}