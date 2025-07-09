from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, FacturaSubida
from .forms import LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import FileResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from functools import wraps
from django.http import HttpResponseForbidden
from django.db.models import Count
from django.db.models.functions import TruncDate
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.conf import settings

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or (hasattr(request.user, 'rol') and request.user.rol == 'admin')):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    return _wrapped_view

@login_required(login_url='login')
def descargar_facturas_pdf(request):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        return HttpResponse('Usuario no encontrado', status=404)

    # Filtrado por rango de fechas si se reciben parámetros GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj)
    if start_date:
        facturas_usuario = facturas_usuario.filter(fecha__gte=start_date)
    if end_date:
        facturas_usuario = facturas_usuario.filter(fecha__lte=end_date)
    facturas_usuario = facturas_usuario.order_by('-fecha_subida')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    title = "Listado de Facturas"
    if start_date or end_date:
        rango = ""
        if start_date:
            rango += f"Desde {start_date} "
        if end_date:
            rango += f"Hasta {end_date}"
        title += f" ({rango.strip()})"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))
    data = [["Fecha", "Número", "Descripción", "NIT", "Categoría", "Monto", "IVA", "Total"]]
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19 if f.tipo_monto == 'neto' else float(f.monto) - (float(f.monto) / 1.19)
        neto = float(f.monto) if f.tipo_monto == 'neto' else float(f.monto) / 1.19
        total = neto + iva
        data.append([
            f.fecha.strftime('%d/%m/%Y') if f.fecha else '',
            f.numero,
            f.descripcion,
            f.nit,
            f.categoria,
            f"{neto:,.2f}",
            f"{iva:,.2f}",
            f"{total:,.2f}"
        ])
    table = Table(data, repeatRows=1, colWidths=[55, 55, 110, 60, 70, 55, 55, 55])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='facturas.pdf')

