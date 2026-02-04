// API base URL - use relative path to work from any host
const API_URL = '/api';

// Global state
let currentSessionId = null;

// DOM elements
let chatMessages, chatInput, sendButton, totalCourses, courseTitles, themeToggle;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements after page loads
    chatMessages = document.getElementById('chatMessages');
    chatInput = document.getElementById('chatInput');
    sendButton = document.getElementById('sendButton');
    totalCourses = document.getElementById('totalCourses');
    courseTitles = document.getElementById('courseTitles');
    themeToggle = document.getElementById('themeToggle');

    setupEventListeners();
    createNewSession();
    loadCourseStats();
    initializeTheme();
});

// Event Listeners
/**
 * Sets up all event listeners for the application:
 * - Chat input and send button for message sending
 * - Theme toggle button with click and keyboard support
 * - Suggested question buttons for quick queries
 */
function setupEventListeners() {
    // Chat functionality
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    themeToggle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleTheme();
        }
    });

    // Suggested questions
    document.querySelectorAll('.suggested-item').forEach(button => {
        button.addEventListener('click', (e) => {
            const question = e.target.getAttribute('data-question');
            chatInput.value = question;
            sendMessage();
        });
    });
}


// Chat Functions
/**
 * Handles sending a chat message to the API.
 * - Disables input and send button during processing
 * - Adds user message to chat UI
 * - Shows loading animation
 * - Sends query to API with current session ID
 * - Handles response or error display
 * - Re-enables input and focuses chat input
 */
async function sendMessage() {
    const query = chatInput.value.trim();
    if (!query) return;

    // Disable input
    chatInput.value = '';
    chatInput.disabled = true;
    sendButton.disabled = true;

    // Add user message
    addMessage(query, 'user');

    // Add loading message - create a unique container for it
    const loadingMessage = createLoadingMessage();
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                session_id: currentSessionId
            })
        });

        if (!response.ok) throw new Error('Query failed');

        const data = await response.json();
        
        // Update session ID if new
        if (!currentSessionId) {
            currentSessionId = data.session_id;
        }

        // Replace loading message with response
        loadingMessage.remove();
        addMessage(data.answer, 'assistant', data.sources);

    } catch (error) {
        // Replace loading message with error
        loadingMessage.remove();
        addMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        chatInput.disabled = false;
        sendButton.disabled = false;
        chatInput.focus();
    }
}

/**
 * Creates a loading message element with animated dots.
 * Used to show a "thinking" indicator while waiting for API response.
 *
 * @returns {HTMLElement} The created loading message element
 */
function createLoadingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="loading">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    return messageDiv;
}

