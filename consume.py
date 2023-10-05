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

    # Primero, buscar en "url" y rellenar con "url2" si se encuentran datos
    url = "http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/GetInformacionByRut/" + RUT
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))

            Datos = []  # Inicializar Datos como una lista

            if data:
                for a in data:
                    Datos.append({
                        "Identificacion": a['Rut'],
                        "Email": a['eMail'],
                        "Name": a['Nombre'],
                        "LastName": a['Apellido_Paterno'] + " " + a['Apellido_Materno'],
                        "Phone": "",
                        "Cellphone": "",
                        "Careers": a['codCarrera'],
                        "id": '',
                    })

                    aux = a['eMail'].replace('@', ' ').split()
                    url2 = "http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/Informacion/Datos/" + aux[0]

                    response2 = urllib.request.urlopen(url2)
                    data2 = json.loads(response2.read().decode('utf-8'))

                    if data2:
                        for b in data2:
                            tipo_codigo = int(b['Codigo_Tipo'])
                            type_mapping = {
                                1: "Pregrado",
                                2: "Curso",
                                3: "Diplomado",
                                4: "Magíster",
                                5: "Doctorado",
                                6: "Especialidad",
                                7: "Otro",
                                8: "Postítulo",
                                9: "Licenciatura",
                                10: "Posgrado"
                            }

                            Datos[-1].update({
                                "Codigo_Alumno": str(b['Codigo_Alumno']),
                                "InitialYear": str(b['Periodo_Actual']),
                                "Endyear": str(b['Promocion']),
                                "CentreId": str(b['Codigo_Tipo']),
                                "ProgramName": str(b['Descripcion_Tipo']),
                                "FacultyId": str(b['Campus']),
                                "Type": type_mapping.get(tipo_codigo, '-'),  # Mapear el valor de Codigo_Tipo
                                "State": str(b['Periodo_Actual']),
                            })

            # Si se encontraron datos en "url", retornar la lista de Datos
            if Datos:
                return Datos

    except Exception as e:
        print("Error:", e)

    # Si no se encontraron datos en "url", entonces buscar en "Alumni"
    url_alumni = "https://api-gw.int.udd.cl/3rabase/api/Persona/InfoPersona/"+ RUT + "-" + str(dv)
    try:
        response_alumni = urllib.request.urlopen(url_alumni)
        if response_alumni.status == 200:
            alumni_data = json.loads(response_alumni.read().decode('utf-8'))

            if 'model' in alumni_data:
                alumni_model = alumni_data['model']
                Datos = [{
                    "Identificacion": alumni_model['run'],
                    "Email": alumni_model['correoPersona'],
                    "Name": alumni_model['nombres'],
                    "LastName": alumni_model['primerApellido'] + " " + alumni_model['segundoApellido'],
                    "Phone": alumni_model['celularPersona'],
                    "Cellphone": alumni_model['celularPersona'],
                    "Careers": [alumni_model['carrera']],  # Puede haber múltiples carreras en Alumni
                    "Type": '',
                    "id": alumni_model['idPersona'],
                    "State": '',
                    "Codigo_Alumno": alumni_model['idPersona'],
                    "InitialYear": alumni_model['fechaTitulo'],
                    "Endyear": alumni_model['añoEgresoEM'],
                    "CentreId": '',
                    "ProgramName": alumni_model['titulo'],
                    "FacultyId": alumni_model['universidadId'],
                    "State": alumni_model['personaEducacionUniversidad'] 
                }]

                aux = alumni_model['correoPersona'].replace('@', ' ').split()
                url2 = "http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/Informacion/Datos/" + aux[0]

                response2 = urllib.request.urlopen(url2)
                data2 = json.loads(response2.read().decode('utf-8'))

                if data2:
                    for b in data2:
                        tipo_codigo = int(b['Codigo_Tipo'])
                        type_mapping = {
                            1: "Pregrado",
                            2: "Curso",
                            3: "Diplomado",
                            4: "Magíster",
                            5: "Doctorado",
                            6: "Especialidad",
                            7: "Otro",
                            8: "Postítulo",
                            9: "Licenciatura",
                            10: "Posgrado"
                        }

                        Datos[0].update({
                            "Type": type_mapping.get(tipo_codigo, '-'),  # Mapear el valor de Codigo_Tipo
                        })
                return Datos

    except Exception as e:
        print("Error:", e)

    return None
    
#http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/GetInformacionByRut
#http://wscache.udd.net/Pregrado/PregradoAcademico/WSPreAcad.svc/JsonAlumno/Informacion/Datos/
#https://api-gw.int.udd.cl/3rabase/api/Persona/InfoPersona/9511220-k
#https://api-gw-test.int.udd.cl/3rabase/api/Persona/InfoPersona/9511220-k
