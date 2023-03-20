from flask import Flask, flash, redirect, render_template, request, session, url_for
from . import login_registro
import sqlite3

def esta_registrado(email, password):
    #Inicializamos un mensaje falso
    msg='No se encontró el correo ingresado'

    #Buscaremos si el correo se encuentra registrado
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM usuarios')
    data = cur.fetchall()
    
    #Comparamos si el correo esta en la consulta sql
    for row in data:
        if row[0] == email:
            #Si el correo se encuentra registrado cambiamos el valor de la variable
            msg='Registrado'
            if row[1] == password:
                #Ahora comparamos si la contraseña es la misma registrada
                msg='Password correcto'
            else:
                msg='La contraseña ingresada no es correcta'
    return msg

def consulta_por_email(email):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM usuarios WHERE email=?',(email,))
    data = cur.fetchone()
    return data

@login_registro.route('/login/')
def login():
    return render_template('login.html')

@login_registro.route('/iniciar_sesion', methods = ['POST', 'GET'])
def iniciar_sesion():
    if request.method == 'POST':
        #Obtenemos los datos del formulario
        email = request.form['email']
        password = request.form['password']
        
        #Verificamos si los campos estan llenos
        if email=='' or password=='':
            flash("Por favor, complete todos los campos del formulario", "danger")
            return render_template('login.html')
        ##Verificacmos si el correo está registrado, implementamos la funcion creada al inicio
        msg=esta_registrado(email, password)
        if msg=='No se encontró el correo ingresado':
            flash("El correo ingresado no está registrado", "danger")
            return render_template('login.html')
        if msg=='La contraseña ingresada no es correcta': #si esta registrado
            flash("La contraseña ingresada no es correcta", "danger")
            return render_template('login.html')
        else: #
            session['email'] = email
            datos=consulta_por_email(email)
            session['id']=datos[0]
            session['nombres']=datos[1]
            session['apellidos']=datos[2]
            session['celular']=datos[3]
            session['password']=datos[5]
            session['tipoUser']=datos[6]
            print(session)
            if session['tipoUser']=='usuario':
                flash("Inicio de sesion exitoso, ahora puedes ver nuestros productos","success")
                return redirect('/')
            else:
                return redirect('/admin')




@login_registro.route('/registro/')
def registro():
    return render_template('registro.html')

@login_registro.route('/registro_usuario', methods = ['POST', 'GET'])
def registro_usuario():
    if request.method == 'POST':
        #Obtenemos los datos del formulario
        email = request.form['email']
        password = request.form['password']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        celular = request.form['celular']

        #Verificamos si los campos estan llenos
        if email=='' or password=='' or nombres=='' or apellidos=='' or celular=='':
            flash("Por favor, complete todos los campos del formulario", "danger")
            return render_template('registro.html')
        ##Verificacmos si el correo está registrado, implementamos la funcion creada al inicio
        msg=esta_registrado(email, password)
        if msg=='Registrado' or msg=='Password correcto' or msg=='La contraseña ingresada no es correcta': #si esta registrado
            flash("El correo ingresado ya está registrado,\n ingrese otro nuevamente", "danger")
            return render_template('registro.html')
        else: #
            session['email'] = email
            try:
           
                con=sqlite3.connect("database.db")
                cur=con.cursor()
                cur.execute("INSERT INTO usuarios(nombres,apellidos,celular,email,password,tipoUser) values (?,?,?,?,?,?)",(nombres,apellidos,celular,email,password,'usuario'))
                con.commit()
                datos=consulta_por_email(email)
                session['id']=datos[0]
                session['nombres']=datos[1]
                session['apellidos']=datos[2]
                session['celular']=datos[3]
                session['password']=datos[5]
                session['tipoUser']=datos[6]
                print(session)
                con.close()
                flash("Te has registrado exitosamente, ahora puedes ver nuestros productos","success")
                return redirect('/')

            except:
                flash("Error en la operación de inserción","danger")
                return render_template('registro.html')

@login_registro.route("/logout")
def logout():
    session.clear()
    return redirect("/")
