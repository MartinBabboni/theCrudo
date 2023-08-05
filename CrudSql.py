import sqlite3

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
    #Acá juntamos los datos del usuario
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
    email = input(f'Ingrese el mail de {nombre} => ')

    # Acá los incorporamos a la base de datos
    elCursor.execute('insert into usuarios (nombre, apellido, puesto, email) values (?,?,?,?)',[nombre, apellido, puesto, email])
    elConector.commit()
    print(f'\nSe creó el siguiente registro para {nombre} {apellido}: ')
    elCursor.execute("SELECT MAX(id) FROM usuarios;") # para presentar los datos del usuario generado elegimos el último id
    nroId = elCursor.fetchall()[0][0] # el resultado de busqueda anterior es una lista con una tupla con el nro de Id
    presentarInfoParticular(nroId) # Llama a la función para presentar los datos.



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
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Peón'") # Se hace una cuenta de las filas de la base que cumplen con el requisito puesto ='Peón'.
    totalpeones = elCursor.fetchall()[0][0] # El resultado de la busqueda va a ser una lista con una tupla con la suma de casos.
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Administrativo'")
    totalAdmin = elCursor.fetchall()[0][0]
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Gerente'")
    totalGerentes = elCursor.fetchall()[0][0]
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


def buscarNyA(): # esta función devuelve el ID correspondiente a los datos nombre y apellido, o None si no hay datos.
    nombre = input('Ingrese el nombre: ').title()
    apellido =input ('Ingrese el apellido: ').title()
    try:
        elCursor.execute(f"SELECT * FROM usuarios WHERE nombre = '{nombre}' AND apellido ='{apellido}'")
        datos = elCursor.fetchall()[0][0]
        return datos
    except IndexError:
        print(f"No temos registros de {nombre} {apellido}")
        return None


def buscarId(): # Esta función verifica si la ID buscada está en la base de datos, el ID correspondiente o None si no hay datos.
    nroId = input('\nIngrese el número de Id => ')
    try:
        elCursor.execute(f"SELECT * FROM usuarios WHERE id = '{nroId}'")
        datos = elCursor.fetchall()[0][0]
        return datos
    except IndexError:
        print(f"No temos registrado el ID: {nroId}")
        return None


def presentarInfoParticular(nroId): # Esta función presenta los datos de una Id en particular.
    elCursor.execute(f"SELECT * FROM usuarios WHERE id ='{nroId}'")
    datos = elCursor.fetchall()[0] # la busqueda anterior devuelve una lista con una tupla. En la variable datos se guarda la tupla con la información del empleado.
    print('ID:', datos[0])
    print('Nombre:', datos[1])
    print('Apellido:', datos[2])
    print('Puesto:', datos[3])
    print('e-mail:', datos[4])


def datosdegerentes():
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Gerente'")
    totalGerentes = elCursor.fetchall()[0][0]
    if totalGerentes == 0:
        print('La empresa no cuenta con empleados en el puesto de gerente\n')
    else:
        elCursor.execute("SELECT * FROM usuarios WHERE puesto = 'Gerente'")
        datos = elCursor.fetchall()
        print('Empleados que ocupan puestos gerenciales en la empresa:')
        for empleado in datos:
            presentarInfoParticular(empleado[0])


def datosdeadmin():
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Administrativo'") # Verificamos que haya Administrativos
    totalAdmin = elCursor.fetchall()[0][0]
    if totalAdmin == 0:
        print('La empresa no cuenta con empleados en el puesto de Administrativo\n')
    else:
        elCursor.execute("SELECT * FROM usuarios WHERE puesto = 'Administrativo'") # Se hace una busqueda de todos los administrativos, que devuelve una lista con tuplas, una tupla por administrativo.
        datos = elCursor.fetchall(). # se guarda en datos la lista
        print('Empleados que ocupan puestos administrativos en la empresa:')
        for empleado in datos: # empleados representa cada tupla de la lista anterior
            presentarInfoParticular(empleado[0]) # Se llama a la función. La posición [0]  de empleados, de la tupla corresponde al ID.

def datosdepeon():
    elCursor.execute("SELECT COUNT (*) FROM usuarios WHERE puesto = 'Peón'")
    totalAdmin = elCursor.fetchall()[0][0]
    if totalAdmin == 0:
        print('La empresa no cuenta con empleados en el puesto de Peón\n')
    else:
        elCursor.execute("SELECT * FROM usuarios WHERE puesto = 'Peón'")
        datos = elCursor.fetchall()
        print('Empleados que ocupan puestos de peón en la empresa:')
        for empleado in datos:
            presentarInfoParticular(empleado[0])


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
                elCursor.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", [nombre, nroId]) # Se actualiza el dato para la Id correspondiente
            apellido = input('Ingrese el nuevo apellido o Enter si desea conservar el apellido actual\n=> ').title()
            if apellido !='':
                elCursor.execute("UPDATE usuarios SET apellido = ? WHERE id = ?", [apellido, nroId])
            while True:
                puesto = input('Ingrese el nuevo puesto o Enter si desea conservar el puesto actual\n=> ').title()
                if puesto !='' and puesto in puestos:
                    if puesto =='Peon':
                        puesto ='Peón'
                    elCursor.execute("UPDATE usuarios SET puesto = ? WHERE id = ?", [puesto, nroId])
                    break
                elif puesto =='':
                    break
                else:
                    print('El puesto elegido no está dentro de las opciones. Debe ser Gerente, Administrativo o Peón')

            mail = input('Ingrese el nuevo e-mail o Enter si desea conservar el e-mail actual\n=> ')
            if mail !='':
                elCursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", [mail, nroId])
            print('Se actualizaron los datos')
            elConector.commit() # Se registran efectivamente los nuevos datos en la Base.
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
                elCursor.execute('DELETE FROM usuarios WHERE id = ?',[nroId]) # se elimina los datos para la Id. No me convence mucho porque borra el nro de Id. ¿Está bien? o ¿sería mejor sobre escribir con none los campos?

# Conexion con la base de datos.
elConector = sqlite3.connect("ElCRUD.db")
elCursor = elConector.cursor()
try:
    elCursor.execute('''create table usuarios (
    id integer primary key,
    nombre text not null,
    apellido text not null,
    puesto text not null,
    email text not null
    )''')
    print('Se creo la tabla')
except:
    print("La tabla ya existe")

# Arranque del menú
print("Bienvenido al sistema de Gestión de Usuarios \"TheCrudo\"".center(100))

puestos = ['Administrativo','Peon','Peón','Gerente'] # ¿Por qué está acá?

menu()
elConector.close()



