// Main page logic
document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication and update UI
    updateAuthUI();
    
    // Load system health info
    await loadSystemInfo();
    
    // Load user info if authenticated
    if (apiService.isAuthenticated()) {
        await loadUserInfo();
    }

    // Setup logout button
    setupLogoutButton();
});

// Update navigation based on authentication status
function updateAuthUI() {
    const logoutBtn = document.getElementById('logoutBtn');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (apiService.isAuthenticated()) {
        // Show logout button
        if (logoutBtn) {
            logoutBtn.style.display = 'inline-block';
        }
        
        // Hide login/register links
        navLinks.forEach(link => {
            if (link.href.includes('login') || link.href.includes('register')) {
                link.style.display = 'none';
            }
        });
    } else {
        // Hide logout button
        if (logoutBtn) {
            logoutBtn.style.display = 'none';
        }
        
        // Show login/register links
        navLinks.forEach(link => {
            if (link.href.includes('login') || link.href.includes('register')) {
                link.style.display = 'inline-block';
            }
        });
    }
}

// Load system health information
async function loadSystemInfo() {
    const systemInfoDiv = document.getElementById('systemInfo');
    
    try {
        const health = await apiService.getHealth();
        
        const html = `
            <div class="info-item">
                <h4>System Status</h4>
                <p><strong>Status:</strong> ${health.status}</p>
                <p><strong>Service:</strong> ${health.service}</p>
                <p class="timestamp">Last updated: ${new Date().toLocaleString()}</p>
            </div>
        `;
        
        systemInfoDiv.innerHTML = html;
    } catch (error) {
        console.error('Failed to load system info:', error);
        systemInfoDiv.innerHTML = `
            <p class="error">
                Failed to connect to service. 
                <br>Please ensure the backend is running at: ${apiService.baseURL}
            </p>
        `;
    }
}

// Load user information
async function loadUserInfo() {
    const userInfoSection = document.getElementById('userInfoSection');
    const userProfileDiv = document.getElementById('userProfile');
    
    try {
        const user = await apiService.getMe();
        
        const html = `
            <div class="profile-item">
                <p><strong>Username:</strong> ${user.username || 'N/A'}</p>
                <p><strong>Email:</strong> ${user.email || 'N/A'}</p>
                <p><strong>Full Name:</strong> ${user.fullname || 'N/A'}</p>
            </div>
        `;
        
        userProfileDiv.innerHTML = html;
        userInfoSection.style.display = 'block';
    } catch (error) {
        console.error('Failed to load user info:', error);
        // Silently fail if not authenticated
    }
}

// Setup logout button
function setupLogoutButton() {
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            if (confirm('Are you sure you want to logout?')) {
                apiService.logout();
                updateAuthUI();
                
                // Hide user info
                const userInfoSection = document.getElementById('userInfoSection');
                if (userInfoSection) {
                    userInfoSection.style.display = 'none';
                }
                
                // Show success message
                alert('Logged out successfully!');
                
                // Reload page
                location.reload();
            }
        });
    }
}

// Helper to display messages
function showMessage(elementId, message, type = 'info') {
    const messageDiv = document.getElementById(elementId);
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = `message show ${type}`;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageDiv.classList.remove('show');
        }, 5000);
    }
}

// Add styling for messages and info items
const styles = `
    <style>
        .info-item, .profile-item {
            padding: 1rem;
            background: #f9f9f9;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }
        
        .info-item h4, .profile-item h4 {
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        
        .timestamp {
            font-size: 0.85rem;
            color: #999;
            margin-top: 0.5rem;
        }
        
        .error {
            color: #721c24;
            background-color: #f8d7da;
            padding: 1rem;
            border-radius: 4px;
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', styles);
