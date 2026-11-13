"""
PDF Generation Engine for Student Academic Performance Reports in EduTrack AI.
Generates compliant PDF documents without external dependencies.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Union


def escape_pdf_text(text: str) -> str:
    """Escape parenthesis and backslashes for PDF string literals, encoding to Latin-1/ASCII."""
    if text is None:
        return ""
    # Map common accented characters to clean ASCII representations for broad viewer compatibility
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C', 'Ñ': 'N',
    }
    cleaned = "".join(replacements.get(char, char) for char in str(text))
    escaped = cleaned.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return escaped


class PDFDocument:
    """Lightweight, self-contained PDF generator for academic performance reports."""

    def __init__(self, width: float = 595.28, height: float = 841.89):
        # Default A4 page dimensions
        self.width = width
        self.height = height
        self.commands: List[str] = []

    def set_fill_color(self, r: float, g: float, b: float):
        """Set fill color (RGB 0.0 - 1.0)."""
        self.commands.append(f"{r:.3f} {g:.3f} {b:.3f} rg")

    def set_stroke_color(self, r: float, g: float, b: float):
        """Set stroke color (RGB 0.0 - 1.0)."""
        self.commands.append(f"{r:.3f} {g:.3f} {b:.3f} RG")

    def draw_rect(self, x: float, y: float, w: float, h: float, fill: bool = True, stroke: bool = False):
        """Draw a rectangle."""
        self.commands.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re")
        if fill and stroke:
            self.commands.append("B")
        elif fill:
            self.commands.append("f")
        elif stroke:
            self.commands.append("S")

    def draw_line(self, x1: float, y1: float, x2: float, y2: float, line_width: float = 1.0):
        """Draw a line between two points."""
        self.commands.append(f"{line_width:.2f} w")
        self.commands.append(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S")

    def draw_text(self, text: str, x: float, y: float, font: str = "/F1", size: float = 10.0):
        """Draw a single-line text string at coordinates (x, y)."""
        escaped = escape_pdf_text(text)
        self.commands.append("BT")
        self.commands.append(f"{font} {size:.2f} Tf")
        self.commands.append(f"{x:.2f} {y:.2f} Td")
        self.commands.append(f"({escaped}) Tj")
        self.commands.append("ET")

    def build(self) -> bytes:
        """Compile PDF commands into binary PDF-1.4 bytes."""
        stream_content = "\n".join(self.commands).encode("latin-1", "replace")
        stream_len = len(stream_content)

        objects: List[bytes] = []

        # Object 1: Catalog
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        # Object 2: Pages container
        objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
        # Object 3: Single Page
        page_dict = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {self.width:.2f} {self.height:.2f}] "
            f"/Contents 4 0 R /Resources << /Font << "
            f"/F1 5 0 R /F2 6 0 R >> >> >>"
        ).encode("ascii")
        objects.append(page_dict)
        # Object 4: Page Content Stream
        content_obj = (
            f"<< /Length {stream_len} >>\nstream\n".encode("ascii")
            + stream_content
            + b"\nendstream"
        )
        objects.append(content_obj)
        # Object 5: Standard Font (Helvetica)
        objects.append(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>"
        )
        # Object 6: Bold Font (Helvetica-Bold)
        objects.append(
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"
        )

        # Assemble PDF file structure
        header = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        body = bytearray(header)
        xref_offsets: List[int] = [0]

        for i, obj in enumerate(objects, start=1):
            offset = len(body)
            xref_offsets.append(offset)
            body.extend(f"{i} 0 obj\n".encode("ascii"))
            body.extend(obj)
            body.extend(b"\nendobj\n")

        xref_pos = len(body)
        total_objs = len(objects) + 1
        xref = f"xref\n0 {total_objs}\n0000000000 65535 f \n".encode("ascii")
        for offset in xref_offsets[1:]:
            xref += f"{offset:010d} 00000 n \n".encode("ascii")

        body.extend(xref)
        trailer = (
            f"trailer\n<< /Size {total_objs} /Root 1 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        ).encode("ascii")
        body.extend(trailer)

        return bytes(body)


def build_performance_report_pdf(
    student_name: str,
    student_email: str,
    subjects: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
    output_path: Optional[Union[str, Path]] = None,
) -> bytes:
    """
    Build a styled academic performance report PDF document.

    Args:
        student_name: Full name of the student.
        student_email: Student contact email.
        subjects: List of subject dictionaries (id, name, teacher, hours).
        tasks: List of task dictionaries (id, title, status, subject_id).
        output_path: Optional file path where the PDF should be saved.

    Returns:
        Generated PDF bytes.
    """
    pdf = PDFDocument()

    # 1. Header Banner
    pdf.set_fill_color(0.12, 0.23, 0.54)  # Deep Navy #1E3A8A
    pdf.draw_rect(40, 770, 515, 45, fill=True, stroke=False)

    pdf.set_fill_color(1.0, 1.0, 1.0)  # White text
    pdf.draw_text("EduTrack AI - Gestao Academica", 55, 795, font="/F2", size=15)
    pdf.draw_text("Relatorio Oficial de Desempenho do Estudante", 55, 778, font="/F1", size=10)

    # 2. Student Info Card
    pdf.set_fill_color(0.94, 0.96, 0.98)  # Slate light #F1F5F9
    pdf.set_stroke_color(0.85, 0.88, 0.92)
    pdf.draw_rect(40, 680, 515, 75, fill=True, stroke=True)

    pdf.set_fill_color(0.06, 0.09, 0.16)
    pdf.draw_text("Identificacao do Aluno", 55, 735, font="/F2", size=11)

    pdf.draw_text(f"Nome: {student_name or 'Nao informado'}", 55, 715, font="/F1", size=10)
    pdf.draw_text(f"E-mail: {student_email or 'Nao informado'}", 55, 695, font="/F1", size=10)

    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.draw_text(f"Data de Emissao: {now_str}", 330, 715, font="/F1", size=10)
    pdf.draw_text(f"Disciplinas Cursadas: {len(subjects)}", 330, 695, font="/F1", size=10)

    # Calculate Global Progress Metrics
    completed_statuses = {"completed", "concluida", "concluída", "done"}
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for t in tasks
        if str(t.get("status", "")).strip().lower() in completed_statuses
    )
    pending_tasks = total_tasks - completed_tasks
    global_progress = (completed_tasks / total_tasks * 100.0) if total_tasks > 0 else 0.0

    # 3. Overall Performance Summary Card
    pdf.set_fill_color(0.95, 0.97, 1.0)
    pdf.set_stroke_color(0.75, 0.82, 0.95)
    pdf.draw_rect(40, 585, 515, 80, fill=True, stroke=True)

    pdf.set_fill_color(0.12, 0.23, 0.54)
    pdf.draw_text("Resumo Geral de Rendimento", 55, 645, font="/F2", size=11)

    pdf.set_fill_color(0.15, 0.18, 0.25)
    pdf.draw_text(f"Total de Tarefas: {total_tasks}", 55, 625, font="/F1", size=10)
    pdf.draw_text(f"Tarefas Concluidas: {completed_tasks}", 180, 625, font="/F1", size=10)
    pdf.draw_text(f"Tarefas Pendentes: {pending_tasks}", 320, 625, font="/F1", size=10)

    pdf.set_fill_color(0.08, 0.45, 0.25)  # Dark green for completion
    pdf.draw_text(f"Progresso Global: {global_progress:.1f}%", 440, 625, font="/F2", size=10)

    # Progress bar container
    pdf.set_fill_color(0.85, 0.88, 0.92)
    pdf.draw_rect(55, 600, 485, 12, fill=True, stroke=False)
    # Filled progress bar
    if global_progress > 0:
        bar_width = (global_progress / 100.0) * 485.0
        pdf.set_fill_color(0.23, 0.51, 0.96)  # Blue bar
        pdf.draw_rect(55, 600, bar_width, 12, fill=True, stroke=False)

    # 4. Subjects & Tasks Detailed Table
    pdf.set_fill_color(0.06, 0.09, 0.16)
    pdf.draw_text("Detalhamento por Disciplina", 40, 555, font="/F2", size=12)

    # Table Header
    y_pos = 530
    pdf.set_fill_color(0.12, 0.23, 0.54)
    pdf.draw_rect(40, y_pos, 515, 20, fill=True, stroke=False)

    pdf.set_fill_color(1.0, 1.0, 1.0)
    pdf.draw_text("Disciplina", 50, y_pos + 6, font="/F2", size=9)
    pdf.draw_text("Professor", 220, y_pos + 6, font="/F2", size=9)
    pdf.draw_text("Horas", 350, y_pos + 6, font="/F2", size=9)
    pdf.draw_text("Tarefas", 410, y_pos + 6, font="/F2", size=9)
    pdf.draw_text("Progresso", 480, y_pos + 6, font="/F2", size=9)

    y_pos -= 22

    if not subjects:
        pdf.set_fill_color(0.5, 0.5, 0.5)
        pdf.draw_text("Nenhuma disciplina cadastrada ate o momento.", 50, y_pos + 4, font="/F1", size=9)
        y_pos -= 20
    else:
        for idx, subj in enumerate(subjects):
            subj_id = subj.get("id")
            subj_name = str(subj.get("name", "Sem Nome"))
            teacher = str(subj.get("teacher", "Nao informado"))
            hours = str(subj.get("hours", "-"))

            # Calculate metrics for this specific subject
            subj_tasks = [t for t in tasks if t.get("subject_id") == subj_id]
            subj_total = len(subj_tasks)
            subj_completed = sum(
                1 for t in subj_tasks
                if str(t.get("status", "")).strip().lower() in completed_statuses
            )
            subj_pct = (subj_completed / subj_total * 100.0) if subj_total > 0 else 0.0

            # Alternate row background
            if idx % 2 == 0:
                pdf.set_fill_color(0.97, 0.98, 0.99)
                pdf.draw_rect(40, y_pos, 515, 20, fill=True, stroke=False)

            pdf.set_fill_color(0.15, 0.18, 0.25)
            pdf.draw_text(subj_name[:30], 50, y_pos + 5, font="/F2", size=9)
            pdf.draw_text(teacher[:22], 220, y_pos + 5, font="/F1", size=9)
            pdf.draw_text(f"{hours}h", 350, y_pos + 5, font="/F1", size=9)
            pdf.draw_text(f"{subj_completed}/{subj_total}", 415, y_pos + 5, font="/F1", size=9)

            if subj_pct == 100.0:
                pdf.set_fill_color(0.08, 0.45, 0.25)  # Green for 100%
            elif subj_pct >= 50.0:
                pdf.set_fill_color(0.15, 0.35, 0.75)  # Blue
            else:
                pdf.set_fill_color(0.75, 0.35, 0.1)  # Amber

            pdf.draw_text(f"{subj_pct:.1f}%", 485, y_pos + 5, font="/F2", size=9)

            pdf.set_stroke_color(0.9, 0.92, 0.94)
            pdf.draw_line(40, y_pos, 555, y_pos, line_width=0.5)

            y_pos -= 20
            if y_pos < 90:
                break  # Fits within single page budget

    # 5. Footer
    pdf.set_stroke_color(0.8, 0.85, 0.9)
    pdf.draw_line(40, 60, 555, 60, line_width=0.75)

    pdf.set_fill_color(0.4, 0.45, 0.5)
    pdf.draw_text(
        "EduTrack AI - Sistema de Gestao Academica Inteligente. Documento emitido para fins de acompanhamento escolar.",
        45, 45, font="/F1", size=8
    )

    pdf_bytes = pdf.build()

    if output_path:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes


def main():
    """Command-line interface for testing and generating reports."""
    parser = argparse.ArgumentParser(description="Generate student performance report PDF.")
    parser.add_argument("--output", type=str, default="relatorio_desempenho.pdf", help="Output PDF file path")
    parser.add_argument("--name", type=str, default="Estudante EduTrack", help="Student name")
    parser.add_argument("--email", type=str, default="estudante@edutrack.ai", help="Student email")
    parser.add_argument("--data-file", type=str, default=None, help="Optional JSON file with subjects and tasks")

    args = parser.parse_args()

    subjects = [
        {"id": 1, "name": "Matematica Discreta", "teacher": "Prof. Roberto", "hours": 60},
        {"id": 2, "name": "Estruturas de Dados", "teacher": "Prof. Ana Silva", "hours": 80},
        {"id": 3, "name": "Banco de Dados I", "teacher": "Prof. Carlos", "hours": 60},
    ]
    tasks = [
        {"id": 101, "subject_id": 1, "status": "completed", "title": "Lista 1"},
        {"id": 102, "subject_id": 1, "status": "completed", "title": "Prova Parcial"},
        {"id": 103, "subject_id": 2, "status": "completed", "title": "Trabalho Arvores"},
        {"id": 104, "subject_id": 2, "status": "pending", "title": "Implementacao Grafos"},
        {"id": 105, "subject_id": 3, "status": "completed", "title": "Modelagem ER"},
    ]

    if args.data_file and os.path.exists(args.data_file):
        with open(args.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            subjects = data.get("subjects", subjects)
            tasks = data.get("tasks", tasks)

    build_performance_report_pdf(
        student_name=args.name,
        student_email=args.email,
        subjects=subjects,
        tasks=tasks,
        output_path=args.output,
    )
    print(f"Relatorio PDF gerado com sucesso em: {args.output}")


if __name__ == "__main__":
    main()
