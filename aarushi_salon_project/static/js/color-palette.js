/**
 * Color Palette Switching System
 * Professional salon theme color management
 */

class ColorPaletteManager {
    constructor() {
        this.currentPalette = 'default';
        this.palettes = {};
        this.init();
    }

    async init() {
        // Load available palettes
        await this.loadPalettes();
        
        // Load current theme
        await this.loadCurrentTheme();
        
        // Create color toggle UI
        this.createColorToggle();
        
        // Apply current palette
        this.applyPalette(this.currentPalette);
    }

    async loadPalettes() {
        try {
            const response = await fetch('/api/color-palettes/');
            const data = await response.json();
            
            this.palettes = {};
            data.forEach(palette => {
                this.palettes[palette.name] = palette;
            });
        } catch (error) {
            console.error('Error loading color palettes:', error);
        }
    }

    async loadCurrentTheme() {
        try {
            const response = await fetch('/api/current-theme/');
            const data = await response.json();
            this.currentPalette = data.palette;
        } catch (error) {
            console.error('Error loading current theme:', error);
            this.currentPalette = 'default';
        }
    }

    createColorToggle() {
        // Create color toggle container
        const toggleContainer = document.createElement('div');
        toggleContainer.className = 'color-toggle-container';
        toggleContainer.innerHTML = `
            <div class="color-toggle-dropdown" id="colorToggleDropdown">
                <h6>Choose Theme</h6>
                <div class="color-options">
                    ${Object.values(this.palettes).map(palette => `
                        <div class="color-option ${palette.name === this.currentPalette ? 'active' : ''}" 
                             data-palette="${palette.name}">
                            <div class="color-preview" style="background: linear-gradient(135deg, ${palette.primary_color}, ${palette.secondary_color});"></div>
                            <span class="color-option-text">${palette.display_name}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            <button class="color-toggle-btn" id="colorToggleBtn" title="Change Color Theme">
                <i class="fas fa-palette"></i>
            </button>
        `;

        document.body.appendChild(toggleContainer);

        // Add event listeners
        const toggleBtn = document.getElementById('colorToggleBtn');
        const dropdown = document.getElementById('colorToggleDropdown');
        const colorOptions = toggleContainer.querySelectorAll('.color-option');

        // Toggle dropdown
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!toggleContainer.contains(e.target)) {
                dropdown.classList.remove('show');
            }
        });

        // Handle color option selection
        colorOptions.forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const paletteName = option.dataset.palette;
                this.setPalette(paletteName);
                dropdown.classList.remove('show');
            });
        });

        // Update toggle button style based on current palette
        this.updateToggleButton();
    }

    updateToggleButton() {
        const toggleBtn = document.getElementById('colorToggleBtn');
        if (toggleBtn && this.palettes[this.currentPalette]) {
            const palette = this.palettes[this.currentPalette];
            toggleBtn.style.background = `linear-gradient(135deg, ${palette.primary_color}, ${palette.secondary_color})`;
        }
    }

    async setPalette(paletteName) {
        if (!this.palettes[paletteName]) {
            console.error('Invalid palette:', paletteName);
            return;
        }

        try {
            const response = await fetch('/api/set-palette/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ palette: paletteName })
            });

            const data = await response.json();
            
            if (data.success) {
                this.currentPalette = paletteName;
                this.applyPalette(paletteName);
                this.updateActiveOption();
                this.updateToggleButton();
                this.showNotification(data.message);
            } else {
                console.error('Error setting palette:', data.error);
            }
        } catch (error) {
            console.error('Error setting palette:', error);
        }
    }

    applyPalette(paletteName) {
        const palette = this.palettes[paletteName];
        if (!palette) return;

        // Remove existing palette classes
        document.body.className = document.body.className.replace(/color-palette-\w+/g, '');
        
        // Add new palette class
        document.body.classList.add(`color-palette-${paletteName}`);

        // Update CSS custom properties
        const root = document.documentElement;
        root.style.setProperty('--primary-color', palette.primary_color);
        root.style.setProperty('--secondary-color', palette.secondary_color);
        root.style.setProperty('--accent-color', palette.accent_color);

        // Update gradients
        root.style.setProperty('--primary-gradient', 
            `linear-gradient(135deg, ${palette.primary_color}, ${palette.secondary_color})`);
        root.style.setProperty('--secondary-gradient', 
            `linear-gradient(135deg, ${palette.secondary_color}, ${palette.primary_color})`);

        // Store in localStorage for persistence
        localStorage.setItem('selectedColorPalette', paletteName);
    }

    updateActiveOption() {
        const colorOptions = document.querySelectorAll('.color-option');
        colorOptions.forEach(option => {
            option.classList.remove('active');
            if (option.dataset.palette === this.currentPalette) {
                option.classList.add('active');
            }
        });
    }

    showNotification(message) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'color-palette-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            font-weight: 600;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    // Load saved palette from localStorage
    loadSavedPalette() {
        const savedPalette = localStorage.getItem('selectedColorPalette');
        if (savedPalette && this.palettes[savedPalette]) {
            this.currentPalette = savedPalette;
            this.applyPalette(savedPalette);
        }
    }
}

// Initialize color palette manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.colorPaletteManager = new ColorPaletteManager();
});

// Export for global access
window.ColorPaletteManager = ColorPaletteManager;

