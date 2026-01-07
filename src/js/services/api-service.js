// API Service - handles all API calls to Identity Service
class APIService {
    constructor(config = API_CONFIG) {
        this.baseURL = config.baseURL;
        this.endpoints = config.endpoints;
        this.tokenKey = config.tokenKey;
    }

    // Get authentication token from localStorage
    getToken() {
        return localStorage.getItem(this.tokenKey);
    }

    // Set authentication token in localStorage
    setToken(token) {
        if (token) {
            localStorage.setItem(this.tokenKey, token);
        } else {
            localStorage.removeItem(this.tokenKey);
        }
    }

    // Make HTTP request with error handling
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        // Add authorization header if token exists
        if (!options.headers) {
            options.headers = {};
        }
        
        const token = this.getToken();
        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Add Content-Type if not set
        if (!options.headers['Content-Type'] && options.body) {
            options.headers['Content-Type'] = 'application/json';
        }

        try {
            const response = await fetch(url, options);
            
            // Handle 401 Unauthorized - token expired
            if (response.status === 401) {
                this.setToken(null);
                // Optionally redirect to login
                // window.location.href = 'login.html';
            }

            const data = await response.json().catch(() => ({}));
            
            if (!response.ok) {
                throw {
                    status: response.status,
                    message: data.detail || data.message || 'Request failed',
                    data: data
                };
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Auth endpoints
    async login(username, password) {
        const response = await this.request(this.endpoints.auth.login, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
        }
        
        return response;
    }

    async register(fullname, email, username, password) {
        return await this.request(this.endpoints.auth.register, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                fullname, 
                email, 
                username, 
                password 
            })
        });
    }

    async getMe() {
        return await this.request(this.endpoints.auth.me, {
            method: 'GET'
        });
    }

    async getHealth() {
        return await this.request(this.endpoints.health, {
            method: 'GET'
        });
    }

    // Logout
    logout() {
        this.setToken(null);
        localStorage.removeItem('tixgo_user');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getToken();
    }
}

// Create global instance
const apiService = new APIService();
