from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = '54.157.55.8'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = 'sistemas20.'
app.config['MYSQL_DB'] = 'BDAlbum' #db_album
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM album')
    data=cur.fetchall()
    return render_template('index.html', albums = data)

@app.route('/add_album', methods=['POST'])
def add_album():
    if request.method == 'POST': #Define método de envío 
        titulo = request.form['titulo'] # request.form recoge datos de formulario
        artista = request.form['artista']
        genero = request.form['genero']
        cur = mysql.connection.cursor() #genera conexion DB SQL
        cur.execute('INSERT INTO album (titulo, artista, genero) VALUES (%s, %s, %s)', 
        (titulo, artista, genero)) # ejecuta comando SLQ datos recogidos del form
        mysql.connection.commit() # Guarda cambios en DB
        flash('Album agregado exitosamente')
        return redirect(url_for('Index')) #Redirecciona a pagina Index

@app.route('/edit/<id>')
def get_album(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM album WHERE id = %s', (id))  
    data = cur.fetchall()
    #print(data[0])
    return render_template('edit-album.html', album = data[0]) 

@app.route('/update/<id>', methods = ['POST'])
def update_album(id):
    if request.method == 'POST':
         # request.form recoge datos de formulario
        titulo = request.form['titulo']
        artista = request.form['artista']
        genero = request.form['genero']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE album
        SET titulo = %s,
            artista = %s,
            genero = %s
        WHERE id = %s
        """, (titulo,artista,genero,id ))
        mysql.connection.commit()
        flash('Album actualizado exitosamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_album(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM album WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Album eliminado exitosamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True) #3000