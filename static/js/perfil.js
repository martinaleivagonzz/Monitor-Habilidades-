// Estado del perfil
let perfilState = {
    usuarios: {},
    usuarioSeleccionado: null
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('usuario-selector')) {
        cargarUsuarios();
        setupPerfilEventListeners();
    }
});

function setupPerfilEventListeners() {
    const selector = document.getElementById('usuario-selector');
    selector.addEventListener('change', handleUsuarioChange);
}

async function cargarUsuarios() {
    try {
        const data = await API.get('/api/usuarios');
        
        if (data.success && Object.keys(data.usuarios).length > 0) {
            perfilState.usuarios = data.usuarios;
            renderUsuarioSelector(data.usuarios);
            document.getElementById('estado-vacio').style.display = 'none';
        } else {
            document.getElementById('perfil-contenido').style.display = 'none';
            document.getElementById('estado-vacio').style.display = 'block';
        }
    } catch (error) {
        console.error('Error cargando usuarios:', error);
        document.getElementById('perfil-contenido').style.display = 'none';
        document.getElementById('estado-vacio').style.display = 'block';
    }
}

function renderUsuarioSelector(usuarios) {
    const selector = document.getElementById('usuario-selector');
    let html = '<option value="">Selecciona un usuario...</option>';
    
    Object.keys(usuarios).forEach(userId => {
        const usuario = usuarios[userId];
        html += `<option value="${userId}">${usuario.nombre} (${userId})</option>`;
    });
    
    selector.innerHTML = html;
}

async function handleUsuarioChange(event) {
    const userId = event.target.value;
    
    if (!userId) {
        document.getElementById('perfil-contenido').style.display = 'none';
        return;
    }
    
    perfilState.usuarioSeleccionado = perfilState.usuarios[userId];
    await cargarPerfilUsuario(perfilState.usuarioSeleccionado);
}

async function cargarPerfilUsuario(usuario) {
    if (!usuario) return;
    
    // Mostrar loading
    document.getElementById('perfil-contenido').style.display = 'block';
    ModernUI.showLoading(document.getElementById('grafico-brechas'));
    ModernUI.showLoading(document.getElementById('plan-accion'));

    // Actualizar información básica
    document.getElementById('usuario-nombre').textContent = usuario.nombre;
    document.getElementById('usuario-experiencia').textContent = usuario.experiencia;
    document.getElementById('usuario-objetivo').textContent = usuario.objetivo;
    document.getElementById('puntuacion-adecuacion').textContent = usuario.puntuacion_adecuacion + '%';

    // Actualizar métricas
    actualizarMetricasUsuario(usuario);

    // Renderizar habilidades
    renderHabilidadesUsuario(usuario);

    // Generar gráfico de brechas
    generarGraficoBrechas(usuario);

    // Generar plan de acción
    generarPlanAccion(usuario);
}

function actualizarMetricasUsuario(usuario) {
    const metricasHtml = `
        ${ModernUI.createMetricCard('bi-check-circle', usuario.skills_actuales.length, 'Habilidades Actuales', 'success')}
        ${ModernUI.createMetricCard('bi-lightbulb', usuario.recomendaciones.length, 'Recomendaciones', 'primary')}
        ${ModernUI.createMetricCard('bi-graph-up', usuario.puntuacion_adecuacion + '%', 'Adecuación', 'info')}
        ${ModernUI.createMetricCard('bi-exclamation-triangle', usuario.brecha_principal, 'Brecha Principal', 'warning')}
    `;
    
    document.getElementById('metricas-usuario').innerHTML = metricasHtml;
}

function renderHabilidadesUsuario(usuario) {
    // Habilidades actuales
    const actualesContainer = document.getElementById('habilidades-actuales-list');
    actualesContainer.innerHTML = usuario.skills_actuales.map(skill => 
        ModernUI.createSkillChip(skill, 'actual')
    ).join('');

    // Habilidades recomendadas
    const recomendadasContainer = document.getElementById('habilidades-recomendadas-list');
    recomendadasContainer.innerHTML = usuario.recomendaciones.map(skill => 
        ModernUI.createSkillChip(skill, 'recomendada')
    ).join('');
}

function generarGraficoBrechas(usuario) {
    const container = document.getElementById('grafico-brechas');
    
    // Datos para el gráfico
    const habilidades = [...usuario.skills_actuales, ...usuario.recomendaciones];
    const tipos = [
        ...usuario.skills_actuales.map(() => 'Actual'),
        ...usuario.recomendaciones.map(() => 'Recomendada')
    ];
    
    const data = [{
        x: habilidades,
        y: tipos,
        type: 'bar',
        orientation: 'h',
        marker: {
            color: tipos.map(tipo => tipo === 'Actual' ? '#10b981' : '#6366f1')
        }
    }];
    
    const layout = {
        title: 'Análisis de Brechas de Habilidades',
        xaxis: { title: 'Habilidades' },
        yaxis: { title: '' },
        showlegend: false,
        height: 400,
        margin: { l: 150 }
    };
    
    Plotly.newPlot(container, data, layout, {
        responsive: true,
        displayModeBar: true,
        displaylogo: false
    });
}

function generarPlanAccion(usuario) {
    const container = document.getElementById('plan-accion');
    
    const planHtml = `
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card-modern h-100">
                    <div class="card-header bg-primary text-white">
                        <h6 class="mb-0">📅 Plan Inmediato (1-3 meses)</h6>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            ${usuario.recomendaciones.slice(0, 3).map(skill => `
                                <li class="mb-2">
                                    <i class="bi bi-check-circle text-success me-2"></i>
                                    <strong>${skill}</strong>
                                    <br>
                                    <small class="text-muted">Cursos recomendados y práctica guiada</small>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="card-modern h-100">
                    <div class="card-header bg-success text-white">
                        <h6 class="mb-0">🎯 Plan a Mediano Plazo (3-6 meses)</h6>
                    </div>
                    <div class="card-body">
                        <ul class="list-unstyled">
                            ${usuario.recomendaciones.slice(3, 6).map(skill => `
                                <li class="mb-2">
                                    <i class="bi bi-lightbulb text-warning me-2"></i>
                                    <strong>${skill}</strong>
                                    <br>
                                    <small class="text-muted">Proyectos prácticos y especialización</small>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card-modern mt-3">
            <div class="card-header bg-info text-white">
                <h6 class="mb-0">💡 Recomendaciones Personalizadas</h6>
            </div>
            <div class="card-body">
                <p>Basado en tu perfil de <strong>${usuario.experiencia}</strong> y objetivo de <strong>${usuario.objetivo}</strong>, te recomendamos:</p>
                <ul>
                    <li>Enfócate en desarrollar <strong>${usuario.brecha_principal}</strong> como prioridad máxima</li>
                    <li>Combina aprendizaje teórico con proyectos prácticos</li>
                    <li>Dedica al menos 5 horas semanales a tu desarrollo profesional</li>
                    <li>Revisa la sección de Recursos para materiales específicos</li>
                </ul>
            </div>
        </div>
    `;
    
    container.innerHTML = planHtml;
}

// Exportar funciones globales
window.cargarUsuarios = cargarUsuarios;