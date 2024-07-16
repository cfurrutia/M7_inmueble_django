document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[name="crear_inmueble"]');
    
    if (form) {
        const regionSelect = form.querySelector('select[name="region"]');
        const comunaSelect = form.querySelector('select[name="comuna"]');
        
        if (regionSelect && comunaSelect) {
            // Deshabilitar el select de comuna inicialmente
            comunaSelect.disabled = true;

            regionSelect.addEventListener('change', function() {
                const regionId = this.value;
                
                // Resetear y deshabilitar el select de comuna
                resetComunaSelect();
                
                if (regionId) {
                    // Mostrar un indicador de carga
                    showLoading(comunaSelect);
                    
                    // Hacer una petición AJAX para obtener las comunas
                    fetch(`/obtener_comunas/?region_id=${regionId}`, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('error de red');
                        }
                        return response.json();
                    })
                    .then(data => {
                        populateComunaSelect(data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        showError(comunaSelect);
                    })
                    .finally(() => {
                        // Remover el indicador de carga
                        hideLoading(comunaSelect);
                    });
                }
            });
        }
    }
});

function resetComunaSelect() {
    const comunaSelect = document.querySelector('select[name="comuna"]');
    comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
    comunaSelect.disabled = true;
}

function populateComunaSelect(data) {
    const comunaSelect = document.querySelector('select[name="comuna"]');
    data.forEach(function(comuna) {
        const option = document.createElement('option');
        option.value = comuna.id;
        option.textContent = comuna.nombre;
        comunaSelect.appendChild(option);
    });
    comunaSelect.disabled = false;
}

function showLoading(element) {
    element.classList.add('loading');
    element.parentNode.insertAdjacentHTML('beforeend', '<span class="loading-indicator">Cargando...</span>');
}

function hideLoading(element) {
    element.classList.remove('loading');
    const loadingIndicator = element.parentNode.querySelector('.loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

function showError(element) {
    element.classList.add('error');
    element.parentNode.insertAdjacentHTML('beforeend', '<span class="error-message">Error al cargar las comunas. Por favor, intente nuevamente.</span>');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}