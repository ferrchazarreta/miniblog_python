﻿# EFI PYTHON 

Mini blog simple creado en flask 

## Instalación

1. Clonar este repositorio de manera local

```bash
git clone 
```

2. Situarce en el directorio del proyecto:

```bash
cd tuProyecto
```

## Configuración

Copiae el archivo `.env.sample` y renómbralo como `.env`

Edita el archivo `.env` y cambia todos los valores necesarios

## Ejecución

Para ejecutar la aplicacion segui estos pasos:

Para Linux
```bash
sudo python3 -m venv env
```

Para Windows
```bash
sudo py -3 -m venv env
```
Activar el entorno virtual
```bash
sudo source/env/Scripts/activate
```

Instalar los requerimientos

```bash
pip install -r requirements.txt
```
Realizar las migraciones correspondientes

```bash
flask db init
```

```bash
flask db migrate -m "creacion_tablas"
```

```bash
flask db upgrade
```

Teniendo todo creado, ya se puede correr la aplicacion flask


```bash
flask run --reload
```

## Integrantes
- Chazarreta Fernando
- Gurrea Mateo