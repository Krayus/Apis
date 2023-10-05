import urllib.request
import json

def calcular_digito_verificador(rut_sin_dv):
    reversed_digits = [int(digit) for digit in reversed(str(rut_sin_dv))]
    factors = [2, 3, 4, 5, 6, 7, 2, 3]
    total = sum(digit * factor for digit, factor in zip(reversed_digits, factors))
    remainder = total % 11
    dv = 11 - remainder
    return str(dv) if dv < 10 else 'K'

def get_one(RUT):
    rut_sin_dv = int(RUT.replace('-', '').lstrip('0'))
    dv = calcular_digito_verificador(rut_sin_dv)
    urlalumni = "https://api-gw.int.udd.cl/3rabase/api/Persona/InfoPersona/"+ RUT + "-" + str(dv)
    
    try:
        response_alumni = urllib.request.urlopen(urlalumni)
        if response_alumni.status == 200:
            alumni_data = json.loads(response_alumni.read().decode('utf-8'))
            
            if 'model' in alumni_data:
                alumni_model = alumni_data['model']
                Datos = {
                    "Identificacion": alumni_model['run'],
                    "Email": alumni_model['correoPersona'],
                    "Name": alumni_model['nombres'],
                    "LastName": alumni_model['primerApellido'] + " " + alumni_model['segundoApellido'],
                    "Phone": alumni_model['celularPersona'],
                    "Cellphone": alumni_model['celularPersona'],
                    "Careers": alumni_model['carrera'],
                    "Type": '-',
                    "id": alumni_model['idPersona'],
                    "State": '-',
                    "Codigo_Alumno": alumni_model['idPersona'],
                    "InitialYear": alumni_model['fechaTitulo'],
                    "Endyear": alumni_model['añoEgresoEM'],
                    "CentreId": '-',
                    "ProgramName": alumni_model['titulo'],
                    "FacultyId": alumni_model['universidadId']
                }
                return Datos
            
        # Si no se encontraron datos en urlalumni, entonces se procede a las otras URLs
        url = "http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/GetInformacionByRut/" + RUT
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            
            Datos = {}  # Inicializar Datos aquí
            
            if data:
                a = data[0]  # Se asume que solo se procesa el primer elemento de 'data'
                
                Datos = {
                    "Identificacion": a['Rut'],
                    "Email": a['eMail'],
                    "Name": a['Nombre'],
                    "LastName": a['Apellido_Paterno'] + " " + a['Apellido_Materno'],
                    "Phone": "-",
                    "Cellphone": "-",
                    "Careers": a['Carrera'],
                    "Type": a['Sistema'],
                    "id": a['codCarrera'],
                    "State": a['Sistema']
                }
                
                aux = a['eMail'].replace('@', ' ').split()
                url2 = "http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/Informacion/Datos/" + aux[0]
                
                response2 = urllib.request.urlopen(url2)
                data2 = json.loads(response2.read().decode('utf-8'))
                
                if data2:
                    b = data2[0]  # Se asume que solo se procesa el primer elemento de 'data2'
                    Datos.update({
                        "Codigo_Alumno": str(b['Codigo_Alumno']),
                        "InitialYear": str(b['Periodo_Actual']),
                        "Endyear": str(b['Promocion']),
                        "CentreId": str(b['Codigo_Tipo']),
                        "ProgramName": str(b['Descripcion_Tipo']),
                        "FacultyId": str(b['Campus'])
                    })
                    
                return Datos
            else:
                return None
        else:
            print("La solicitud no se completó correctamente")
            return None
    except Exception as e:
        print("Error:", e)
        return None