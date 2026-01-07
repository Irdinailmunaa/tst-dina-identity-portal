// Authentication handling
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        handleLoginPage();
    }
    
    if (registerForm) {
        handleRegisterPage();
    }
});

// Handle login page
function handleLoginPage() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');
    
    // Password visibility toggle
    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
    }
    
    // Form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous messages
        if (errorMessage) errorMessage.textContent = '';
        if (successMessage) successMessage.textContent = '';
        
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        
        // Validation
        if (!username) {
            showError(errorMessage, 'Username is required');
            return;
        }
        
        if (!password) {
            showError(errorMessage, 'Password is required');
            return;
        }
        
        try {
            // Disable button during submission
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Logging in...';
            
            // Call API
            const response = await apiService.login(username, password);
            
            // Check if token was set
            if (apiService.getToken()) {
                showSuccess(successMessage, 'Login successful! Redirecting...');
                
                // Redirect after short delay
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                showError(errorMessage, response.message || 'Login failed');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Login';
            }
        } catch (error) {
            console.error('Login error:', error);
            
            let errorMsg = 'Login failed. Please try again.';
            
            if (error.message) {
                errorMsg = error.message;
            } else if (error.response?.message) {
                errorMsg = error.response.message;
            }
            
            showError(errorMessage, errorMsg);
            
            // Re-enable button
            const submitBtn = loginForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Login';
        }
    });
}

// Handle register page
function handleRegisterPage() {
    const registerForm = document.getElementById('registerForm');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');
    const fullnameInput = document.getElementById('fullname');
    const emailInput = document.getElementById('email');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirm = document.getElementById('toggleConfirm');
    
    // Password visibility toggles
    if (togglePassword) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            togglePassword.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
    }
    
    if (toggleConfirm) {
        toggleConfirm.addEventListener('click', () => {
            const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            confirmPasswordInput.setAttribute('type', type);
            toggleConfirm.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
    }
    
    // Form submission
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous messages
        if (errorMessage) errorMessage.textContent = '';
        if (successMessage) successMessage.textContent = '';
        
        const fullname = fullnameInput.value.trim();
        const email = emailInput.value.trim();
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        
        // Validation
        if (!fullname) {
            showError(errorMessage, 'Full name is required');
            return;
        }
        
        if (!email) {
            showError(errorMessage, 'Email is required');
            return;
        }
        
        // Email validation
        if (!isValidEmail(email)) {
            showError(errorMessage, 'Please enter a valid email address');
            return;
        }
        
        if (!username) {
            showError(errorMessage, 'Username is required');
            return;
        }
        
        if (username.length < 3) {
            showError(errorMessage, 'Username must be at least 3 characters');
            return;
        }
        
        if (!password) {
            showError(errorMessage, 'Password is required');
            return;
        }
        
        if (password.length < 6) {
            showError(errorMessage, 'Password must be at least 6 characters');
            return;
        }
        
        if (password !== confirmPassword) {
            showError(errorMessage, 'Passwords do not match');
            return;
        }
        
        try {
            // Disable button during submission
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating account...';
            
            // Call API
            const response = await apiService.register(fullname, email, username, password);
            
            // Success - clear form and show message
            registerForm.reset();
            showSuccess(successMessage, 'Account created successfully! Redirecting to login...');
            
            // Redirect after short delay
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        } catch (error) {
            console.error('Registration error:', error);
            
            let errorMsg = 'Registration failed. Please try again.';
            
            if (error.message) {
                errorMsg = error.message;
            } else if (error.response?.message) {
                errorMsg = error.response.message;
            } else if (error.response?.detail) {
                errorMsg = error.response.detail;
            }
            
            showError(errorMessage, errorMsg);
            
            // Re-enable button
            const submitBtn = registerForm.querySelector('button[type="submit"]');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });
}

// Helper function to show error message
function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.className = 'message show error';
        element.style.display = 'block';
    }
}

// Helper function to show success message
function showSuccess(element, message) {
    if (element) {
        element.textContent = message;
        element.className = 'message show success';
        element.style.display = 'block';
    }
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add message styling
const styles = `
    <style>
        .message {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 4px;
            display: none;
            animation: slideIn 0.3s ease-in-out;
        }
        
        .message.show {
            display: block;
        }
        
        .message.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .message.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', styles);
