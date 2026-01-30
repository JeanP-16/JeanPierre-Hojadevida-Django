/**
 * ========================================
 * VALIDACIONES INMUTABLES DEL SISTEMA
 * Estas reglas NO son configurables
 * ========================================
 */

// Constantes inmutables del sistema
const VALIDATION_RULES = {
    BIRTH_YEAR_MIN: 1980,
    BIRTH_YEAR_MAX: new Date().getFullYear(),
    CERTIFICATE_YEAR_MIN: 2007,
    CERTIFICATE_YEAR_MAX: 2026,
    CEDULA_LENGTH: 10
};

/**
 * 🔒 VALIDACIÓN 1: Fecha de nacimiento (1980 - año actual)
 */
function validateBirthDate(dateInput) {
    if (!dateInput.value) return true;
    
    const selectedDate = new Date(dateInput.value);
    const year = selectedDate.getFullYear();
    const currentYear = VALIDATION_RULES.BIRTH_YEAR_MAX;
    
    if (year < VALIDATION_RULES.BIRTH_YEAR_MIN || year > currentYear) {
        showError(
            dateInput,
            `La fecha de nacimiento debe estar entre ${VALIDATION_RULES.BIRTH_YEAR_MIN} y ${currentYear}.`
        );
        return false;
    }
    
    clearError(dateInput);
    return true;
}

/**
 * 🔒 VALIDACIÓN 2: Fechas de certificados/estudios (2007 - 2026)
 */
function validateCertificateDate(dateInput) {
    if (!dateInput.value) return true;
    
    const selectedDate = new Date(dateInput.value);
    const year = selectedDate.getFullYear();
    
    if (year < VALIDATION_RULES.CERTIFICATE_YEAR_MIN || year > VALIDATION_RULES.CERTIFICATE_YEAR_MAX) {
        showError(
            dateInput,
            `Las fechas solo pueden estar entre ${VALIDATION_RULES.CERTIFICATE_YEAR_MIN} y ${VALIDATION_RULES.CERTIFICATE_YEAR_MAX}.`
        );
        return false;
    }
    
    clearError(dateInput);
    return true;
}

/**
 * 🔒 VALIDACIÓN 3: Cédula (exactamente 10 dígitos numéricos)
 */
function validateCedula(cedulaInput) {
    const value = cedulaInput.value.trim();
    
    // Verificar que solo contenga dígitos
    if (!/^\d+$/.test(value)) {
        showError(
            cedulaInput,
            'La cédula debe contener solo números, sin letras, espacios ni símbolos.'
        );
        return false;
    }
    
    // Verificar longitud exacta
    if (value.length !== VALIDATION_RULES.CEDULA_LENGTH) {
        showError(
            cedulaInput,
            `La cédula debe contener exactamente ${VALIDATION_RULES.CEDULA_LENGTH} dígitos numéricos.`
        );
        return false;
    }
    
    clearError(cedulaInput);
    return true;
}

/**
 * Validación cronológica: fecha inicio < fecha fin
 */
function validateDateRange(startInput, endInput) {
    if (!startInput.value || !endInput.value) return true;
    
    const startDate = new Date(startInput.value);
    const endDate = new Date(endInput.value);
    
    if (startDate > endDate) {
        showError(
            endInput,
            'La fecha de fin debe ser posterior a la fecha de inicio.'
        );
        return false;
    }
    
    clearError(endInput);
    return true;
}

/**
 * Mostrar mensaje de error
 */
function showError(input, message) {
    // Eliminar error previo si existe
    clearError(input);
    
    // Agregar clase de error al input
    input.classList.add('is-invalid');
    
    // Crear elemento de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    errorDiv.setAttribute('data-validation-error', 'true');
    
    // Insertar después del input
    input.parentNode.appendChild(errorDiv);
    
    // Scroll al error
    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Focus en el input
    input.focus();
}

/**
 * Limpiar mensaje de error
 */
function clearError(input) {
    input.classList.remove('is-invalid');
    
    // Eliminar mensajes de error
    const errorMessages = input.parentNode.querySelectorAll('[data-validation-error="true"]');
    errorMessages.forEach(msg => msg.remove());
}

/**
 * Configurar validaciones en tiempo real
 */
