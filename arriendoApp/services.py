from .models import Usuario, Inmueble, InmuebleUsuario, ContratoArriendo, TipoInmueble

def crear_tipo_inmueble(nombre, descripcion=''):
    tipo_inmueble = TipoInmueble(nombre=nombre, descripcion=descripcion)
    tipo_inmueble.save()
    return tipo_inmueble

def obtener_tipos_inmueble():
    return TipoInmueble.objects.all()

def crear_inmueble(nombre, descripcion, m2_construidos, m2_totales, estacionamientos, 
                habitaciones, banos, direccion, comuna, tipo_inmueble_id, precio_mensual):
    tipo_inmueble = TipoInmueble.objects.filter(id=tipo_inmueble_id).first()
    if not tipo_inmueble:
        return None
    
    inmueble = Inmueble(nombre=nombre, descripcion=descripcion, m2_construidos=m2_construidos,
                        m2_totales=m2_totales, estacionamientos=estacionamientos, habitaciones=habitaciones,
                        banos=banos, direccion=direccion, comuna=comuna, tipo_inmueble=tipo_inmueble,
                        precio_mensual=precio_mensual)
    inmueble.save()
    return inmueble

def asignar_arrendador(inmueble_id, usuario_id, fecha_inicio):
    inmueble = Inmueble.objects.filter(id=inmueble_id).first()
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not inmueble or not usuario:
        return False
    
    InmuebleUsuario.objects.create(
        usuario=usuario,
        inmueble=inmueble,
        rol='ARRENDADOR',
        fecha_inicio=fecha_inicio
    )
    return True

def crear_contrato_arriendo(inmueble_id, arrendatario_id, fecha_inicio, fecha_fin=None):
    inmueble = Inmueble.objects.filter(id=inmueble_id).first()
    arrendatario = Usuario.objects.filter(id=arrendatario_id).first()
    if not inmueble or not arrendatario:
        return None
    
    inmueble_usuario = InmuebleUsuario.objects.create(
        usuario=arrendatario,
        inmueble=inmueble,
        rol='ARRENDATARIO',
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    contrato = ContratoArriendo.objects.create(
        inmueble_usuario=inmueble_usuario,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    return contrato

def terminar_contrato_arriendo(contrato_id, fecha_fin):
    contrato = ContratoArriendo.objects.filter(id=contrato_id).first()
    if not contrato:
        return None
    
    contrato.fecha_fin = fecha_fin
    contrato.estado = 'TERMINADO'
    contrato.save()
    
    inmueble_usuario = contrato.inmueble_usuario
    inmueble_usuario.fecha_fin = fecha_fin
    inmueble_usuario.save()
    
    return contrato

def obtener_inmuebles_arrendados(usuario_id):
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return None
    
    return Inmueble.objects.filter(
        inmuebleusuario__usuario=usuario,
        inmuebleusuario__rol='ARRENDATARIO'
    )

def obtener_contratos_activos(usuario_id):
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return None
    
    return ContratoArriendo.objects.filter(
        inmueble_usuario__usuario=usuario,
        inmueble_usuario__rol='ARRENDATARIO',
        estado='ACTIVO'
    )