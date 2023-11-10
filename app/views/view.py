from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for
)

from app import app, db, jwt

from app.models.models import (
    Usuario,
    Post,
    Categoria,
    Comentario,
)

from app.schemas.schema import (
    PostSchema,
    UsuarioSchema,
    ComentarioSchema,
    CategoriaSchema,
)

from datetime import datetime, timedelta

#Importar librerias para hash de password
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

#<------------------------------------Inicio UsuarioAPI------------------------------------>
from flask.views import MethodView
class UsuarioAPI(MethodView): 
    def get(self, usuario_id = None):
        if usuario_id == None:
            usuarios = Usuario.query.all()
            usuarios_schema = UsuarioSchema().dump(usuarios, many=True)
        else:
            usuarios = Usuario.query.get(usuario_id)
            usuarios_schema = UsuarioSchema().dump(usuarios)
        return jsonify(usuarios_schema)

    def post(self):
        usuario_json = UsuarioSchema().load(request.json)
        nombre = usuario_json.get('nombre')
        correo = usuario_json.get('correo')
        clave = usuario_json.get('clave')
        is_admin = usuario_json.get('is_admin')

        clave_hash = generate_password_hash(
        clave, method='pbkdf2', salt_length=8)

        nuevo_usuario = Usuario(nombre=nombre,correo=correo,is_admin=is_admin, clave=clave_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({
            'Data recibida': 'OK',
            'nombre':nombre,
            'clave_hash':clave_hash,
            'correo':correo,
            'is_admin':is_admin
        },200)

    def put(self, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        usuario_json = UsuarioSchema().load(request.json)
        nombre = usuario_json.get('nombre')
        correo = usuario_json.get('correo')
        clave = usuario_json.get('clave')
        is_admin =usuario_json.get('is_admin')

        clave_hash = generate_password_hash(
        clave, method='pbkdf2', salt_length=8)

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.clave = clave_hash
        usuario.is_admin = is_admin

        db.session.commit()
        return jsonify(UsuarioSchema().dump(usuario))

    def delete (self,usuario_id):
        usuario = Usuario.query.get(usuario_id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify(Mensaje = 'Usuario Eliminado')

app.add_url_rule('/usuario', view_func = UsuarioAPI.as_view('usuario'))
app.add_url_rule('/usuario/<usuario_id>', view_func = UsuarioAPI.as_view('usuario_id'))

#<------------------------------------Fin UsuarioAPI------------------------------------>

#<------------------------------------Inicio PostAPI------------------------------------>
class PostAPI(MethodView):
    def get(self,post_id=None):
        if post_id == None:
            posts = Post.query.all()
            posts_schema = PostSchema().dump(posts, many=True)
        else:
            posts = Post.query.get(post_id)
            posts_schema = PostSchema().dump(posts)
        return jsonify(posts_schema)

    def post(self):
        post_json = PostSchema().load(request.json)
        titulo = post_json.get('titulo')
        contenido = post_json.get('contenido')
        fecha_creacion = post_json.get('fecha_creacion')
        autor_id = post_json.get('autor_id')
        categoria_id = post_json.get('categoria_id')
        nuevo_post = Post(titulo=titulo,contenido=contenido,fecha_creacion=fecha_creacion,autor_id=autor_id,categoria_id=categoria_id)
        db.session.add(nuevo_post)
        db.session.commit()
        return jsonify(Mensaje = '¡Nuevo post creado!')
    
    def put(self,post_id):
        post = Post.query.get(post_id)
        post_json = PostSchema().load(request.json)
        titulo = post_json.get('titulo')
        contenido = post_json.get('contenido')
        fecha_creacion = post_json.get('fecha_creacion')
        autor_id = post_json.get('autor_id')
        categoria_id = post_json.get('categoria_id')

        post.titulo = titulo
        post.contenido = contenido
        post.fecha_creacion = fecha_creacion
        post.autor_id = autor_id
        post.categoria_id = categoria_id

        db.session.commit()
        return jsonify(PostSchema().dump(post))
    
    def delete (self,post_id):
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify(Mensaje='Post Eliminado')

app.add_url_rule('/post', view_func = PostAPI.as_view('post'))
app.add_url_rule('/post/<post_id>', view_func = PostAPI.as_view('post_id'))

#<------------------------------------Fin PostAPI------------------------------------>

#<------------------------------------Inicio ComentarioAPI------------------------------------>
class ComentarioAPI(MethodView):
    def get(self,comentario_id=None):
        if comentario_id == None:
            comentarios = Comentario.query.all()
            comentarios_schema = ComentarioSchema().dump(comentarios, many=True)
        else:
            comentarios = Comentario.query.get(comentario_id)
            comentarios_schema = ComentarioSchema().dump(comentarios)
        return jsonify(comentarios_schema)

    def post(self):
        comentario_json = ComentarioSchema().load(request.json)
        texto_comentario = comentario_json.get('texto_comentario')
        fecha_creacion = comentario_json.get('fecha_creacion')
        autor_id = comentario_json.get('autor_id')
        post_id = comentario_json.get('post_id')
        nuevo_comentario = Comentario(texto_comentario=texto_comentario, fecha_creacion=fecha_creacion,autor_id=autor_id,post_id=post_id)
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify(Mensaje = '¡Nuevo comentario creado!')
    
    def put(self,comentario_id):
        comentario = Comentario.query.get(comentario_id)
        comentario_json = ComentarioSchema().load(request.json)
        texto_comentario = comentario_json.get('texto_comentario')
        fecha_creacion = comentario_json.get('fecha_creacion')
        autor_id = comentario_json.get('autor_id')
        post_id = comentario_json.get('post_id')

        comentario.texto_comentario = texto_comentario
        comentario.fecha_creacion = fecha_creacion
        comentario.autor_id = autor_id
        comentario.post_id = post_id

        db.session.commit()
        return jsonify(ComentarioSchema().dump(comentario))
    
    def delete (self,comentario_id):
        comentario = Comentario.query.get(comentario_id)
        db.session.delete(comentario)
        db.session.commit()
        return jsonify(Mensaje='Comentario Eliminado')

app.add_url_rule('/comentario', view_func = ComentarioAPI.as_view('comentario'))
app.add_url_rule('/comentario/<comentario_id>', view_func = ComentarioAPI.as_view('comentario_id'))

#<------------------------------------Fin ComentarioAPI------------------------------------>

#<------------------------------------Inicio CategoriaAPI------------------------------------>
class CategoriaAPI(MethodView): 
    def get(self, categoria_id = None):
        if categoria_id == None:
            categorias = Categoria.query.all()
            categorias_schema = CategoriaSchema().dump(categorias, many=True)
        else:
            categoria = Categoria.query.get(categoria_id)
            categorias_schema = CategoriaSchema().dump(categoria)
        return jsonify(categorias_schema)

    def post(self):
        categoria_json = CategoriaSchema().load(request.json)
        categoria = categoria_json.get('categoria')
        nuevo_categoria = Categoria(categoria=categoria)
        db.session.add(nuevo_categoria)
        db.session.commit()
        return jsonify(Mensaje = '¡Nueva categoria creada!')

    def put(self, categoria_id):
        categoria_edit = Categoria.query.get(categoria_id)
        categoria_json = CategoriaSchema().load(request.json)
        categoria = categoria_json.get('categoria')

        categoria_edit.categoria = categoria

        db.session.commit()
        return jsonify(Mensaje = '¡Categoria Modificada!')

    def delete (self,categoria_id):
        categoria = Categoria.query.get(categoria_id)
        db.session.delete(categoria)
        db.session.commit()
        return jsonify(Mensaje = 'Categoria Eliminada')

app.add_url_rule('/categoria', view_func = CategoriaAPI.as_view('categoria'))
app.add_url_rule('/categoria/<categoria_id>', view_func = CategoriaAPI.as_view('categoria_id'))

#<------------------------------------Fin CategoriaAPI------------------------------------>

class Login(MethodView):
    def get(self):
        data = request.authorization
        nombre_usuario = data.get('username')
        clave_usuario = data.get('password')

        user = Usuario.query.filter_by(nombre = nombre_usuario).first()
        is_admin = user.is_admin

        if user and check_password_hash(user.clave, clave_usuario):
            access_token = create_access_token(
                identity=nombre_usuario,
                expires_delta=timedelta(minutes=1),
                additional_claims=dict(
                    is_admin=is_admin
                )
            )
            return jsonify({'ok':access_token})
        return jsonify(Error='No puede generar el token'),400   
app.add_url_rule('/login', view_func = Login.as_view('login')) 

class Ruta_Login(MethodView):
    @jwt_required()
    def get(self):
        usuario_actual = get_jwt_identity()
        info_extra = get_jwt()
        if info_extra['is_admin']==1:
            return jsonify(
                {
                    "Mensaje":f"El usuario {usuario_actual} tiene acceso a esta ruta",
                    "Info Adicional": info_extra
                }
            )
        return jsonify(
                {
                    "Mensaje":f"El usuario {usuario_actual} no tiene acceso a esta ruta",
                }
            )
app.add_url_rule('/ruta_login', view_func = Ruta_Login.as_view('ruta_login'))

@jwt.invalid_token_loader
def unauthorized_user(reason):
    return jsonify(mensaje=f"Acceso denegado porque : {reason}"), 401

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(mensaje=f"El Token a expirado"),401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(mensaje=f"Token no ingresado"),401
            

                   
@app.context_processor
def inject_categorias():
    categorias = db.session.query(Categoria).all()
    return dict(
        categorias = categorias
    )

@app.context_processor
def inject_posts():
    posts = db.session.query(Post).all()
    posts = reversed(posts)
    return dict(
        posts = posts
    )

@app.context_processor
def inject_comentarios():
    comentarios = db.session.query(Comentario).all()
    return dict(
        comentarios = comentarios
    )

@app.route('/')
def index():
   return render_template(
       'index.html'
    )

@app.route('/inicio_sesion', methods=['POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email_usuario = request.form['email']
        clave_usuario = request.form['clave']
        usuarios = db.session.query(Usuario).filter_by(
                    correo = email_usuario,clave = clave_usuario
                    ).all()
        try:
            usuario_id = usuarios[0].id
            return redirect(url_for('inicio', usuario_id = usuario_id))
        except:
            return redirect(url_for('index'))
        
@app.route('/registro', methods=['POST'])
def registro():
    return render_template('registrarse.html')

@app.route('/registrarse', methods=['POST'])
def registrarse():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        email_usuario = request.form['email']
        clave_usuario = request.form['clave']
        
        #Instancia
        nuevo_usuario = Usuario(nombre = nombre_usuario, 
                                correo = email_usuario,
                                clave = clave_usuario)
        #Agregar Instancia
        db.session.add(nuevo_usuario)
        #Guardar Instancia 
        db.session.commit()
    return(redirect(url_for('index')))

@app.route('/inicio')
def inicio():
    usuario_id = request.args['usuario_id']
    usuario_id = int(usuario_id)
    usuario = db.session.query(Usuario).filter_by(
              id = usuario_id
              ).all()
    
    usuario_nombre = usuario[0].nombre
    return render_template(
        'inicio.html',
        usuario_id = usuario_id,
        usuario_nombre = usuario_nombre,
        logeado = True
    )

@app.route('/crear_post', methods=['POST'])
def crear_post():
    if request.method=='POST':
        usuario_id = request.form['usuario_id']
        
        titulo = request.form['titulo']        
        contenido = request.form['contenido']       
        categoria_id = request.form['categoria']

        fecha = datetime.now()
        
        #Instancia
        nuevo_post = Post(titulo = titulo, 
                          contenido = contenido, 
                          fecha_creacion = fecha, 
                          autor_id = usuario_id, 
                          categoria_id = categoria_id)
        #Agregar Instancia
        db.session.add(nuevo_post)
        #Guardar Instancia
        db.session.commit() 
        return redirect(url_for('inicio', usuario_id = usuario_id))
    
@app.route('/crear_comentario', methods=['POST'])
def crear_comentario():
    if request.method=='POST':
        contenido = request.form['contenido']       
        fecha = datetime.now()
        usuario_id = request.form['usuario_id']
        post_id = request.form['post_id']
        
        #Instancia
        nuevo_comentario = Comentario(texto_comentario = contenido,
                                      fecha_creacion = fecha, 
                                      autor_id = usuario_id, 
                                      post_id = post_id)
        #Agregar Instancia
        db.session.add(nuevo_comentario)
        #Guardar Instancia
        db.session.commit() 
        return redirect(url_for('inicio', usuario_id = usuario_id))

@app.route("/borrar_post", methods=['POST'])
def borrar_post():
    if request.method=='POST':
        usuario_id = request.form['usuario_id']
        
        post_id = request.form['post_id']

        comentarios = db.session.query(Comentario).filter_by(
                      post_id = post_id
                      ).all()
        for comentario in comentarios:
            db.session.delete(comentario)
            db.session.commit()
        post = Post.query.get(post_id)
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('inicio', usuario_id = usuario_id))

@app.route("/editar", methods=['POST'])
def editar():
    if request.method=='POST':
        usuario_id = request.form['usuario_id']
        post_id = request.form['post_id']
        post = Post.query.get(post_id)
        titulo = post.titulo
        contenido = post.contenido
        return render_template(
            'editar.html',
            titulo = titulo,
            contenido = contenido,
            usuario_id = usuario_id,
            post_id = post_id,
            logeado = True
        )
    
@app.route("/editar_post", methods=['POST'])
def editar_post():
    if request.method=='POST':
        usuario_id = request.form['usuario_id']
        post_id = request.form['post_id']
        titulo_editado = request.form['titulo_editado']
        contenido_editado = request.form['contenido_editado']

        post = Post.query.get(post_id)
        post.titulo = titulo_editado
        post.contenido = contenido_editado
        db.session.commit()

    return redirect(url_for('inicio', usuario_id = usuario_id))