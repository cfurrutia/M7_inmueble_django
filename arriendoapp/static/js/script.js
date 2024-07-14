document.addEventListener('DOMContentLoaded', function() {
    // Buscar el formulario de crear inmuebles
    var form = document.querySelector('form[name="crear_inmueble"]');
    
    if (form) {
        var regionSelect = form.querySelector('select[name="region"]');
        var comunaSelect = form.querySelector('select[name="comuna"]');

        if (regionSelect && comunaSelect) {
            regionSelect.addEventListener('change', function() {
                var regionId = this.value;
                
                // Limpiar las opciones actuales
                comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
                
                if (regionId) {
                    // Hacer una petición AJAX para obtener las comunas
                    fetch('/obtener_comunas/?region_id=' + regionId, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                    })
                        .then(response => response.json())
                        .then(data => {
                            data.forEach(function(comuna) {
                                var option = document.createElement('option');
                                option.value = comuna.id;
                                option.textContent = comuna.nombre;
                                comunaSelect.appendChild(option);
                            });
                        })
                        .catch(error => console.error('Error:', error));
                }
            });
        }
    }
});

// Function to get CSRF token
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