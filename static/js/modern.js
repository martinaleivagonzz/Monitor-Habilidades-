// Tema oscuro/claro
const themeToggle = document.getElementById('themeToggle');
const currentTheme = localStorage.getItem('theme') || 'light';

// Aplicar tema guardado
document.documentElement.setAttribute('data-bs-theme', currentTheme);
updateThemeIcon();

themeToggle.addEventListener('click', () => {
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon();
});

function updateThemeIcon() {
    const theme = document.documentElement.getAttribute('data-bs-theme');
    const icon = themeToggle.querySelector('i');
    icon.className = theme === 'light' ? 'bi bi-moon' : 'bi bi-sun';
}

// Utilidades modernas
class ModernUI {
    static showLoading(element) {
        element.innerHTML = `
            <div class="text-center py-4">
                <div class="loader-modern"></div>
                <p class="text-muted mt-2">Cargando...</p>
            </div>
        `;
    }

    static showError(element, message) {
        element.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-warning display-4"></i>
                <p class="text-muted mt-2">${message}</p>
            </div>
        `;
    }

    static createSkillChip(skill, type = 'default') {
        const colors = {
            default: 'skill-chip',
            actual: 'skill-chip actual',
            recomendada: 'skill-chip recomendada'
        };
        
        return `
            <span class="${colors[type]}">
                <i class="bi bi-tag"></i>
                ${skill}
            </span>
        `;
    }

    static createMetricCard(icon, value, label, color = 'primary') {
        return `
            <div class="col-xl-3 col-md-6 mb-4">
                <div class="metric-card">
                    <div class="metric-icon">
                        <i class="bi ${icon}"></i>
                    </div>
                    <div class="metric-value">${value}</div>
                    <div class="metric-label">${label}</div>
                </div>
            </div>
        `;
    }

    static showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container');
        const alertId = 'alert-' + Date.now();
        
        const alertHTML = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        alertContainer.innerHTML = alertHTML;
        
        // Auto-remover después de 5 segundos
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) alert.remove();
        }, 5000);
    }
}

// API Utilities
class API {
    static async get(url) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Error:', error);
            ModernUI.showAlert('Error de conexión con el servidor', 'danger');
            return { success: false, message: 'Error de conexión' };
        }
    }

    static async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('API Error:', error);
            ModernUI.showAlert('Error de conexión con el servidor', 'danger');
            return { success: false, message: 'Error de conexión' };
        }
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Añadir animaciones a los elementos
    const animatedElements = document.querySelectorAll('.fade-in-up');
    animatedElements.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.1}s`;
    });
});