@csrf_exempt
@login_required(login_url='login')
def subir_factura(request):
    import requests
    if request.method == 'POST':
        try:
            usuario_obj = Usuario.objects.get(username=request.user.username)
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=400)

        descripcion = request.POST.get('invoice-description', '')
        numero = request.POST.get('invoice-number', '')
        nit = request.POST.get('invoice-nit', '')
        fecha = request.POST.get('invoice-date', '')
        categoria = request.POST.get('invoice-category', '')
        monto = request.POST.get('invoice-amount', '')
        tipo_monto = request.POST.get('amount-type', 'neto')
        archivo = request.FILES.get('invoice-file', None)

        try:
            monto_decimal = float(monto)
            if monto_decimal < 0:
                raise ValueError('El monto no puede ser negativo')
        except Exception:
            return JsonResponse({'success': False, 'error': 'El monto ingresado no es válido. Debe ser un número positivo.'}, status=400)

        # --- INTEGRACIÓN CON FACTUS ---
        # 1. Obtener token de autenticación
        auth_url = 'https://api-sandbox.factus.com.co/oauth/token'
        client_id = '9de1b0af-7c02-471e-a568-bdc78a5b119d'
        client_secret = '6byR029aNsrSSEESx87mISZiUep6fcooUEcngm5N'
        username = 'sandbox@factus.com.co'
        password = 'sandbox2024%'
        data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password
        }
        try:
            auth_response = requests.post(auth_url, data=data)
            auth_response.raise_for_status()
            access_token = auth_response.json().get('access_token')
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error autenticando con Factus: {str(e)}'}, status=500)
        if not access_token:
            return JsonResponse({'success': False, 'error': 'No se pudo obtener token de acceso de Factus.'}, status=500)

        # 2. Enviar factura a Factus (Ajusta los campos según la documentación oficial de Factus)
        # Ejemplo de payload basado en la documentación de Factus:
        factura_payload = {
            "numbering_range_id": int(request.POST.get('numbering_range_id', 8)),
            "reference_code": request.POST.get('reference_code', 'ivas'),
            "observation": request.POST.get('observation', ''),
            "payment_form": request.POST.get('payment_form', '1'),
            "payment_due_date": request.POST.get('payment_due_date', fecha),
            "payment_method_code": request.POST.get('payment_method_code', '10'),
            "operation_type": int(request.POST.get('operation_type', 10)),
            "send_email": request.POST.get('send_email', 'false') == 'true',
            "order_reference": {
                "reference_code": request.POST.get('order_reference_code', 'ref-001'),
                "issue_date": request.POST.get('order_issue_date', '')
            },
            "billing_period": {
                "start_date": request.POST.get('billing_start_date', fecha),
                "start_time": request.POST.get('billing_start_time', '00:00:00'),
                "end_date": request.POST.get('billing_end_date', fecha),
                "end_time": request.POST.get('billing_end_time', '23:59:59')
            },
            "customer": {
                "identification": nit,
                "dv": request.POST.get('customer_dv', ''),
                "company": request.POST.get('customer_company', ''),
                "trade_name": request.POST.get('customer_trade_name', ''),
                "names": request.POST.get('customer_names', ''),
                "address": request.POST.get('customer_address', ''),
                "email": request.POST.get('customer_email', ''),
                "phone": request.POST.get('customer_phone', ''),
                "legal_organization_id": request.POST.get('customer_legal_organization_id', ''),
                "tribute_id": request.POST.get('customer_tribute_id', ''),
                "identification_document_id": request.POST.get('customer_identification_document_id', ''),
                "municipality_id": request.POST.get('customer_municipality_id', '')
            },
            "items": [
                {
                    "scheme_id": int(request.POST.get('item1_scheme_id', 1)),
                    "note": request.POST.get('item1_note', ''),
                    "code_reference": request.POST.get('item1_code_reference', '12345'),
                    "name": request.POST.get('item1_name', descripcion),
                    "quantity": int(request.POST.get('item1_quantity', 1)),
                    "discount_rate": float(request.POST.get('item1_discount_rate', 20)),
                    "price": float(request.POST.get('item1_price', monto_decimal)),
                    "tax_rate": request.POST.get('item1_tax_rate', '19.00'),
                    "unit_measure_id": int(request.POST.get('item1_unit_measure_id', 70)),
                    "standard_code_id": int(request.POST.get('item1_standard_code_id', 1)),
                    "is_excluded": int(request.POST.get('item1_is_excluded', 0)),
                    "tribute_id": int(request.POST.get('item1_tribute_id', 1)),
                    "withholding_taxes": [
                        {
                            "code": request.POST.get('item1_withholding_code_1', '06'),
                            "withholding_tax_rate": request.POST.get('item1_withholding_tax_rate_1', '7.00')
                        },
                        {
                            "code": request.POST.get('item1_withholding_code_2', '05'),
                            "withholding_tax_rate": request.POST.get('item1_withholding_tax_rate_2', '15.00')
                        }
                    ],
                    "mandate": {
                        "identification_document_id": int(request.POST.get('item1_mandate_identification_document_id', 6)),
                        "identification": request.POST.get('item1_mandate_identification', nit)
                    }
                },
                {
                    "scheme_id": int(request.POST.get('item2_scheme_id', 0)),
                    "note": request.POST.get('item2_note', ''),
                    "code_reference": request.POST.get('item2_code_reference', '54321'),
                    "name": request.POST.get('item2_name', 'producto de prueba 2'),
                    "quantity": int(request.POST.get('item2_quantity', 1)),
                    "discount_rate": float(request.POST.get('item2_discount_rate', 0)),
                    "price": float(request.POST.get('item2_price', monto_decimal)),
                    "tax_rate": request.POST.get('item2_tax_rate', '5.00'),
                    "unit_measure_id": int(request.POST.get('item2_unit_measure_id', 70)),
                    "standard_code_id": int(request.POST.get('item2_standard_code_id', 1)),
                    "is_excluded": int(request.POST.get('item2_is_excluded', 0)),
                    "tribute_id": int(request.POST.get('item2_tribute_id', 1)),
                    "withholding_taxes": []
                }
            ]
        }
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        factus_url = 'https://api-sandbox.factus.com.co/v1/bills/validate'  # Endpoint correcto según Postman
        try:
            factus_response = requests.post(factus_url, json=factura_payload, headers=headers)
            factus_response.raise_for_status()
            factus_data = factus_response.json()
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error enviando factura a Factus: {str(e)}'}, status=500)

        # 3. Guardar localmente solo si Factus responde OK
        factura = FacturaSubida(
            usuario=usuario_obj,
            descripcion=descripcion,
            numero=numero,
            nit=nit,
            fecha=fecha if fecha else None,
            categoria=categoria,
            monto=monto_decimal,
            tipo_monto=tipo_monto,
        )
        # Si la respuesta de Factus incluye un PDF o ID, guárdalo en el modelo
        if factus_data.get('pdf_url'):
            factura.factus_pdf_url = factus_data['pdf_url']
        # Guardar el enlace público de visualización si viene en la respuesta
        if 'data' in factus_data and 'bill' in factus_data['data'] and 'public_url' in factus_data['data']['bill']:
            factura.factus_public_url = factus_data['data']['bill']['public_url']
        if archivo:
            factura.archivo = archivo
        factura.save()
        # Notificación de subida exitosa
        from .models import Notification
        Notification.objects.create(
            user=usuario_obj,
            tipo='info',
            titulo='Factura subida exitosamente',
            mensaje=f'Su factura número {factura.numero} fue registrada correctamente en Factus.',
        )
        # Devuelve la información relevante de Factus
        return JsonResponse({'success': True, 'factus': factus_data})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

