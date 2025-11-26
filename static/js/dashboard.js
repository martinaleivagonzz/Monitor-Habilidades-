// Estado global del dashboard
let dashboardData = {
    metricas: {},
    matriz: [],
    graficos: {}
};

// Inicialización cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    cargarDashboard();
    setupEventListeners();
});

function setupEventListeners() {
    // Actualizar datos cada 30 segundos
    setInterval(cargarDashboard, 30000);
}

async function cargarDashboard() {
    try {
        // Mostrar loading
        ModernUI.showLoading(document.getElementById('priorizacion-chart'));
        ModernUI.showLoading(document.getElementById('tabla-habilidades-body'));

        // Cargar datos del dashboard
        const data = await API.get('/api/dashboard-data');
        
        if (data.success) {
            dashboardData = data;
            actualizarMetricas(data.metricas);
            renderizarGraficoBarras(data.bar_chart);
            renderizarTablaHabilidades(data.matriz_data);
        } else {
            ModernUI.showAlert('Error cargando datos del dashboard', 'danger');
        }
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        ModernUI.showAlert('Error de conexión', 'danger');
    }
}

function actualizarMetricas(metricas) {
    document.getElementById('metric-habilidades').textContent = metricas.total_habilidades;
    document.getElementById('metric-prioridad').textContent = metricas.alta_prioridad;
    document.getElementById('metric-puntuacion').textContent = metricas.puntuacion_promedio + '%';
    document.getElementById('metric-usuarios').textContent = metricas.total_usuarios;
}

function renderizarGraficoBarras(chartData) {
    const container = document.getElementById('priorizacion-chart');
    
    if (chartData && chartData.data) {
        Plotly.newPlot(container, chartData.data, chartData.layout, {
            responsive: true,
            displayModeBar: true,
            displaylogo: false
        });
    } else {
        container.innerHTML = `
            <div class="text-center py-4">
                <i class="bi bi-exclamation-triangle text-warning display-4"></i>
                <p class="text-muted mt-2">No se pudieron cargar los gráficos</p>
            </div>
        `;
    }
}

function renderizarTablaHabilidades(matriz) {
    const tbody = document.getElementById('tabla-habilidades-body');
    
    if (!matriz || matriz.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center py-4">
                    <p class="text-muted">No hay datos disponibles</p>
                </td>
            </tr>
        `;
        return;
    }

    let html = '';
    matriz.forEach((habilidad, index) => {
        const badgeClass = getBadgeClass(habilidad.importancia);
        const categoria = categorizarHabilidad(habilidad.skill);
        
        html += `
            <tr class="fade-in-up" style="animation-delay: ${index * 0.05}s">
                <td>
                    <strong>${habilidad.skill}</strong>
                </td>
                <td>
                    <div class="progress" style="height: 8px;">
                        <div class="progress-bar ${badgeClass.replace('badge-', 'bg-')}" 
                             role="progressbar" 
                             style="width: ${habilidad.porcentaje_mercado}%"
                             aria-valuenow="${habilidad.porcentaje_mercado}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                        </div>
                    </div>
                    <small class="text-muted">${habilidad.porcentaje_mercado}%</small>
                </td>
                <td>
                    <span class="badge ${badgeClass}">${habilidad.importancia}</span>
                </td>
                <td>
                    <small class="text-muted">${categoria}</small>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function getBadgeClass(importancia) {
    switch(importancia.toLowerCase()) {
        case 'crítica': return 'badge-high';
        case 'alta': return 'badge-medium';
        case 'media': return 'badge-low';
        default: return 'badge-secondary';
    }
}

function categorizarHabilidad(habilidad) {
    const techSkills = ['python', 'sql', 'machine learning', 'power bi', 'tableau', 'excel', 'spark', 'tensorflow'];
    const businessSkills = ['business intelligence', 'kpi', 'análisis financiero', 'storytelling'];
    const managementSkills = ['project management', 'gestión de proyectos', 'scrum', 'agile'];
    
    const skillLower = habilidad.toLowerCase();
    
    if (techSkills.some(tech => skillLower.includes(tech))) return '💻 Técnica';
    if (businessSkills.some(business => skillLower.includes(business))) return '📊 Negocio';
    if (managementSkills.some(management => skillLower.includes(management))) return '👥 Gestión';
    
    return '📈 Análisis';
}

// Exportar para uso global
window.cargarDashboard = cargarDashboard;
