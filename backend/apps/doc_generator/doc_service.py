"""
Servicio de generación de documentos.
Detecta variables, reemplaza contenido y genera DOCX/ZIP.
"""
import re
import io
import zipfile
from pathlib import Path
from docx import Document
from docx.shared import Pt


VARIABLE_PATTERN = re.compile(r'\{\{(\s*[\w\s]+\s*)\}\}')


def extract_variables(docx_path: str) -> list[str]:
    """Extrae todas las variables {{variable}} únicas del documento."""
    doc = Document(docx_path)
    found = set()

    for paragraph in doc.paragraphs:
        for match in VARIABLE_PATTERN.finditer(paragraph.text):
            found.add(match.group(1).strip())

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for match in VARIABLE_PATTERN.finditer(cell.text):
                    found.add(match.group(1).strip())

    return sorted(found)


def _replace_in_paragraph(paragraph, replacements: dict):
    """Reemplaza variables en un párrafo preservando el formato del run."""
    full_text = paragraph.text
    if not any(f'{{{{{k}}}}}' in full_text for k in replacements):
        return

    for run in paragraph.runs:
        for key, value in replacements.items():
            placeholder = f'{{{{{key}}}}}'
            if placeholder in run.text:
                run.text = run.text.replace(placeholder, str(value))


def generate_document(template_path: str, data: dict) -> bytes:
    """Genera un único documento DOCX reemplazando las variables con data."""
    doc = Document(template_path)

    for paragraph in doc.paragraphs:
        _replace_in_paragraph(paragraph, data)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    _replace_in_paragraph(paragraph, data)

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def generate_bulk(template_path: str, records: list[dict], name_field: str = None) -> tuple[bytes, int, int]:
    """
    Genera documentos en masa y los empaqueta en un ZIP.
    Retorna: (zip_bytes, total, procesados)
    """
    zip_buffer = io.BytesIO()
    processed = 0
    errors = 0

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for i, record in enumerate(records):
            try:
                docx_bytes = generate_document(template_path, record)
                filename = f'documento_{i + 1:03d}'
                if name_field and name_field in record:
                    safe_name = re.sub(r'[^\w\s-]', '', str(record[name_field]))[:40].strip()
                    filename = safe_name or filename
                zf.writestr(f'{filename}.docx', docx_bytes)
                processed += 1
            except Exception:
                errors += 1

    return zip_buffer.getvalue(), processed, errors


