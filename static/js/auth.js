// Authentication Module

// Mock user data - in a real app, this would be stored securely and managed by a backend
const USERS = [
    {
        id: 1,
        name: 'Admin User',
        email: 'admin@betulabla.org',
        password: 'admin123',
        role: 'admin'
    },
    {
        id: 2,
        name: 'Coordinator User',
        email: 'coordinator@betulabla.org',
        password: 'coord123',
        role: 'coordinator'
    }
];

// Check if user is logged in
function isLoggedIn() {
    const user = sessionStorage.getItem('currentUser');
    return !!user;
}

// Get current user
function getCurrentUser() {
    const userString = sessionStorage.getItem('currentUser');
    return userString ? JSON.parse(userString) : null;
}

// Login function
function login(email, password) {
    const user = USERS.find(u => u.email === email && u.password === password);
    
    if (user) {
        // Create a copy of the user without the password
        const { password, ...userWithoutPassword } = user;
        
        // Store in session storage (in a real app, would use secure HTTP-only cookies)
        sessionStorage.setItem('currentUser', JSON.stringify(userWithoutPassword));
        
        // Redirect based on role
        if (user.role === 'admin') {
            window.location.href = 'admin-dashboard.html';
        } else if (user.role === 'coordinator') {
            window.location.href = 'coordinator-dashboard.html';
        }
        
        return true;
    }
    
    return false;
}

// Logout function
function logout() {
    sessionStorage.removeItem('currentUser');
    window.location.href = 'index.html';
}

// Check authentication on restricted pages
function checkAuth() {
    const currentPath = window.location.pathname;
    
    // Pages that require authentication
    const adminPages = [
        '/admin-dashboard.html', 
        '/admin-staff.html', 
        '/admin-settings.html'
    ];
    
    const coordinatorPages = [
        '/coordinator-dashboard.html',
        '/coordinator-orphans.html',
        '/coordinator-boreholes.html',
        '/coordinator-reports.html'
    ];
    
    const requiresAdmin = adminPages.some(page => currentPath.includes(page));
    const requiresCoordinator = coordinatorPages.some(page => currentPath.includes(page));
    
    if (requiresAdmin || requiresCoordinator) {
        const user = getCurrentUser();
        
        if (!user) {
            // Not logged in
            window.location.href = 'login.html';
            return;
        }
        
        if (requiresAdmin && user.role !== 'admin') {
            // Not admin but trying to access admin page
            window.location.href = 'login.html';
            return;
        }
        
        if (requiresCoordinator && user.role !== 'coordinator' && user.role !== 'admin') {
            // Not coordinator but trying to access coordinator page
            window.location.href = 'login.html';
            return;
        }
    }
}

// Initialize auth-related event handlers
function initAuth() {
    // Check if on login page
    if (window.location.pathname.includes('login.html')) {
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                const success = login(email, password);
                
                if (!success) {
                    document.getElementById('loginError').style.display = 'block';
                }
            });
        }
    }
    
    // Set up logout buttons
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
    
    // Update UI based on auth state
    updateUIForAuthState();
}

// Update UI elements based on auth state
function updateUIForAuthState() {
    const user = getCurrentUser();
    
    // Update navigation
    const loginBtn = document.querySelector('a[href="login.html"]');
    
    if (loginBtn && user) {
        // If logged in, change login button to dashboard link
        loginBtn.textContent = 'Dashboard';
        if (user.role === 'admin') {
            loginBtn.href = 'admin-dashboard.html';
        } else {
            loginBtn.href = 'coordinator-dashboard.html';
        }
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    initAuth();
});