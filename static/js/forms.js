// Estado del formulario de registro
let registroState = {
    habilidadesSeleccionadas: [],
    skillsDisponibles: {}
};

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('registro-form')) {
        setupRegistrationForm();
    }
});

async function loadSkillsOptions() {
    try {
        const data = await API.get('/api/skills-lista');
        
        if (data.success) {
            registroState.skillsDisponibles = data.skills;
            renderSkillsCategories(data.skills);
        } else {
            ModernUI.showAlert('Error cargando habilidades disponibles', 'warning');
        }
    } catch (error) {
        console.error('Error cargando skills:', error);
        // Skills de respaldo
        registroState.skillsDisponibles = {
            tecnicas: ["Python", "SQL", "Machine Learning", "Power BI", "Tableau", "Excel"],
            analisis: ["Data Analysis", "Business Intelligence", "KPI", "Análisis Financiero"],
            gestion: ["Project Management", "Gestión de Proyectos", "Scrum", "Agile", "Business Analysis"]
        };
        renderSkillsCategories(registroState.skillsDisponibles);
    }
}

function renderSkillsCategories(skills) {
    // Habilidades Técnicas
    const tecnicasContainer = document.getElementById('skills-tecnicas');
    tecnicasContainer.innerHTML = skills.tecnicas.map(skill => `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${skill}" id="skill-${skill}">
            <label class="form-check-label" for="skill-${skill}">
                ${skill}
            </label>
        </div>
    `).join('');

    // Habilidades de Análisis
    const analisisContainer = document.getElementById('skills-analisis');
    analisisContainer.innerHTML = skills.analisis.map(skill => `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${skill}" id="skill-${skill}">
            <label class="form-check-label" for="skill-${skill}">
                ${skill}
            </label>
        </div>
    `).join('');

    // Habilidades de Gestión
    const gestionContainer = document.getElementById('skills-gestion');
    gestionContainer.innerHTML = skills.gestion.map(skill => `
        <div class="form-check">
            <input class="form-check-input" type="checkbox" value="${skill}" id="skill-${skill}">
            <label class="form-check-label" for="skill-${skill}">
                ${skill}
            </label>
        </div>
    `).join('');

    // Agregar event listeners a los checkboxes
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener('change', handleSkillSelection);
    });
}

function setupRegistrationForm() {
    const form = document.getElementById('registro-form');
    form.addEventListener('submit', handleFormSubmit);
    
    // Cargar opciones de skills
    loadSkillsOptions();
}

function handleSkillSelection(event) {
    const skill = event.target.value;
    const isChecked = event.target.checked;

    if (isChecked) {
        registroState.habilidadesSeleccionadas.push(skill);
    } else {
        registroState.habilidadesSeleccionadas = registroState.habilidadesSeleccionadas.filter(s => s !== skill);
    }

    updateSelectedSkillsDisplay();
}

function updateSelectedSkillsDisplay() {
    const container = document.getElementById('habilidades-seleccionadas');
    const counter = document.getElementById('contador-skills');

    if (registroState.habilidadesSeleccionadas.length === 0) {
        container.innerHTML = '<span class="text-muted">No hay habilidades seleccionadas</span>';
    } else {
        container.innerHTML = registroState.habilidadesSeleccionadas.map(skill => 
            ModernUI.createSkillChip(skill)
        ).join('');
    }

    counter.textContent = `${registroState.habilidadesSeleccionadas.length} habilidades seleccionadas`;
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = {
        user_id: document.getElementById('user_id').value,
        nombre: document.getElementById('nombre').value,
        experiencia: document.getElementById('experiencia').value,
        objetivo: document.getElementById('objetivo').value,
        habilidades: registroState.habilidadesSeleccionadas
    };

    // Validación básica
    if (!formData.user_id || !formData.nombre || !formData.experiencia || !formData.objetivo) {
        ModernUI.showAlert('Por favor completa todos los campos obligatorios', 'warning');
        return;
    }

    if (formData.habilidades.length === 0) {
        ModernUI.showAlert('Selecciona al menos una habilidad', 'warning');
        return;
    }

    // Mostrar loading
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Creando perfil...';
    submitBtn.disabled = true;

    try {
        const result = await API.post('/api/registrar-usuario', formData);
        
        if (result.success) {
            showRegistrationSuccess(result);
        } else {
            ModernUI.showAlert(result.message || 'Error creando el perfil', 'danger');
        }
    } catch (error) {
        console.error('Error en registro:', error);
        ModernUI.showAlert('Error de conexión con el servidor', 'danger');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

function showRegistrationSuccess(result) {
    const resultadosDiv = document.getElementById('resultados-registro');
    const formDiv = document.getElementById('registro-form').closest('.card-modern');
    
    resultadosDiv.style.display = 'block';
    formDiv.style.display = 'none';

    resultadosDiv.innerHTML = `
        <div class="card-modern border-success">
            <div class="card-body text-center py-5">
                <i class="bi bi-check-circle-fill text-success display-1 mb-3"></i>
                <h3 class="text-success mb-3">¡Perfil Creado Exitosamente!</h3>
                <p class="lead">Hemos analizado tus habilidades y generado recomendaciones personalizadas</p>
                
                <div class="row mt-4">
                    <div class="col-md-6 mb-3">
                        <div class="card-modern">
                            <div class="card-header bg-success text-white">
                                <h6 class="mb-0">Tus Habilidades</h6>
                            </div>
                            <div class="card-body">
                                <div class="d-flex flex-wrap gap-2">
                                    ${result.user_data.skills_actuales.map(skill => 
                                        ModernUI.createSkillChip(skill, 'actual')
                                    ).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 mb-3">
                        <div class="card-modern">
                            <div class="card-header bg-primary text-white">
                                <h6 class="mb-0">Recomendaciones</h6>
                            </div>
                            <div class="card-body">
                                <div class="d-flex flex-wrap gap-2">
                                    ${result.recomendaciones.map(skill => 
                                        ModernUI.createSkillChip(skill, 'recomendada')
                                    ).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-4">
                    <p class="text-muted mb-3">
                        <strong>Adecuación al mercado:</strong> ${result.user_data.puntuacion_adecuacion}%
                    </p>
                </div>

                <div class="mt-4">
                    <a href="/perfil" class="btn btn-modern btn-primary me-3">
                        <i class="bi bi-person-check me-2"></i>Ver Mi Perfil
                    </a>
                    <button onclick="resetForm()" class="btn btn-modern btn-outline-secondary">
                        <i class="bi bi-person-add me-2"></i>Crear Otro Perfil
                    </button>
                </div>
            </div>
        </div>
    `;
}

function resetForm() {
    document.getElementById('registro-form').reset();
    registroState.habilidadesSeleccionadas = [];
    updateSelectedSkillsDisplay();
    
    document.getElementById('resultados-registro').style.display = 'none';
    document.getElementById('registro-form').closest('.card-modern').style.display = 'block';
}

// Exportar funciones globales
window.loadSkillsOptions = loadSkillsOptions;
window.setupRegistrationForm = setupRegistrationForm;
window.resetForm = resetForm;