SAMPLE_TEMPLATES: dict[str, dict] = {
    'certificado_laboral': {
        'name': 'Certificado Laboral',
        'paragraphs': [
            ('CERTIFICADO LABORAL', True, 16),
            ('', False, 11),
            ('Bogotá D.C., {{fecha}}', False, 11),
            ('', False, 11),
            ('A quien pueda interesar:', False, 11),
            ('', False, 11),
            ('La empresa {{empresa}}, con NIT {{nit}}, certifica que {{nombre}}, identificado(a) con cédula de ciudadanía número {{cedula}}, labora con nosotros en el cargo de {{cargo}} desde el {{fecha_inicio}} hasta la actualidad.', False, 11),
            ('', False, 11),
            ('Durante su vinculación ha desempeñado sus funciones con responsabilidad y compromiso. Su salario mensual es de {{salario}}.', False, 11),
            ('', False, 11),
            ('Este certificado se expide a solicitud del interesado.', False, 11),
            ('', False, 11),
            ('Atentamente,', False, 11),
            ('', False, 11),
            ('', False, 11),
            ('{{firmante}}', False, 11),
            ('{{cargo_firmante}}', False, 11),
            ('{{empresa}}', False, 11),
        ],
    },
    'carta_presentacion': {
        'name': 'Carta de Presentación',
        'paragraphs': [
            ('CARTA DE PRESENTACIÓN', True, 16),
            ('', False, 11),
            ('{{ciudad}}, {{fecha}}', False, 11),
            ('', False, 11),
            ('Señores', False, 11),
            ('{{empresa_destino}}', False, 11),
            ('Ciudad', False, 11),
            ('', False, 11),
            ('Respetados señores:', False, 11),
            ('', False, 11),
            ('Por medio de la presente, nos permitimos presentar a {{nombre}}, portador(a) de la cédula de ciudadanía {{cedula}}, quien se ha desempeñado en nuestra empresa como {{cargo}} durante {{tiempo}}.', False, 11),
            ('', False, 11),
            ('{{descripcion}}', False, 11),
            ('', False, 11),
            ('Agradecemos la atención prestada a la presente.', False, 11),
            ('', False, 11),
            ('Cordialmente,', False, 11),
            ('', False, 11),
            ('', False, 11),
            ('{{firmante}}', False, 11),
            ('{{cargo_firmante}}', False, 11),
        ],
    },
    'paz_y_salvo': {
        'name': 'Paz y Salvo',
        'paragraphs': [
            ('PAZ Y SALVO', True, 16),
            ('', False, 11),
            ('{{ciudad}}, {{fecha}}', False, 11),
            ('', False, 11),
            ('La empresa {{empresa}} certifica que {{nombre}}, identificado(a) con cédula {{cedula}}, se encuentra a paz y salvo por concepto de {{concepto}}.', False, 11),
            ('', False, 11),
            ('Este documento se expide a solicitud del interesado para los fines que considere pertinentes.', False, 11),
            ('', False, 11),
            ('Observaciones: {{observaciones}}', False, 11),
            ('', False, 11),
            ('', False, 11),
            ('{{firmante}}', False, 11),
            ('{{cargo_firmante}}', False, 11),
            ('{{empresa}}', False, 11),
            ('Fecha de expedición: {{fecha}}', False, 11),
        ],
    },
    'constancia_ingresos': {
        'name': 'Constancia de Ingresos',
        'paragraphs': [
            ('CONSTANCIA DE INGRESOS', True, 16),
            ('', False, 11),
            ('{{ciudad}}, {{fecha}}', False, 11),
            ('', False, 11),
            ('A quien pueda interesar:', False, 11),
            ('', False, 11),
            ('La empresa {{empresa}} hace constar que {{nombre}}, con cédula {{cedula}}, cargo {{cargo}}, devenga un salario mensual de {{salario}} en modalidad {{modalidad}}.', False, 11),
            ('', False, 11),
            ('Tipo de contrato: {{tipo_contrato}}', False, 11),
            ('Fecha de inicio: {{fecha_inicio}}', False, 11),
            ('', False, 11),
            ('Esta constancia se expide a petición del interesado.', False, 11),
            ('', False, 11),
            ('', False, 11),
            ('{{firmante}}', False, 11),
            ('{{cargo_firmante}}', False, 11),
        ],
    },
    'invitacion_reunion': {
        'name': 'Invitación a Reunión',
        'paragraphs': [
            ('INVITACIÓN A REUNIÓN', True, 16),
            ('', False, 11),
            ('{{ciudad}}, {{fecha}}', False, 11),
            ('', False, 11),
            ('Estimado(a) {{nombre}}:', False, 11),
            ('', False, 11),
            ('Por medio de la presente, nos permitimos invitarlo(a) a la reunión que se llevará a cabo el día {{fecha_reunion}} a las {{hora}} en {{lugar}}.', False, 11),
            ('', False, 11),
            ('Tema a tratar: {{tema}}', False, 11),
            ('', False, 11),
            ('Agenda:', False, 11),
            ('1. {{punto_1}}', False, 11),
            ('2. {{punto_2}}', False, 11),
            ('3. {{punto_3}}', False, 11),
            ('', False, 11),
            ('Agradecemos su puntual asistencia.', False, 11),
            ('', False, 11),
            ('Cordialmente,', False, 11),
            ('', False, 11),
            ('{{organizador}}', False, 11),
            ('{{cargo_organizador}}', False, 11),
        ],
    },
}


def generate_sample_template(key: str) -> bytes:
    """Genera un archivo .docx de plantilla de ejemplo para descargar."""
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    template_def = SAMPLE_TEMPLATES.get(key)
    if not template_def:
        raise ValueError(f'Plantilla desconocida: {key}')

    doc = Document()

    # Reducir márgenes
    for section in doc.sections:
        section.top_margin = Pt(50)
        section.bottom_margin = Pt(50)
        section.left_margin = Pt(70)
        section.right_margin = Pt(70)

    for text, is_title, size in template_def['paragraphs']:
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.size = Pt(size)
        if is_title:
            run.font.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def parse_excel_data(file_obj) -> list[dict]:
    """Lee un archivo Excel y retorna lista de dicts con los datos."""
    import openpyxl
    wb = openpyxl.load_workbook(file_obj, read_only=True)
    ws = wb.active

    headers = [str(cell.value).strip() for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    records = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if any(v is not None for v in row):
            records.append({headers[i]: (str(v) if v is not None else '') for i, v in enumerate(row)})
    return records
