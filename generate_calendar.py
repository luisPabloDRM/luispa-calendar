from datetime import date, datetime, timedelta
from pathlib import Path
import uuid

START = date(2026, 8, 17)
END = date(2026, 12, 31)
OUT = Path("calendario.ics")

PREP = {
    date(2026, 8, 18): ("Entrevista - LitElement desde cero", "Web Components: Custom Elements y Shadow DOM - 15 min. LitElement, customElement, property, render y html - 20 min. Crear un componente sencillo - 30 min. Explicarlo comparandolo con Angular - 10 min."),
    date(2026, 8, 19): ("Entrevista - Web Components en profundidad", "Custom Elements y ciclo de vida - 15 min. Shadow DOM y encapsulacion - 15 min. Slots y composicion - 15 min. Eventos y comunicacion - 15 min. Ventajas y desventajas frente a Angular - 15 min."),
    date(2026, 8, 21): ("Entrevista - Practica Lit", "Crear user-card con propiedades, estado, CustomEvent, slot y estilos encapsulados - 50 min. Explicarlo como entrevista - 15 min. Anotar dudas - 10 min."),
    date(2026, 8, 23): ("Entrevista - Mini proyecto Lit", "Construir un user-card completo con propiedades, estado, CustomEvent, slot y Shadow DOM - 55 min. Explicarlo sin mirar codigo - 10 min. Anotar puntos debiles - 10 min."),
    date(2026, 8, 25): ("Entrevista - Reactividad y lifecycle en Lit", "property y state - 15 min. willUpdate, updated y callbacks - 20 min. Crear componente con estado reactivo - 25 min. Cinco preguntas tecnicas en voz alta - 15 min."),
    date(2026, 8, 26): ("Entrevista - JavaScript y TypeScript", "this y closures - 15 min. Promises, async/await y event loop - 20 min. Interfaces, types, generics y utility types - 20 min. Type narrowing y errores - 10 min. Tres preguntas tecnicas - 10 min."),
    date(2026, 8, 28): ("Entrevista - Experiencia profesional", "Preparar respuestas sobre Duonex, Angular, TypeScript, RxJS, Node, AdonisJS, APIs y bases de datos. Preparar un problema tecnico dificil y explicar como lo resolviste. Preparar por que buscas un cambio y por que te interesa el puesto. Responder todo en voz alta."),
    date(2026, 8, 30): ("Entrevista - Simulacion completa", "Simulacion de 75 min: presentacion, experiencia, LitElement, Web Components, Angular vs Lit, JavaScript/TypeScript, problemas tecnicos, motivacion y preguntas para la empresa. No estudiar teoria nueva: detectar puntos debiles."),
    date(2026, 9, 1): ("Entrevista - Repaso final", "20 min Lit/LitElement. 15 min Web Components. 15 min Angular vs Lit. 15 min experiencia profesional. 10 min preguntas personales. No aprender contenido nuevo. Terminar y descansar."),
}

