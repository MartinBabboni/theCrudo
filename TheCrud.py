import json
import os
from pathlib import Path


def menu():
    opcion = ''
    while opcion!= 's': # mantiene dentro del menú principal, a menos que se desee salir.
        print("\nMenú\n¿Qué acción desea realizar?")
        print("1 - Crear un nuevo registro en empleados\n2 - Leer información sobre los empleados\n3 - Actualizar los registros\n4 - Eliminar un registro\nS - Salir")
        opcion=input('=> ').lower()
        if opcion == '1':
            crearUsuario()
        elif opcion == '2':
            leerInformacion()
        elif opcion == '3':
            actualizarDatos()
        elif opcion == '4':
            eliminarRegistro()
        elif opcion == 's':
            print('\nGracias por utilizar nuestro sistema.\nTenga usted un buen día.')
        else:
            print('\nNo podemos procesar la opción elegida.\nPor favor elija una de las siguientes opciones.')


# opción 1 del Menú principal
def crearUsuario():
    global nId  # no entendí porqué pero esta variable, y no otras, si no la declaraba como global no la reconocia.
    nombre = input('\nIngrese el nombre del empleado\n=> ').title()
    apellido = input('Ingrese el apellido del empleado\n=> ').title()

    puesto =''
    while puesto=='': # Mientras no se asigne un puesto valido se mantiene en el loop.
        puesto = input(f'Ingrese el puesto de {nombre}. Debe ser alguno de los siguientes:\nAdministrativo\nPeón\nGerente\n=> ').title()
        if puesto not in puestos: # comprueba que esté en la lista de puestos posibles.
            puesto=''
            print('El puesto elegido no se encuentra dentro de las opciones disponibles')
    if puesto =='Peon': # acepta peon o Peon como valido y lo corrige.
        puesto ='Peón'

    mail = input(f'Ingrese el mail de {nombre} => ')

    baseDatos.setdefault(nId, [apellido, nombre, puesto, mail]) # ingresa el registro en la base de datos.

    print(f'\nSe creó el siguiente registro para {nombre} {apellido}: ')
    presentarInfoParticular(nId) # Llama a la función para presentar los datos.
    nId += 1 # aumenta el nro de ID cada vez que se genera un registro.


# opción 2 del Menún principal
def leerInformacion():
    infogeneral() # llama a una función que brinda información resumida.
    opcion = input('\nSi desea más información ingrese S.\nIngrese otra opción por No.\n => ').lower()
    if opcion != 's':
        return  # cualquier ingreso distinto de s me vuelve al menú principal.
    else:
        print('\n¿Qué información le gustaría conocer:')
        opcion2 = input('\n1 - Datos de un empleado en particular\n2 - Datos de los gerentes\n3 - Datos de los administrativos\n4 - Datos de los peones\n=> ')
        if opcion2 =='1':
            datosparticulares()
        elif opcion2 =='2':
            datosdegerentes()
        elif opcion2 =='3':
            datosdeadmin()
        elif opcion2 =='4':
            datosdepeon()
        else:
            print('No disponemos de la opción elegida, si desea conocer información de los empleados\nvuelva a elegir la opción 2 del menú principal')


def infogeneral(): # contador de empleados y puestos.
    totalpeones = 0
    totalAdmin = 0
    totalGerentes = 0
    for empleado in baseDatos.values():
        if empleado[2] == 'Peón':
            totalpeones += 1
        elif empleado[2] == 'Administrativo':
            totalAdmin += 1
        elif empleado[2] == 'Gerente':
            totalGerentes += 1
    totalempleados = totalpeones + totalAdmin + totalGerentes
    print(f'\nLa empresa cuenta con {totalempleados} empleados.')
    print(f'Gerentes: {totalGerentes}')
    print(f'Administrativos: {totalAdmin}')
    print(f'Peones: {totalpeones}')


def datosparticulares(): # presenta los datos para un registro en particular
    opcion = input('\n¿Cómo desea realizar la búsqueda?\n1 - Por nombre y apellido\n2 - Por Id\n=> ')
    if opcion != '1' and opcion != '2':
        print('La opción elegida no está en el menú\n')
    else:
        if opcion == '1':
            nroId = buscarNyA()
        else:
            nroId = buscarId()
        if nroId != None:
            presentarInfoParticular(nroId)


def buscarNyA(): # esta función recorre el diccionario tomando como parametros el nombre y el apellido,
                 # devuelve el ID correspondiente o None si no hay datos.
    nombre = input('Ingrese el nombre: ').title()
    apellido =input ('Ingrese el apellido: ').title()
    for empleado in baseDatos.items():
        if empleado[1][0] == apellido and empleado[1][1] == nombre:
            return empleado[0]
    print(f'{nombre} {apellido} no se encuentra en nuestros registros\n')
    return None


def buscarId(): # Esta función verifica si la ID buscada está en el diccionario.
                # Si la ID está en el diccionario verifica que contenga datos (que no hayan sido borrados)
                # Devuelve el ID correspondiente o None si no hay datos.
    nroId = input('\nIngrese el número de Id => ')
    if nroId in baseDatos and baseDatos[nroId][0]!= 0:
        return nroId
    else:
        print('No tenemos registros para la Id elegida\n')
        return None


