from datetime import date, datetime, timedelta
from pathlib import Path
import hashlib

# ============================================================
# Luispa — calendario único de entrenamiento + desarrollo
# Fuente única: este script.
#
# Genera calendario.ics.
# Hay un único calendario fuente: calendario.ics.
# No edites los .ics a mano: regenera este archivo con este script.
# ============================================================

START = date(2026, 8, 24)
END = date(2026, 11, 30)

OUT = Path("calendario.ics")

# Recursos oficiales. Se añaden dentro de las notas de los eventos.
RESOURCES = {
    "lit": [
        "https://lit.dev/docs/getting-started/",
        "https://lit.dev/docs/components/properties/",
        "https://lit.dev/docs/components/lifecycle/",
        "https://developer.mozilla.org/en-US/docs/Web/API/Web_components",
    ],
    "web_components": [
        "https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_custom_elements",
        "https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_shadow_DOM",
        "https://developer.mozilla.org/en-US/docs/Web/API/Web_components/Using_templates_and_slots",
    ],
    "angular": [
        "https://angular.dev/guide/components",
        "https://angular.dev/guide/signals",
    ],
    "typescript": [
        "https://www.typescriptlang.org/docs/handbook/2/generics.html",
        "https://www.typescriptlang.org/docs/handbook/2/narrowing.html",
        "https://www.typescriptlang.org/docs/",
    ],
    "node": [
        "https://nodejs.org/en/learn",
        "https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop",
    ],
    "docker": [
        "https://docs.docker.com/get-started/",
    ],
}

def esc(s):
    return (
        s.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )

def resources(keys):
    urls = []
    for key in keys:
        urls.extend(RESOURCES[key])
    return "\nRecursos:\n" + "\n".join(urls)

def event(uid, title, day, sh, sm, eh, em, desc, location=None):
    # UID determinista: Apple Calendar necesita que el mismo evento conserve
    # su UID entre regeneraciones para actualizarlo en vez de duplicarlo.
    stable_uid = hashlib.sha1(f"{day.isoformat()}|{title}".encode("utf-8")).hexdigest()
    lines = [
        "BEGIN:VEVENT",
        f"UID:{stable_uid}@luispa-calendar",
        "DTSTAMP:20260824T190000Z",
        f"DTSTART;TZID=Europe/Madrid:{day:%Y%m%d}T{sh:02d}{sm:02d}00",
        f"DTEND;TZID=Europe/Madrid:{day:%Y%m%d}T{eh:02d}{em:02d}00",
        f"SUMMARY:{esc(title)}",
        f"DESCRIPTION:{esc(desc)}",
    ]
    if location:
        lines.append(f"LOCATION:{esc(location)}")
    lines.append("END:VEVENT")
    return lines

def strength_event(day, title, plan):
    return event(
        None,
        title,
        day,
        20, 30, 21, 10,
        plan + """
Duración: 40 min.
Regla de adaptación: si el CrossFit cercano ha tenido mucho volumen del mismo patrón
(piernas, bisagra, hombros, espalda o agarre), reduce una serie o cambia el patrón
por una variante menos fatigante. No entrenar al fallo.
Progresión: cuando completes todas las series con técnica sólida y RPE <= 7,5,
sube 2,5-5 kg la próxima vez que aparezca el mismo patrón. Registra carga, reps y RPE.
""",
        "Gimnasio",
    )

def friday_strength(day, plan):
    return event(
        None,
        "💪 Fuerza — Viernes",
        day,
        7, 0, 7, 40,
        plan + """
Duración: 40 min.
Regla de adaptación: si el CrossFit del miércoles/jueves tuvo mucho volumen de
deadlift, clean/snatch, swings, sentadillas, lunges, hombros o agarre, cambia el
patrón coincidente por una variante menos fatigante. No entrenar al fallo.
Progresión: RPE 7 como base; sube carga solo con técnica sólida.
""",
        "Gimnasio",
    )