POST = [
    ("Desarrollo - Angular avanzado", "Implementar una pequena feature con standalone components, signals/RxJS y separacion clara entre UI, dominio y datos. Documentar 3 decisiones tecnicas."),
    ("Desarrollo - TypeScript avanzado", "Practicar generics, constraints, Pick, Omit, Partial, Record, discriminated unions y type narrowing. Crear 3 ejemplos reutilizables."),
    ("Desarrollo - Lit y Web Components", "Construir un componente Lit reutilizable con propiedades, estado, CustomEvent, slots y Shadow DOM. Compararlo con Angular."),
    ("Desarrollo - JavaScript asincrono", "Practicar event loop, microtasks, macrotasks, Promise, async/await, errores y concurrencia. Resolver ejercicios y explicar cada resultado."),
    ("Desarrollo - RxJS", "Construir un flujo realista de busqueda con debounceTime, distinctUntilChanged, switchMap, catchError y finalize."),
    ("Desarrollo - Testing frontend", "Escribir tests de componente o servicio cubriendo happy path, errores y casos limite. Revisar mantenibilidad."),
    ("Desarrollo - Node y arquitectura", "Implementar un endpoint con validacion, controller, use case, repository y manejo de errores. Escribir pruebas basicas."),
    ("Desarrollo - Arquitectura frontend", "Disenar una pequena aplicacion: componentes, dominio, estado, API y persistencia. Justificar fronteras y evitar sobrearquitectura."),
    ("Desarrollo - Gym Tracker Pro", "Implementar una pieza pequena y vertical del proyecto: UI, dominio y datos. Priorizar una funcionalidad terminada."),
    ("Desarrollo - Entrevista tecnica JS/TS", "Responder preguntas de closures, this, prototipos, event loop, generics y type narrowing. Implementar 2 ejercicios sin consultar soluciones."),
    ("Desarrollo - Rendimiento Angular", "Revisar change detection, OnPush, signals, @for, lazy loading y memoizacion. Aplicar 2 mejoras a un ejemplo."),
    ("Desarrollo - Accesibilidad", "Auditar teclado, foco, labels, roles, contraste y mensajes de error. Corregir los problemas encontrados."),
]

def esc(s):
    return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')

def event(uid, title, day, sh, sm, eh, em, desc, location=None):
    lines = ["BEGIN:VEVENT", f"UID:{uid}@luispa-calendar", "DTSTAMP:20260817T194000Z", f"DTSTART;TZID=Europe/Madrid:{day:%Y%m%d}T{sh:02d}{sm:02d}00", f"DTEND;TZID=Europe/Madrid:{day:%Y%m%d}T{eh:02d}{em:02d}00", f"SUMMARY:{esc(title)}", f"DESCRIPTION:{esc(desc)}"]
    if location:
        lines.append(f"LOCATION:{esc(location)}")
    lines.append("END:VEVENT")
    return lines

lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//OpenAI//Luispa Plan 2026//ES", "CALSCALE:GREGORIAN", "METHOD:PUBLISH", "X-WR-CALNAME:Luispa - Entrenamiento y Desarrollo"]
d = START
post_index = 0
while d <= END:
    # Training: Monday/Thursday CrossFit; Tuesday evening strength; Friday 07:00 strength.
    if d.weekday() in (0, 3):
        lines += event(uuid.uuid4(), "CrossFit", d, 18, 0, 19, 15, "Sesion de CrossFit. Prioridad: tecnica, intensidad controlada y buena ejecucion.")
    if d.weekday() == 1:
        lines += event(uuid.uuid4(), "Fuerza - Gimnasio", d, 18, 0, 18, 40, "Sesion de fuerza de 40 min. Registrar cargas y repeticiones. Mantener tecnica.")
    if d.weekday() == 4:
        lines += event(uuid.uuid4(), "Fuerza - Gimnasio", d, 7, 0, 7, 40, "Sesion de fuerza de 40 min. Registrar cargas y repeticiones.")

    # Study: Tue/Wed/Fri 21:00, Sun 20:00. 5 hours/week.
    if d.weekday() in (1, 2, 4, 6):
        if d in PREP:
            title, desc = PREP[d]
        elif d > date(2026, 9, 2):
            title, desc = POST[post_index % len(POST)]
            post_index += 1
        else:
            title, desc = ("Entrevista - Repaso", "Repasar LitElement, Web Components, JavaScript/TypeScript y experiencia profesional. Priorizar practica y respuestas en voz alta.")
        hour = 20 if d.weekday() == 6 else 21
        lines += event(uuid.uuid4(), title, d, hour, 0, hour + 1, 15, desc + " Duracion: 75 min. Empezar directamente con la tarea.")
    d += timedelta(days=1)

lines += event("kisters-interview", "Entrevista - KISTERS AG", date(2026, 9, 2), 10, 0, 11, 0, "Entrevista inicial. Repaso recomendado: LitElement, Web Components, Angular, TypeScript y experiencia profesional.", "Virtual")
lines.append("END:VCALENDAR")
OUT.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")