def presentarInfoParticular(nroId): # Esta función presenta los datos de una Id en particular.
        print('\nId:', nroId)
        print('Apellido: ', baseDatos[nroId][0])
        print('Nombre: ', baseDatos[nroId][1])
        print('Puesto: ', baseDatos[nroId][2])
        print('e-mail: ', baseDatos[nroId][3])
        input('\nIngrese Enter continuar\n')


def datosdegerentes():
    contador=0
    print('Empleados que ocupan puestos gerenciales en la empresa:')
    for empleado in baseDatos.items():
        if empleado[1][2] == 'Gerente':
            presentarInfoParticular(empleado[0])
        else:
            contador +=1
    if contador == totalempleados:
        print('La empresa no cuenta con empleados en el puesto de gerente\n')

def datosdeadmin():
    contador=0
    print('Empleados que ocupan puestos de administración en la empresa:')
    for empleado in baseDatos.items():
        if empleado[1][2] == 'Administrativo':
            presentarInfoParticular(empleado[0])
        else:
            contador +=1
    if contador == totalempleados:
        print('La empresa no cuenta con empleados en el puesto de administración\n')

def datosdepeon():
    contador=0
    print('Empleados que ocupan un puesto de peón en la empresa:')
    for empleado in baseDatos.items():
        if empleado[1][2] == 'Peón':
            presentarInfoParticular(empleado[0])
        else:
            contador +=1
    if contador == totalempleados:
        print('La empresa no cuenta con empleados en el puesto de peón\n')


# opción 3 del Menún principal
def actualizarDatos():
    opcion3 = input('\n¿Cómo desea identificar los datos a actualizar?\n1 - Por nombre y apellido\n2 - Por Id\n=> ')
    if opcion3 != '1' and opcion3 != '2':
        print('La opción elegida no está en el menú')
    else:
        if opcion3 == '1':
            nroId = buscarNyA()
        else:
            nroId = buscarId()
        if nroId != None:
            print('Datos registrados: ')
            presentarInfoParticular(nroId)
            nombre = input('Ingrese el nuevo nombre o Enter si desea conservar el nombre actual\n=> ').title()
            if nombre !='':
                baseDatos[nroId][1] = nombre
            apellido = input('Ingrese el nuevo apellido o Enter si desea conservar el apellido actual\n=> ').title()
            if apellido !='':
                baseDatos[nroId][0] = apellido
            while True:
                puesto = input('Ingrese el nuevo puesto o Enter si desea conservar el puesto actual\n=> ').title()
                if puesto !='' and puesto in puestos:
                    if puesto =='Peon':
                        puesto ='Peón'
                    baseDatos[nroId][2] = puesto
                    break
                elif puesto =='':
                    break
                else:
                    print('El puesto elegido no está dentro de las opciones. Debe ser Gerente, Administrativo o Peón')
            mail = input('Ingrese el nuevo e-mail o Enter si desea conservar el e-mail actual\n=> ')
            if mail !='':
                baseDatos[nroId][3] = mail
            print('Se actualizaron los datos')
            presentarInfoParticular(nroId)


# opción 4 del Menún principal
def eliminarRegistro():
    opcion3 = input('¿Cómo desea identificar los datos a eliminar?\n1 - Por nombre y apellido\n2 - Por Id\n=> ')
    if opcion3 != '1' and opcion3 != '2':
        print('La opción elegida no está en el menú')
    else:
        if opcion3 == '1':
            nroId = buscarNyA()
        else:
            nroId = buscarId()
        if nroId != None:
            print('Se eliminará el siguiente registro: ')
            presentarInfoParticular(nroId)
            confirmar = input('¿Desea eliminar el registro?\nS - Confirmar\nOtra opción para NO\n=> ').lower()
            if confirmar == 's':
                baseDatos[nroId] = [0,0,0,0]


arch = Path (os.getcwd(),'TheCrud.json') # crea un objeto path con la direccion del archivo .json, siempre que el archivo .json debe estar en la misma dirección del script.
# os.getcwd() me da la direccion del script, esto me funciona en linux, en windows no. No se por qué.
# Se supone que con Path podría abrir direcciones de Windows que van con \ y de linux que van con /
# algo así en Windows 'C:\MisDocumentos\...\TheCrud.json'
# y así en linux '/home/../TheCrud.json'
# Path hace su gracia, pero os.getcwd(), en Windows no me da exactamente la direccion del script.
archivo = open(arch, 'r')
baseDatos = json.load(archivo)
archivo.close()
nId = len(baseDatos)
print("Bienvenido al sistema de Gestión de Usuarios \"TheCrudo\"".center(100))
puestos = ['Administrativo', 'Peon','Peón','Gerente']
totalempleados = 0
menu()
archivo = open(arch, 'w')
json.dump(baseDatos, archivo)
archivo.close()
