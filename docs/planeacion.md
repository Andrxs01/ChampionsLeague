# 📌 Planeación del Proyecto Integrador – Champions League 2017/18

## 🎯 Objetivo del Proyecto

Diseñar e implementar un sistema web que permita gestionar información de jugadores y equipos de la Champions League 2017/18, brindando funcionalidades como registro, consulta, edición y eliminación lógica, utilizando FastAPI, base de datos y despliegue web.

## 📚 Fuente de los Datos

- Archivo CSV original con estadísticas reales de jugadores y equipos de la temporada 2017/18.
- Datos obtenidos de [transfermarkt.com](https://www.transfermarkt.com), [uefa.com](https://www.uefa.com) y fuentes deportivas.

---

## 👤 Casos de Uso

### ✔️ Registrar un nuevo jugador
- **Actor**: Administrador
- **Acción**: Llenar formulario con los datos del jugador.
- **Resultado**: Jugador almacenado en la base de datos.

### ✔️ Consultar jugador por ID o nombre
- **Actor**: Usuario
- **Acción**: Introducir ID o nombre del jugador.
- **Resultado**: Visualización del jugador con sus estadísticas.

### ✔️ Modificar información del jugador
- **Actor**: Administrador
- **Acción**: Editar datos desde un formulario.
- **Resultado**: Información actualizada.

### ✔️ Eliminar jugador (eliminación lógica)
- **Actor**: Administrador
- **Acción**: Oprimir botón de eliminación.
- **Resultado**: El jugador es marcado como eliminado (pero no se borra).

---

## 🧩 Modelo de Datos

### Jugador
- `id`: int
- `nombre`: str
- `equipo`: str
- `posición`: str
- `edad`: int
- `nacionalidad`: str
- `goles`: int
- `asistencias`: int
- `eliminado`: bool
- `eliminado_logico`: bool

### Equipo
- `id`: int
- `nombre`: str
- `país`: str
- `grupo`: str
- `eliminado`: bool
- `eliminado_logico`: bool

---

## 📷 Diagrama del Modelo de Datos

![Modelo de Datos](modelo_datos.png)

- Un equipo puede tener muchos jugadores.
- Un jugador pertenece a un equipo.
- La relación es de uno a muchos.

---

## 📂 Estructura inicial del proyecto

