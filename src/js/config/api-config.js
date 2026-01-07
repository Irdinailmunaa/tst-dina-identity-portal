// API Configuration
const API_CONFIG = {
    // Local development
    // baseURL: 'http://localhost:8000',
    
    // Production - STB deployment
    baseURL: 'https://dina.theokaitou.my.id',
    
    // Endpoints
    endpoints: {
        auth: {
            login: '/auth/login',
            register: '/auth/register',
            me: '/auth/me'
        },
        health: '/health'
    },
    
    // Token storage
    tokenKey: 'tixgo_token',
    userKey: 'tixgo_user'
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
