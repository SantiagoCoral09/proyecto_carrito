from flask import Flask, flash, redirect, render_template, request, session, url_for
from . import carrito
import sqlite3
from funciones import getLoginDetails, getProductDetails, getCartDetails

@carrito.route('/agregar', methods = ['POST', 'GET'])
def agregar():
    if 'email' not in session:
        return redirect('/login/')
    datos, itms_carrito = getLoginDetails(session['email'])
    UserId=datos[0]
    
    if request.method == 'POST':
        #Obtenemos los datos del formulario
        cantidad = int(request.form['cantidad'])
        productId = request.form['productId']

        producto=getProductDetails(productId)
        stock=producto[5] ##Es cuantas unidaddes hay disponibles
        precio_unidad=producto[2]
        categoria=producto[6]

        if cantidad>stock:
            flash(f"La cantidad solicitada no puede ser mayor a {stock}","danger")
            return render_template("detalles.html", producto=producto, itms_carrito=itms_carrito)
        
        stock-=cantidad
        precio_total=cantidad*precio_unidad

        try:
           
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO kart(userId,productId,productCantidad,precio) values (?,?,?,?)",(UserId,productId,cantidad,precio_total))
            con.commit()
            cur.execute("UPDATE productos SET cantidad=? WHERE productId = ?", (stock,productId, ))
            con.commit()
            con.close()
            flash("Se agregó exitosamente","success")
            return redirect(f"/{categoria}/1")

        except Exception as e:
            flash(f"Error en la operación de inserción {e}","danger")
            return redirect('/')
        
        
@carrito.route('/mostrar')
def mostrar():
    if 'email' not in session:
        return redirect('/login/')
    usuario,itms_carrito=getLoginDetails(session['email'])
    userId=usuario[0]
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT kartId, productos.productId, productos.nombre, productos.precio, productos.imagen, kart.productCantidad, kart.precio FROM productos, kart WHERE productos.productId = kart.productId AND kart.userId = ?", (userId, ))
        productos = cur.fetchall()
    conn.close()
    # print(productos)
    precio_total=0
    for product in productos:
        precio_total+=product[6]
    

    return render_template('mostrar.html', itms_carrito=itms_carrito, productos=productos, precio_total=precio_total)

@carrito.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect('/login/')

    email = session['email']
    kartId = int(request.args.get('kartId'))

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        usuario,itms_carrito=getLoginDetails(session['email'])
        userId=usuario[0]
        try:
            cur.execute("SELECT productId, productCantidad FROM kart WHERE kartId = ?", (kartId, ))
            datos=cur.fetchone()
            # print(datos)
            productId = datos[0]
            cantidad = datos[1]
            # print("ids",productId, cantidad)

            cur.execute("DELETE FROM kart WHERE kartId = ?", (kartId,))
            con.commit()
            producto=getProductDetails(productId)
            stock=producto[5] ##Es cuantas unidaddes hay disponibles
            precio_unidad=producto[2]
            categoria=producto[6]
            stock+=cantidad
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("UPDATE productos SET cantidad=? WHERE productId = ?", (stock,productId, ))
            con.commit()
            flash("Se sacó el producto del carrito","success")
            return redirect('/mostrar')
        except Exception as e:
            flash(f"Ocurrió un error {e}","danger")
            return redirect('/mostrar')
        finally:
            con.close()