function setupRealtimeValidation() {
    // Fecha de nacimiento
    const birthDateInputs = document.querySelectorAll('input[name="fecha_nacimiento"]');
    birthDateInputs.forEach(input => {
        input.addEventListener('change', () => validateBirthDate(input));
        input.addEventListener('blur', () => validateBirthDate(input));
    });
    
    // Fechas de certificados/estudios/experiencia
    const certificateDateInputs = document.querySelectorAll(
        'input[name="fecha"], input[name="fecha_inicio"], input[name="fecha_fin"]'
    );
    certificateDateInputs.forEach(input => {
        input.addEventListener('change', () => validateCertificateDate(input));
        input.addEventListener('blur', () => validateCertificateDate(input));
    });
    
    // Cédula
    const cedulaInputs = document.querySelectorAll('input[name="cedula"]');
    cedulaInputs.forEach(input => {
        // Validar en tiempo real
        input.addEventListener('input', () => {
            // Solo permitir números
            input.value = input.value.replace(/\D/g, '');
            
            // Limitar a 10 dígitos
            if (input.value.length > VALIDATION_RULES.CEDULA_LENGTH) {
                input.value = input.value.slice(0, VALIDATION_RULES.CEDULA_LENGTH);
            }
        });
        
        input.addEventListener('blur', () => validateCedula(input));
    });
    
    // Validar rangos de fechas (inicio/fin)
    const startInputs = document.querySelectorAll('input[name="fecha_inicio"]');
    startInputs.forEach(startInput => {
        const form = startInput.closest('form');
        if (form) {
            const endInput = form.querySelector('input[name="fecha_fin"]');
            if (endInput) {
                startInput.addEventListener('change', () => validateDateRange(startInput, endInput));
                endInput.addEventListener('change', () => validateDateRange(startInput, endInput));
            }
        }
    });
}

/**
 * Validar formulario completo antes del envío
 */
function validateFormSubmit(form) {
    let isValid = true;
    const errors = [];
    
    // Validar fecha de nacimiento
    const birthDateInput = form.querySelector('input[name="fecha_nacimiento"]');
    if (birthDateInput && birthDateInput.value) {
        if (!validateBirthDate(birthDateInput)) {
            isValid = false;
            errors.push('Fecha de nacimiento inválida');
        }
    }
    
    // Validar fechas de certificados/estudios
    const certDateInputs = form.querySelectorAll(
        'input[name="fecha"], input[name="fecha_inicio"], input[name="fecha_fin"]'
    );
    certDateInputs.forEach(input => {
        if (input.value && !validateCertificateDate(input)) {
            isValid = false;
            errors.push(`Fecha inválida en ${input.name}`);
        }
    });
    
    // Validar cédula
    const cedulaInput = form.querySelector('input[name="cedula"]');
    if (cedulaInput && cedulaInput.value) {
        if (!validateCedula(cedulaInput)) {
            isValid = false;
            errors.push('Cédula inválida');
        }
    }
    
    // Validar rangos de fechas
    const startInputs = form.querySelectorAll('input[name="fecha_inicio"]');
    startInputs.forEach(startInput => {
        const endInput = form.querySelector('input[name="fecha_fin"]');
        if (endInput && startInput.value && endInput.value) {
            if (!validateDateRange(startInput, endInput)) {
                isValid = false;
                errors.push('Rango de fechas inválido');
            }
        }
    });
    
    if (!isValid) {
        // Mostrar resumen de errores
        alert('❌ No se puede guardar. Errores encontrados:\n\n' + errors.join('\n'));
        return false;
    }
    
    return true;
}

/**
 * Configurar validación en todos los formularios
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateFormSubmit(form)) {
                event.preventDefault();
                event.stopPropagation();
                return false;
            }
        });
    });
}

/**
 * Configurar límites en inputs de fecha mediante atributos HTML
 */
function setupDateLimits() {
    const currentYear = new Date().getFullYear();
    
    // Fecha de nacimiento: 1980 hasta año actual
    const birthDateInputs = document.querySelectorAll('input[name="fecha_nacimiento"]');
    birthDateInputs.forEach(input => {
        input.setAttribute('min', '1980-01-01');
        input.setAttribute('max', `${currentYear}-12-31`);
        input.setAttribute('required', 'required');
    });
    
    // Fechas de certificados: 2007 hasta 2026
    const certDateInputs = document.querySelectorAll(
        'input[name="fecha"], input[name="fecha_inicio"], input[name="fecha_fin"]'
    );
    certDateInputs.forEach(input => {
        input.setAttribute('min', '2007-01-01');
        input.setAttribute('max', '2026-12-31');
    });
    
    // Cédula: pattern exacto
    const cedulaInputs = document.querySelectorAll('input[name="cedula"]');
    cedulaInputs.forEach(input => {
        input.setAttribute('pattern', '\\d{10}');
        input.setAttribute('maxlength', '10');
        input.setAttribute('inputmode', 'numeric');
        input.setAttribute('required', 'required');
        input.setAttribute('title', 'Exactamente 10 dígitos numéricos');
    });
}

/**
 * Inicializar todas las validaciones cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔒 Sistema de validaciones inmutables iniciado');
    console.log('Reglas activas:', VALIDATION_RULES);
    
    setupDateLimits();
    setupRealtimeValidation();
    setupFormValidation();
    
    console.log('✅ Validaciones configuradas correctamente');
});

/**
 * Exportar funciones para uso externo si es necesario
 */
if (typeof window !== 'undefined') {
    window.CVValidation = {
        validateBirthDate,
        validateCertificateDate,
        validateCedula,
        validateDateRange,
        validateFormSubmit,
        RULES: VALIDATION_RULES
    };
}