def optional_thursday(day, plan):
    return event(
        None,
        "💪 Fuerza — Jueves OPCIONAL",
        day,
        7, 0, 7, 35,
        plan + """
Duración: 30-35 min.
Esta sesión solo se hace si el CrossFit del miércoles fue ligero/moderado y te
encuentras recuperado. RPE 6-7. Si hay fatiga relevante de hombros, espalda, piernas
o agarre: DESCANSO. Esta tercera sesión es opcional, no obligatoria.
""",
        "Gimnasio",
    )

def study(day, title, body, resource_keys):
    # Tue/Wed/Fri: 21:00-22:15. Sunday: 20:00-21:15.
    hour = 20 if day.weekday() == 6 else 21
    return event(
        None,
        title,
        day,
        hour, 0, hour + 1, 15,
        body + """
Duración: 75 min.
Método: concepto mínimo → práctica escribiendo código → feedback/corrección →
explicación sin apuntes → registro.
Resultado obligatorio: código funcionando, ejercicio resuelto, test, feature o
explicación estructurada. No terminar una sesión solo habiendo leído teoría.
""" + resources(resource_keys),
        "Estudio",
    )

events = []

# ============================================================
# ESTUDIO — entrevista y después desarrollo profesional
# ============================================================

PREP = {
    date(2026, 8, 25): (
        "🎯 Estudio — Lit: fundamentos para entrevista",
        """10' Custom Elements y Shadow DOM. 15' Lit y modelo mental de componente.
20' @property, @state, render y templates. 25' crear un <user-card> funcional.
5' explicar Lit vs Angular. Resultado: componente funcionando + explicación de 3 min.""",
        ["lit", "web_components"],
    ),
    date(2026, 8, 26): (
        "🎯 Estudio — Web Components en profundidad",
        """15' Custom Elements. 15' Shadow DOM/encapsulación. 15' slots/composición.
15' eventos y comunicación. 15' responder 5 preguntas de entrevista en voz alta.
Resultado: diagrama de arquitectura + respuestas.""",
        ["web_components"],
    ),
    date(2026, 8, 28): (
        "🎯 Estudio — Migración Angular → Lit",
        """15' decidir qué migrar y qué no. 20' estrategia incremental y convivencia
Angular/Lit. 15' propiedades, eventos y estado. 15' testing/build. 10' riesgos,
rollback y criterios de éxito. Resultado: propuesta de migración de 1 página + defensa oral.""",
        ["lit", "web_components", "angular"],
    ),
    date(2026, 8, 30): (
        "🎯 Estudio — Simulación completa de entrevista",
        """75' sin estudiar teoría durante la sesión. Presentación, experiencia,
Angular/TypeScript/RxJS, JavaScript, Lit/Web Components, migración, arquitectura,
debugging y preguntas a la empresa. Resultado: máximo 5 lagunas priorizadas.""",
        ["lit", "angular", "typescript"],
    ),
    date(2026, 9, 1): (
        "🎯 Estudio — Repaso final entrevista",
        """20' Lit/migración. 15' Web Components. 15' Angular/TypeScript/RxJS.
15' experiencia profesional. 10' preguntas para la empresa. Nada nuevo. Resultado:
lista de respuestas clave + descanso.""",
        ["lit", "web_components", "angular", "typescript"],
    ),
    date(2026, 9, 2): (
        "🎯 Entrevista — KISTERS AG",
        """Antes de la entrevista: 20-30' máximo. Repasar presentación, experiencia,
Angular/TypeScript, Web Components, Lit y estrategia de migración. No estudiar
contenido nuevo. Después: 15' registrar preguntas, 30' reconstruir respuestas,
20' identificar lagunas, 10' elegir prioridades.""",
        ["lit", "web_components", "angular"],
    ),
}