def user_logout(request):
    logout(request)
    return redirect('login')

def inicio(request):
    return render(request, 'paginas/index.html')

def alinicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def presentacion(request):
    return render(request, 'paginas/presentacion.html')

def login(request):
    return render(request, 'paginas/login.html')

def registrarse(request):
    if request.method == 'POST':
        password = request.POST.get('password', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        tipo_documento = request.POST.get('tipo_documento', '').strip()
        numero_documento = request.POST.get('numero_documento', '').strip()
        genero = request.POST.get('genero', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        rol = request.POST.get('rol', '').strip()
        email = request.POST.get('email', '').strip()

        # Generar username automáticamente
        username_base = f"{first_name}.{last_name}".replace(' ', '').lower()
        username = username_base
        count = 1
        while Usuario.objects.filter(username=username).exists():
            username = f"{username_base}{count}"
            count += 1

        # Validaciones básicas
        if not password or not first_name or not last_name or not tipo_documento or not numero_documento or not genero or not ciudad or not telefono or not direccion or not email:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('registrarse')
        if Usuario.objects.filter(numero_documento=numero_documento).exists():
            messages.error(request, 'Ya existe un usuario con ese número de documento.')
            return redirect('registrarse')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Ya existe un usuario con ese correo electrónico.')
            return redirect('registrarse')

        user = Usuario.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            genero=genero,
            ciudad=ciudad,
            telefono=telefono,
            direccion=direccion,
            rol=rol,
            email=email,
        )
        # Enviar correo de bienvenida
        from django.core.mail import send_mail
        from django.conf import settings
        asunto = 'Bienvenido a IVACOL'
        mensaje = f'Hola {first_name}, tu usuario ha sido creado exitosamente. Ya puedes iniciar sesión en IVACOL.'
        send_mail(
            asunto,
            mensaje,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True
        )
        messages.success(request, 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'paginas/registrarse.html')


def tratamiento(request):
    import requests
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': '6LdUPmQrAAAAADgEKB1dyBPNxWRt8L08JWOrBNCw',
            'response': recaptcha_response,
            'remoteip': request.META.get('REMOTE_ADDR')
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result.get('success'):
            messages.success(request, 'Captcha verificado correctamente.')
            return redirect('registrarse')
        else:
            messages.error(request, 'Captcha inválido. Por favor, inténtalo de nuevo.')
    return render(request, 'paginas/tratamiento.html')

def DeclaracionDatos(request):
    return render(request, 'paginas/DeclaracionDatos.html')

@login_required(login_url='login')
def crud(request):
    return render(request, 'paginas/crud.html')

def contactenos(request):
    return render(request, 'paginas/contactenos.html')

def diccionario(request):
    return render(request, 'paginas/diccionario.html')

def dml(request):
    return render(request, 'paginas/dml.html')

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def invitar_registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        if not nombre or not correo:
            return render(request, 'paginas/inicio.html', {'error': 'Debes ingresar nombre y correo.'})
        # Construir enlace a tratamiento
        url_tratamiento = request.build_absolute_uri(reverse('tratamiento'))
        asunto = 'Invitación a registrarte en IVACOL'
        mensaje = f"Hola {nombre}, ya puedes iniciar tu registro en nuestra página, haz clic aquí: {url_tratamiento}"
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=False,
            )
            return render(request, 'paginas/inicio.html', {'success': 'Correo enviado correctamente.'})
        except Exception as e:
            return render(request, 'paginas/inicio.html', {'error': f'Error al enviar el correo: {e}'})
    return redirect('inicio')