function addMessage(content, type, sources = null, isWelcome = false) {
    const messageId = Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}${isWelcome ? ' welcome-message' : ''}`;
    messageDiv.id = `message-${messageId}`;
    
    // Convert markdown to HTML for assistant messages
    const displayContent = type === 'assistant' ? marked.parse(content) : escapeHtml(content);
    
    let html = `<div class="message-content">${displayContent}</div>`;
    
    if (sources && sources.length > 0) {
        const parsedSources = sources.map(parseSource);
        html += `
            <details class="sources-collapsible">
                <summary class="sources-header">Sources</summary>
                <div class="sources-content">${parsedSources.join(', ')}</div>
            </details>
        `;
    }
    
    messageDiv.innerHTML = html;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return messageId;
}

/**
 * Escapes HTML special characters to prevent XSS attacks in user messages.
 * Uses textContent to safely set text, then retrieves innerHTML with escaped characters.
 *
 * @param {string} text - The text to escape
 * @returns {string} The escaped HTML string
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Parses a source string that may contain an embedded link.
 * Format: "display text" or "display text|||https://link.com"
 * Returns HTML for the source (clickable link if link present).
 */
function parseSource(source) {
    const delimiter = '|||';
    const parts = source.split(delimiter);
    const displayText = parts[0].trim();
    const link = parts.length > 1 ? parts[1].trim() : null;

    if (link && link.length > 0) {
        // Return clickable link that opens in new tab
        return `<a href="${escapeHtml(link)}" target="_blank" class="source-link">${escapeHtml(displayText)}</a>`;
    } else {
        // Return plain text
        return escapeHtml(displayText);
    }
}

// Removed removeMessage function - no longer needed since we handle loading differently

/**
 * Creates a new chat session by resetting the session ID and clearing chat messages.
 * Adds a welcome message to the chat interface.
 */
async function createNewSession() {
    currentSessionId = null;
    chatMessages.innerHTML = '';
    addMessage('Welcome to the Course Materials Assistant! I can help you with questions about courses, lessons and specific content. What would you like to know?', 'assistant', null, true);
}

/**
 * Loads course statistics from the API and updates the sidebar UI.
 * Fetches total course count and course titles, handles errors gracefully.
 */
async function loadCourseStats() {
    try {
        console.log('Loading course stats...');
        const response = await fetch(`${API_URL}/courses`);
        if (!response.ok) throw new Error('Failed to load course stats');

        const data = await response.json();
        console.log('Course data received:', data);

        // Update stats in UI
        if (totalCourses) {
            totalCourses.textContent = data.total_courses;
        }

        // Update course titles
        if (courseTitles) {
            if (data.course_titles && data.course_titles.length > 0) {
                courseTitles.innerHTML = data.course_titles
                    .map(title => `<div class="course-title-item">${title}</div>`)
                    .join('');
            } else {
                courseTitles.innerHTML = '<span class="no-courses">No courses available</span>';
            }
        }

    } catch (error) {
        console.error('Error loading course stats:', error);
        // Set default values on error
        if (totalCourses) {
            totalCourses.textContent = '0';
        }
        if (courseTitles) {
            courseTitles.innerHTML = '<span class="error">Failed to load courses</span>';
        }
    }
}

// Theme Functions
/**
 * Initializes the theme by loading the user's saved preference from localStorage.
 * If no preference is saved, defaults to dark theme.
 * Calls setTheme() to apply the loaded theme.
 */
function initializeTheme() {
    // Check for saved theme preference or use dark as default
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);
}

/**
 * Toggles between light and dark themes.
 * Reads the current theme from the toggle button's data-theme attribute,
 * determines the opposite theme, and calls setTheme() to apply it.
 * Saves the new theme preference to localStorage for persistence.
 */
function toggleTheme() {
    const currentTheme = themeToggle.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);

    // Save preference to localStorage
    localStorage.setItem('theme', newTheme);
}

/**
 * Applies the specified theme by updating CSS custom properties and button state.
 * Updates the toggle button's data-theme attribute and aria-label for accessibility.
 * Sets CSS variables for light theme or resets to dark theme defaults.
 * Adds smooth transition effects for theme changes.
 *
 * @param {string} theme - The theme to apply: 'light' or 'dark'
 */
function setTheme(theme) {
    // Update button state
    themeToggle.setAttribute('data-theme', theme);
    themeToggle.setAttribute('aria-label', `Toggle theme (currently ${theme} mode)`);

    // Update CSS variables for light theme
    if (theme === 'light') {
        document.documentElement.style.setProperty('--background', '#f8fafc');
        document.documentElement.style.setProperty('--surface', '#ffffff');
        document.documentElement.style.setProperty('--surface-hover', '#f1f5f9');
        document.documentElement.style.setProperty('--text-primary', '#0f172a');
        document.documentElement.style.setProperty('--text-secondary', '#64748b');
        document.documentElement.style.setProperty('--border-color', '#e2e8f0');
        document.documentElement.style.setProperty('--assistant-message', '#f1f5f9');
        document.documentElement.style.setProperty('--focus-ring', 'rgba(37, 99, 235, 0.1)');
        document.documentElement.style.setProperty('--shadow', '0 4px 6px -1px rgba(0, 0, 0, 0.1)');
    } else {
        // Reset to dark theme (default values)
        document.documentElement.style.setProperty('--background', '#0f172a');
        document.documentElement.style.setProperty('--surface', '#1e293b');
        document.documentElement.style.setProperty('--surface-hover', '#334155');
        document.documentElement.style.setProperty('--text-primary', '#f1f5f9');
        document.documentElement.style.setProperty('--text-secondary', '#94a3b8');
        document.documentElement.style.setProperty('--border-color', '#334155');
        document.documentElement.style.setProperty('--assistant-message', '#374151');
        document.documentElement.style.setProperty('--focus-ring', 'rgba(37, 99, 235, 0.2)');
        document.documentElement.style.setProperty('--shadow', '0 4px 6px -1px rgba(0, 0, 0, 0.3)');
    }

    // Add smooth transition for theme change
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';

    // Remove transition after animation completes
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
}