POST = [
    ("🧠 Desarrollo — Angular avanzado",
     "10' repaso mínimo. 50' implementar una feature con standalone components y signals/RxJS. 10' code review. 5' registrar 3 decisiones técnicas.",
     ["angular"]),
    ("🧠 Desarrollo — TypeScript profundo",
     "15' generics/constraints. 20' narrowing. 25' utility/mapped/conditional types. 10' crear 3 ejemplos. 5' explicar cuándo NO complicar los tipos.",
     ["typescript"]),
    ("🧠 Desarrollo — JavaScript profundo",
     "15' event loop/closures. 35' ejercicios de promises, async/await y microtasks. 15' corregir. 10' explicar resultados sin apuntes.",
     ["typescript"]),
    ("🧠 Desarrollo — Node/AdonisJS",
     "10' diseño. 45' implementar endpoint con validación, capas, errores y persistencia. 15' test. 5' registrar decisiones.",
     ["node"]),
    ("🧠 Desarrollo — Testing",
     "10' elegir feature. 45' tests happy path + error + edge case. 15' ejecutar/corregir. 5' registrar aprendizaje.",
     ["angular"]),
    ("🧠 Desarrollo — Arquitectura",
     "15' elegir feature. 30' diseñar UI→dominio→API→BD. 20' comparar dos alternativas y trade-offs. 10' escribir ADR corto.",
     ["angular", "node"]),
    ("🧠 Desarrollo — Lit/Web Components",
     "15' repaso. 45' construir un componente Lit reutilizable con properties, state, CustomEvent y slot. 10' compararlo con Angular. 5' registrar.",
     ["lit", "web_components"]),
    ("🧠 Desarrollo — Contexto IT",
     """75' estudiar un tema: CI/CD, Docker, cloud, observabilidad, seguridad, cachés,
colas o arquitectura distribuida. Resultado: mapa conceptual + 5 preguntas.""",
     ["docker", "node"]),
    ("🧠 Desarrollo — Gym Tracker Pro",
     "10' elegir una pieza vertical. 50' UI + lógica + datos/API. 10' pruebas. 5' commit/documentación. Resultado: feature funcionando.",
     ["angular", "node"]),
    ("🧠 Desarrollo — Code review",
     "15' revisar naming/duplicación. 20' tipos y errores. 20' arquitectura. 15' tests. 5' refactor final. Resultado: diff antes/después.",
     ["typescript", "angular"]),
    ("🧠 Desarrollo — Entrevista técnica",
     "20' cinco preguntas JS/TS. 25' dos ejercicios de código. 20' explicación oral. 10' registrar fallos.",
     ["typescript", "angular"]),
    ("🧠 Desarrollo — IA aplicada al desarrollo",
     """20' investigar usos útiles de LLMs en código/tests/documentación. 30' probar un flujo
con verificación. 15' identificar riesgos. 10' crear checklist personal.""",
     ["typescript"]),
]