def solicitarContra(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return render(request, 'paginas/solicitarContraseña.html', {'error': 'Por favor ingresa un correo.'})
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            # Para no revelar si el correo existe o no
            return render(request, 'paginas/solicitarContraseña.html', {'success': True})
        token = default_token_generator.make_token(usuario)
        uid = urlsafe_base64_encode(force_bytes(usuario.pk))
        reset_url = request.build_absolute_uri(
            reverse('cambiarContra') + f'?uid={uid}&token={token}'
        )
        from django.core.mail import EmailMultiAlternatives
        subject = 'Restablecimiento de contraseña IVACOL'
        html_message = render_to_string('paginas/email_reset_password.html', {
            'usuario': usuario,
            'reset_url': reset_url,
        })
        text_message = f"Hola {usuario.first_name},\n\nSolicitaste un cambio de tu contraseña, a continuación puedes hacerlo efectivo. Si no fuiste tú, puedes ignorar este mensaje.\n\nEnlace: {reset_url}\n\nSaludos,\nEquipo IVACOL"
        print('Enviando a:', usuario.email)
        print('Asunto:', subject)
        print('Texto plano:', text_message)
        print('HTML:', html_message)
        try:
            email = EmailMultiAlternatives(
                subject,
                text_message,
                'ivacolom.app@gmail.com',
                [usuario.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            return render(request, 'paginas/solicitarContraseña.html', {'success': True, 'debug': text_message})
        except Exception as e:
            return render(request, 'paginas/solicitarContraseña.html', {'error': f'Error al enviar el correo: {e}', 'debug': text_message})
    return render(request, 'paginas/solicitarContraseña.html')

def cambiarContra(request):
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth import get_user_model
    UserModel = get_user_model()

    if request.method == 'GET':
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        if not uidb64 or not token:
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'Enlace inválido o incompleto.'})
        return render(request, 'paginas/cambiarContraseña.html', {'uid': uidb64, 'token': token})

    if request.method == 'POST':
        uidb64 = request.POST.get('uid')
        token = request.POST.get('token')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not uidb64 or not token:
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'Enlace inválido o incompleto.'})
        if not password1 or not password2:
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'Debes ingresar la nueva contraseña dos veces.', 'uid': uidb64, 'token': token})
        if password1 != password2:
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'Las contraseñas no coinciden.', 'uid': uidb64, 'token': token})
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'Usuario inválido.', 'uid': uidb64, 'token': token})
        if not default_token_generator.check_token(user, token):
            return render(request, 'paginas/cambiarContraseña.html', {'error': 'El enlace de restablecimiento es inválido o ha expirado.'})
        user.set_password(password1)
        user.save()
        return render(request, 'paginas/cambiarContraseña.html', {'success': '¡Contraseña restablecida exitosamente! Ya puedes iniciar sesión.'})

def confirmarContra(request):
    return render(request, 'paginas/confirmarContraseña.html')

