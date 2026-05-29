"""
Servicio de IA desacoplado para el módulo de notas.
Abstrae el proveedor de IA — se puede cambiar a IA local o cualquier otro API
sin modificar las vistas ni los modelos.
"""
import os
from dataclasses import dataclass
from enum import Enum


class AIAction(str, Enum):
    SUMMARIZE = 'summarize'
    IMPROVE = 'improve'
    REPORT = 'report'
    TASKS = 'tasks'
    KEY_POINTS = 'key_points'
    MEETING = 'meeting'


@dataclass
class AIResult:
    action: str
    original: str
    processed: str
    tokens_used: int = 0
    provider: str = 'claude'


PROMPTS = {
    AIAction.SUMMARIZE: (
        "Eres un asistente empresarial profesional. "
        "Resume el siguiente texto de forma concisa y clara, manteniendo los puntos más importantes. "
        "Usa lenguaje formal y profesional. Responde solo con el resumen, sin explicaciones adicionales."
    ),
    AIAction.IMPROVE: (
        "Eres un redactor empresarial experto. "
        "Mejora la redacción del siguiente texto: corrige errores, mejora la gramática y el estilo, "
        "hazlo más claro y profesional. Conserva el significado original. "
        "Responde solo con el texto mejorado."
    ),
    AIAction.REPORT: (
        "Eres un analista empresarial. Convierte las siguientes notas o apuntes en un informe "
        "profesional bien estructurado en español. "
        "El informe debe incluir: título, resumen ejecutivo, hallazgos principales, "
        "conclusiones y acciones recomendadas (si aplica). "
        "Usa formato Markdown con encabezados claros."
    ),
    AIAction.TASKS: (
        "Eres un asistente de productividad empresarial. "
        "Analiza el siguiente texto y extrae todas las tareas, pendientes y acciones concretas. "
        "Presenta el resultado como una lista de tareas en formato Markdown, "
        "organizada por prioridad si es posible. "
        "Responde solo con la lista de tareas."
    ),
    AIAction.KEY_POINTS: (
        "Eres un analista empresarial. Identifica y lista los puntos clave del siguiente texto. "
        "Usa viñetas en formato Markdown. Sé conciso y preciso. "
        "Responde solo con los puntos clave."
    ),
    AIAction.MEETING: (
        "Eres un secretario ejecutivo profesional. Convierte las siguientes notas de reunión "
        "en un acta de reunión formal y estructurada en español. "
        "Incluye: fecha (si se menciona), asistentes (si se mencionan), temas tratados, "
        "decisiones tomadas, compromisos y próximos pasos. "
        "Usa formato Markdown profesional."
    ),
}


def process_with_ai(content: str, action: AIAction, title: str = '') -> AIResult:
    """
    Punto de entrada principal. Llama al proveedor configurado.
    Para cambiar de proveedor, modificar solo esta función.
    """
    provider = os.getenv('AI_PROVIDER', 'claude')

    if provider == 'claude':
        return _process_with_claude(content, action, title)
    # Aquí se agregarían otros proveedores:
    # elif provider == 'openai': return _process_with_openai(...)
    # elif provider == 'local': return _process_with_local(...)
    raise ValueError(f"Proveedor de IA no soportado: {provider}")


def _process_with_claude(content: str, action: AIAction, title: str = '') -> AIResult:
    import anthropic

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY no está configurada en el archivo .env")

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = PROMPTS.get(action, PROMPTS[AIAction.IMPROVE])
    user_message = f"Título: {title}\n\n{content}" if title else content

    message = client.messages.create(
        model=os.getenv('AI_MODEL', 'claude-haiku-4-5-20251001'),
        max_tokens=2048,
        messages=[{'role': 'user', 'content': user_message}],
        system=system_prompt,
    )

    processed_text = message.content[0].text
    tokens = message.usage.input_tokens + message.usage.output_tokens

    return AIResult(
        action=action.value,
        original=content,
        processed=processed_text,
        tokens_used=tokens,
        provider='claude',
    )