post_index = 0
d = START
while d <= END:
    # ---- CrossFit ----
    # Exception: current week only Thursday 27/08 at 17:00.
    if d == date(2026, 8, 27):
        events.append(event(
            None, "🏋️ CrossFit", d, 17, 0, 18, 15,
            """Sesión excepcional de esta semana: jueves 17:00.
Al terminar registra WOD, movimientos, cargas, tiempo y limitante principal.
No hace falta modificar el calendario por el WOD.""", "CrossFit"
        ))
    elif d >= date(2026, 8, 31) and d.weekday() in (0, 2):
        events.append(event(
            None, "🏋️ CrossFit", d, 18, 0, 19, 15,
            """Sesión de CrossFit. Registra WOD, movimientos, cargas, tiempo y
limitante principal. Los WOD posteriores se usan aquí para adaptar la fuerza,
sin regenerar el calendario.""", "CrossFit"
        ))

    # ---- Strength ----
    if d == date(2026, 8, 25):
        events.append(event(
            None, "💪 Fuerza — Martes", d, 20, 30, 21, 10,
            """40 min. 0-5' calentamiento + aproximaciones. 5-19' prensa 3x5-6 @ RPE 7,
descanso 2'. 19-31' press banca 3x6 @ RPE 7, 90s. 31-38' remo con pecho apoyado
2x8-10 @ RPE 7. 38-40' dead bug. Si el WOD previo cargó mucho las piernas,
prensa 2x8 @ RPE 6-7.""", "Gimnasio"
        ))
    elif d >= date(2026, 9, 1) and d.weekday() == 1:
        week = (d - date(2026, 9, 1)).days // 7
        if week % 2 == 0:
            plan = """40 min. 0-5' calentamiento + aproximaciones. 5-19' sentadilla/prensa
3x5-6 @ RPE 7-7,5, 2'. 19-31' banca 3x5-6 @ RPE 7-7,5, 90s.
31-38' remo apoyado 2x8-10 + brazos 2x10. 38-40' core."""
        else:
            plan = """40 min. 0-5' calentamiento + aproximaciones. 5-19' peso muerto/RDL
3x4-6 @ RPE 7, 2'. 19-31' press inclinado/militar 3x6-8 @ RPE 7, 90s.
31-38' jalón/remo 2x8-10 + brazos 2x10. 38-40' core."""
        events.append(strength_event(d, "💪 Fuerza — Martes", plan)
        )

    if d >= date(2026, 9, 3) and d.weekday() == 3:
        events.append(optional_thursday(
            d,
            """30-35'. Press máquina 3x8 + remo con pecho apoyado 3x8 +
brazos 2x10 + core. Todo @ RPE 6-7."""
        ))

    if d == date(2026, 8, 28):
        events.append(friday_strength(
            d,
            """40 min. 0-5' calentamiento. 5-19' RDL 3x6 @ RPE 7, 2'.
19-31' press inclinado con mancuernas 3x8 @ RPE 7, 90s.
31-38' jalón/remo 2x8-10 + curl 2x10. 38-40' plancha."""
        ))
    elif d >= date(2026, 9, 4) and d.weekday() == 4:
        plan = """40 min. 0-5' calentamiento. 5-19' bisagra o pierna 3x5-6 @ RPE 7, 2'.
19-31' empuje principal 3x6-8 @ RPE 7, 90s. 31-38' tirón + brazos 2x10.
38-40' core."""
        events.append(friday_strength(d, plan)
        )

    # ---- Bike Sunday ----
    if d.weekday() == 6:
        events.append(event(
            None, "🚴 Bici", d, 10, 0, 11, 30,
            """60-120' preferentemente Z2/ritmo conversacional. Salida libre.
Registrar duración, distancia, desnivel y sensaciones. Si la semana está cargada,
60' es suficiente.""", "Bici"
        ))

    # ---- Study ----
    if d.weekday() in (1, 2, 4, 6):
        if d in PREP:
            title, desc, rkeys = PREP[d]
        elif d > date(2026, 9, 2):
            title, desc, rkeys = POST[post_index % len(POST)]
            post_index += 1
        else:
            title, desc, rkeys = (
                "🎯 Estudio — Entrevista",
                "Repasar Lit, Web Components, JavaScript/TypeScript y experiencia profesional. Priorizar práctica y respuestas en voz alta.",
                ["lit", "web_components", "typescript"],
            )

        hour = 20 if d.weekday() == 6 else 21
        events.append(study(d, title, desc, rkeys)
        )

    d += timedelta(days=1)

# Sort chronologically.
def event_start(e):
    m = next(x for x in e if x.startswith("DTSTART;TZID=Europe/Madrid:"))
    return m.split(":", 1)[1]

# events is a list of line lists; DTSTART has YYYYMMDDTHHMMSS and sorts lexically.
events.sort(key=event_start)

header = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Luispa//Plan definitivo 2026//ES",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Luispa - Entrenamiento y Desarrollo",
    "X-WR-TIMEZONE:Europe/Madrid",
]

content = "\r\n".join(header + [line for e in events for line in e] + ["END:VCALENDAR"]) + "\r\n"

OUT.write_text(content, encoding="utf-8")
print(f"Generado {OUT}")
print(f"Eventos: {len(events)}")