@login_required(login_url='login')
def paginaPrincipal(request):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        usuario_obj = None

    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj).order_by('-fecha_subida')[:6] if usuario_obj else []
    facturas_context = []
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19 if f.tipo_monto == 'neto' else float(f.monto) - (float(f.monto) / 1.19)
        neto = float(f.monto) if f.tipo_monto == 'neto' else float(f.monto) / 1.19
        total = neto + iva
        facturas_context.append({
            'id': f.id,
            'fecha': f.fecha,
            'numero': f.numero,
            'descripcion': f.descripcion,
            'nit': f.nit,
            'categoria': f.categoria,
            'monto': neto,
            'iva': iva,
            'total': total,
        })
    context = {
        'facturas': facturas_context,
    }
    return render(request, 'ivapp/paginaPrincipal.html', context)

@login_required(login_url='login')
def get_facturas_usuario(request):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'}, status=400)
    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj).order_by('-fecha_subida')[:6]
    facturas_context = []
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19 if f.tipo_monto == 'neto' else float(f.monto) - (float(f.monto) / 1.19)
        neto = float(f.monto) if f.tipo_monto == 'neto' else float(f.monto) / 1.19
        total = neto + iva
        facturas_context.append({
            'id': f.id,
            'fecha': f.fecha.strftime('%d/%m/%Y') if f.fecha else '',
            'numero': f.numero,
            'descripcion': f.descripcion,
            'nit': f.nit,
            'categoria': f.categoria,
            'monto': f"{neto:.15f}",
            'iva': f"{iva:.15f}",
            'total': f"{total:.15f}",
        })
    return JsonResponse({'success': True, 'facturas': facturas_context})

@login_required(login_url='login')
def perfil(request):
    try: 
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        usuario_obj = None
    return render(request, 'ivapp/perfil.html', {'usuario': usuario_obj})


@login_required(login_url='login')
def graficas(request):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        usuario_obj = None
    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj).order_by('fecha') if usuario_obj else []
    facturas_context = []
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19 if f.tipo_monto == 'neto' else float(f.monto) - (float(f.monto) / 1.19)
        neto = float(f.monto) if f.tipo_monto == 'neto' else float(f.monto) / 1.19
        total = neto + iva
        facturas_context.append({
            'date': f.fecha.strftime('%Y-%m-%d') if f.fecha else '',
            'numero': f.numero,
            'label': f.descripcion,
            'category': f.categoria,
            'nit': f.nit,
            'neto': round(neto, 2),
            'iva': round(iva, 2),
            'acumulado': round(total, 2),
        })
    facturas_json = json.dumps(facturas_context, cls=DjangoJSONEncoder)
    return render(request, 'ivapp/graficas.html', {'facturas_json': facturas_json})

@login_required(login_url='login')
def leerFacturas(request):
    return render(request, 'ivapp/leerFacturas.html')

@login_required(login_url='login')
def notificaciones(request):
    return render(request, 'ivapp/notificaciones.html')

@admin_required
@login_required(login_url='login')
def facturasAdmin(request):
    from django.core.serializers.json import DjangoJSONEncoder
    import json
    facturas = FacturaSubida.objects.select_related('usuario').all().order_by('-fecha_subida')
    facturas_context = []
    for f in facturas:
        iva = float(f.monto) * 0.19 if f.tipo_monto == 'neto' else float(f.monto) - (float(f.monto) / 1.19)
        neto = float(f.monto) if f.tipo_monto == 'neto' else float(f.monto) / 1.19
        total = neto + iva
        # Criterio de factura completa
        completa = (
            f.fecha and f.numero and f.descripcion and f.nit and f.categoria and neto >= 0
        )
        estado = 'Completa' if completa else 'Incompleta'
        archivo_url = None
        if getattr(f, 'archivo', None):
            try:
                if f.archivo:
                    archivo_url = reverse('factura_archivo', args=[f.id])
            except Exception:
                archivo_url = None
        facturas_context.append({
            'date': f.fecha.strftime('%Y-%m-%d') if f.fecha else '',
            'numero': f.numero,
            'label': f.descripcion,
            'nit': f.nit,
            'category': f.categoria,
            'neto': round(neto, 2),
            'iva': round(iva, 2),
            'acumulado': round(total, 2),
            'usuario': f.usuario.get_full_name() or f.usuario.username,
            'usuario_id': f.usuario.id,
            'id': f.id,
            'estado': estado,
            'archivo_url': reverse('factura_archivo', args=[f.id]) if getattr(f, 'archivo', None) else None,
        })
    facturas_json = json.dumps(facturas_context, cls=DjangoJSONEncoder)
    return render(request, 'ingresos/facturasAdmin.html', {'facturas_json': facturas_json})

@admin_required
@login_required(login_url='login')
def UsuariosAdm(request):
    usuarios = Usuario.objects.all()
    return render(request, 'ingresos/InicioAdm.html', {'usuarios': usuarios})

@admin_required
@login_required(login_url='login')
def CrudAdm(request, id):
    usuario_inst = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        # Aquí deberías actualizar los campos según el formulario recibido
        # Ejemplo:
        usuario_inst.first_name = request.POST.get('first_name', usuario_inst.first_name)
        usuario_inst.email = request.POST.get('email', usuario_inst.email)
        usuario_inst.save()
        return redirect('CrudAdm')
    return render(request, 'ingresos/crudAdm.html', {'usuario': usuario_inst})

@admin_required
@login_required(login_url='login')
def InicioAdm(request):
    usuarios = Usuario.objects.all()
    # Agrupar facturas por fecha
    facturas_por_dia = (
        FacturaSubida.objects.values('fecha')
        .annotate(total=Count('id'))
        .order_by('fecha')
    )
    # Convertir a lista de dicts para JS
    facturas_dia_list = [
        {'fecha': f['fecha'].strftime('%Y-%m-%d') if f['fecha'] else '', 'total': f['total']} for f in facturas_por_dia if f['fecha']
    ]
    facturas_dia_json = json.dumps(facturas_dia_list, cls=DjangoJSONEncoder)
    return render(request, 'ingresos/InicioAdm.html', {
        'usuarios': usuarios,
        'facturas_dia_json': facturas_dia_json
    })

@admin_required
@login_required(login_url='login')
def editarAdm(request, id):
    from .forms import UsuarioForm
    usuario_inst = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario_inst)
        if form.is_valid():
            usuario = form.save(commit=False)
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('InicioAdm')
    else:
        form = UsuarioForm(instance=usuario_inst)
    return render(request, 'ingresos/editarAdm.html', {'usuario': usuario_inst, 'formulario': form})

@admin_required
@login_required(login_url='login')
def eliminarAdm(request, id):
    usuario_inst = get_object_or_404(Usuario, id=id)
    usuario_inst.delete()
    return redirect('InicioAdm')

@admin_required
@login_required(login_url='login')
def CrearAdm(request):
    from .forms import UsuarioForm
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            # Enviar correo de bienvenida
            from django.core.mail import send_mail
            from django.conf import settings
            asunto = 'Bienvenido a IVACOL'
            mensaje = f'Hola {usuario.first_name}, tu usuario ha sido creado exitosamente. Ya puedes iniciar sesión en IVACOL.'
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [usuario.email],
                fail_silently=True
            )
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('InicioAdm')
    else:
        form = UsuarioForm()
    return render(request, 'ingresos/crearAdm.html', {'formulario': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Buscar usuario por correo
            from .models import Usuario
            try:
                usuario = Usuario.objects.get(email=cd["username"])
                user = authenticate(
                    request,
                    username=usuario.username,
                    password=cd["password"]
                )
            except Usuario.DoesNotExist:
                user = None
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    if hasattr(user, 'rol') and user.rol == 'admin':
                        return redirect('InicioAdm')
                    else:
                        return redirect('paginaPrincipal')
                else:
                    messages.error(request, "Usuario inactivo")
            else:
                messages.error(request, "Credenciales inválidas")
        #si falla validación del form o de las credenciales se renderiza de nuevo con errores
    else:
        form = LoginForm()

    return render(request, "paginas/login.html", {"form": form})

@login_required(login_url='login')
def historial_facturas(request):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        usuario_obj = None

    facturas_usuario = FacturaSubida.objects.filter(usuario=usuario_obj).order_by('-fecha_subida') if usuario_obj else []
    facturas_context = []
    total_neto = 0
    total_iva = 0
    total_general = 0
    for f in facturas_usuario:
        iva = float(f.monto) * 0.19
        total = float(f.monto) + iva
        total_neto += float(f.monto)
        total_iva += iva
        total_general += total
        facturas_context.append({
            'id': f.id,
            'fecha': f.fecha,
            'numero': f.numero,
            'descripcion': f.descripcion,
            'nit': f.nit,
            'categoria': f.categoria,
            'monto': f.monto,
            'iva': iva,
            'total': total,
            'archivo': f.archivo.url if f.archivo else None,
            'public_url': getattr(f, 'factus_public_url', None),
        })
    context = {
        'facturas': facturas_context,
        'titulo_pagina': 'Historial de Facturas Subidas',
        'total_neto': total_neto,
        'total_iva': total_iva,
        'total_general': total_general,
    }
    return render(request, 'ivapp/historial_facturas.html', context)

from .models import Notification
import json

# Vista para borrar factura como admin
@admin_required
@login_required(login_url='login')
def borrar_factura_admin(request, id):
    factura = get_object_or_404(FacturaSubida, id=id)
    usuario_obj = factura.usuario
    if request.method == 'POST':
        # Recibir motivo del borrado (JSON o form-data)
        motivo = ''
        try:
            data = json.loads(request.body.decode())
            motivo = data.get('motivo', '').strip()
        except Exception:
            # Si no es JSON, intentar como form-data
            motivo = request.POST.get('motivo', '').strip()
        # Crear notificación
        Notification.objects.create(
            user=usuario_obj,
            tipo='alerta',
            titulo='Factura eliminada por el administrador',
            mensaje=f'Su factura número {factura.numero} fue eliminada por el administrador. Motivo: {motivo}',
        )
        factura.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

# Vista para borrar factura como usuario normal
@login_required(login_url='login')
def borrar_factura(request, id):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        return redirect('historial_facturas')
    factura = get_object_or_404(FacturaSubida, usuario=usuario_obj, id=id)
    if request.method == 'POST':
        Notification.objects.create(
            user=usuario_obj,
            tipo='info',
            titulo='Factura eliminada',
            mensaje=f'Eliminaste tu factura número {factura.numero} correctamente.',
        )
        factura.delete()
        return redirect('historial_facturas')
    return redirect('historial_facturas')

@login_required(login_url='login')
def editar_factura(request, id):
    try:
        usuario_obj = Usuario.objects.get(username=request.user.username)
    except Usuario.DoesNotExist:
        return redirect('historial_facturas')
    factura = get_object_or_404(FacturaSubida, usuario=usuario_obj, id=id)
    if request.method == 'POST':
        factura.descripcion = request.POST.get('descripcion', factura.descripcion)
        factura.numero = request.POST.get('numero', factura.numero)
        factura.nit = request.POST.get('nit', factura.nit)
        factura.fecha = request.POST.get('fecha', factura.fecha)
        factura.categoria = request.POST.get('categoria', factura.categoria)
        factura.monto = request.POST.get('monto', factura.monto)
        factura.tipo_monto = request.POST.get('tipo_monto', factura.tipo_monto)
        if request.FILES.get('archivo'):
            factura.archivo = request.FILES['archivo']
        factura.save()
        return redirect('historial_facturas')
    context = {
        'factura': factura
    }
    return render(request, 'ivapp/editar_factura.html', context)


# Vista para mostrar la imagen o archivo de la factura
from django.http import Http404
import mimetypes

@login_required(login_url='login')
def factura_archivo(request, id):
    from django.core.exceptions import PermissionDenied
    try:
        if request.user.is_superuser or (hasattr(request.user, 'rol') and request.user.rol == 'admin'):
            factura = get_object_or_404(FacturaSubida, id=id)
        else:
            factura = get_object_or_404(FacturaSubida, id=id, usuario=request.user)
    except FacturaSubida.DoesNotExist:
        raise Http404('No existe FacturaSubida que coincida con la consulta dada.')
    if not factura.archivo:
        return HttpResponse('No hay archivo adjunto para esta factura.', status=404)
    file_path = factura.archivo.path
    file_mime, _ = mimetypes.guess_type(file_path)
    if file_mime and file_mime.startswith('image/'):
        with open(file_path, 'rb') as f:
            return HttpResponse(f.read(), content_type=file_mime)
    else:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{factura.archivo.name.split("/")[-1]}"'
        return response

def Soporte(request):
    from django.core.mail import send_mail
    from django.conf import settings
    mensaje_estado = None
    mensaje_tipo = None
    if request.method == 'POST':
        nombre = request.POST.get('name', '').strip()
        correo = request.POST.get('email', '').strip()
        asunto = request.POST.get('subject', '').strip() or 'Contacto desde formulario web'
        mensaje = request.POST.get('message', '').strip()
        if nombre and correo and mensaje:
            cuerpo = f"""
Nombre: {nombre}
Correo: {correo}
Asunto: {asunto}
Mensaje:
{mensaje}
"""
            try:
                send_mail(
                    f"[Soporte IVACOL] {asunto}",
                    cuerpo,
                    settings.DEFAULT_FROM_EMAIL,
                    ['ivacolom.app@gmail.com'],
                    fail_silently=False
                )
                mensaje_estado = '¡Mensaje enviado correctamente! Nos pondremos en contacto contigo pronto.'
                mensaje_tipo = 'success'
            except Exception as e:
                mensaje_estado = 'Ocurrió un error al enviar el mensaje. Intenta de nuevo más tarde.'
                mensaje_tipo = 'error'
        else:
            mensaje_estado = 'Por favor completa todos los campos obligatorios.'
            mensaje_tipo = 'error'
    return render(request, 'ivapp/soporte.html', {'mensaje_estado': mensaje_estado, 'mensaje_tipo': mensaje_tipo})

# --- NOTIFICACIONES ---
from .models import Notification
from django.views.decorators.http import require_POST

@login_required(login_url='login')
def api_notificaciones_usuario(request):
    notificaciones = Notification.objects.filter(user=request.user).order_by('-fecha')
    data = [
        {
            'id': n.id,
            'tipo': n.tipo,
            'titulo': n.titulo,
            'mensaje': n.mensaje,
            'fecha': n.fecha.strftime('%Y-%m-%d'),
            'leida': n.leida,
        }
        for n in notificaciones
    ]
    return JsonResponse({'notificaciones': data})

@csrf_exempt
@require_POST
@login_required(login_url='login')
def api_marcar_notificacion_leida(request):
    import json
    try:
        body = json.loads(request.body)
        notif_id = body.get('id')
        notif = Notification.objects.get(id=notif_id, user=request.user)
        notif.leida = True
        notif.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
def soporte_contacto(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        nombre = data.get('name', '').strip()
        email = data.get('email', '').strip()
        mensaje = data.get('message', '').strip()
        if not nombre or not email or not mensaje:
            return JsonResponse({'success': False, 'error': 'Faltan campos obligatorios.'}, status=400)
        try:
            # 1. Enviar mensaje al equipo de soporte
            cuerpo = f"""
Nombre: {nombre}
Correo: {email}
Mensaje:
{mensaje}
"""
            send_mail(
                subject='[Contacto IVACOL] Nuevo mensaje de contacto',
                message=cuerpo,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['ivacolom.app@gmail.com'],
                fail_silently=False,
            )
            # 2. Enviar confirmación al usuario
            send_mail(
                subject='IVACOL - Hemos recibido tu mensaje',
                message='Hemos recibido tu mensaje, nos comunicaremos tan pronto como sea posible.\n\nGracias por contactarnos.\n\nEquipo IVACOL',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)