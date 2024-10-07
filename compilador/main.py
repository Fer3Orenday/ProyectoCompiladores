from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtGui import (
    QTextCharFormat,
    QColor,
    QTextCursor,
    QStandardItemModel,
    QStandardItem,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFileDialog,
    QTextEdit,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
    QTreeView,
    QHeaderView,
    QPlainTextEdit,
)
from PyQt5.uic import loadUi
import sys
import os

from lexer import lexer

from seman import (
    parser,
    set_error_output,
    get_sintactic_errors,
    get_symbol_info,
    get_symbol_type,
    symbol_table,
)

from sint import parser2, set_error_output, get_sintactic_errors


class NoScrollTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(NoScrollTextEdit, self).__init__(parent)

    def wheelEvent(self, event):
        pass


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)

        self.line_numbers = []

        self.current_path = None
        self.current_fontSize = 10
        self.setWindowTitle("Compilador")
        self.showMaximized()

        # #self.actionNuevo_archivo.triggered.connect(self.newFile)
        # #self.actionGuardar.triggered.connect(self.saveFile)
        # self.guardarbutton.clicked.connect(self.saveFile)

        # #self.actionGuardar_como.triggered.connect(self.saveFileAs)
        # self.guardarcbutton.clicked.connect(self.saveFileAs)

        # self.actionAbrir_archivo.triggered.connect(self.openFile)
        # self.actionCerrar_archivo.triggered.connect(self.closeFile)
        # self.actionDeshacer.triggered.connect(self.undo)
        # self.actionRehacer.triggered.connect(self.redo)
        # self.actionCortar.triggered.connect(self.cut)
        # self.actionCopiar.triggered.connect(self.copy)
        # self.actionPegar.triggered.connect(self.paste)

        # self.actionNuevoArchivo.triggered.connect(self.newFile)
        # self.actionGuardar_2.triggered.connect(self.saveFile)
        # self.actionGuardarComo.triggered.connect(self.saveFileAs)
        # self.actionAbrirArchivo.triggered.connect(self.openFile)
        # self.actionCerrarArchivo.triggered.connect(self.closeFile)
        # self.actionDeshacer_2.triggered.connect(self.undo)
        # self.actionRehacer_2.triggered.connect(self.redo)

        # self.actionAnalisis_sintactico.triggered.connect(self.sintax_analize)
        # self.actionCompSintax.triggered.connect(self.sintax_analize)
        # tree_view = self.tabCompilacion.findChild(QWidget, "tabSintactico").findChild(QTreeView, "txtSintactico")
        # tree_view.setAlternatingRowColors(True)
        # tree_view.setStyleSheet("QTreeView { alternate-background-color: #f0f0f0; }")
        # tree_view.header().setDefaultAlignment(Qt.AlignCenter)
        # tree_view.header().setStretchLastSection(True)
        # tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # self.listNumeroLinea = NoScrollTextEdit(self.centralwidget)
        # self.listNumeroLinea.setReadOnly(True)
        # self.listNumeroLinea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.listNumeroLinea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.listNumeroLinea.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # self.listNumeroLinea.setMinimumWidth(40)
        # self.listNumeroLinea.setMaximumWidth(40)

        # self.textCodigoFuente.textChanged.connect(self.onTextChanged)
        # self.textCodigoFuente.cursorPositionChanged.connect(self.onCursorChange)

        self.txtErroresLexico = self.findChild(QPlainTextEdit, "txtErroresLexico")

        # self.actionNuevo_archivo.triggered.connect(self.newFile)

        # self.actionGuardar.triggered.connect(self.saveFile)
        self.guardarbutton.clicked.connect(self.saveFile)

        # self.actionGuardar_como.triggered.connect(self.saveFileAs)
        self.guardarcbutton.clicked.connect(self.saveFileAs)

        # self.actionAbrir_archivo.triggered.connect(self.openFile)
        self.abrirbutton.clicked.connect(self.openFile)

        self.actionCerrar_archivo.triggered.connect(self.closeFile)
        # self.actionDeshacer.triggered.connect(self.undo)
        # self.actionRehacer.triggered.connect(self.redo)
        # self.actionCortar.triggered.connect(self.cut)
        # self.actionCopiar.triggered.connect(self.copy)
        # self.actionPegar.triggered.connect(self.paste)

        # self.actionNuevoArchivo.triggered.connect(self.newFile)
        # self.actionGuardar_2.triggered.connect(self.saveFile)
        # self.actionGuardarComo.triggered.connect(self.saveFileAs)
        # self.actionAbrirArchivo.triggered.connect(self.openFile)

        # self.actionCerrarArchivo.triggered.connect(self.closeFile)
        self.cerrarbutton.clicked.connect(self.closeFile)

        # self.actionDeshacer_2.triggered.connect(self.undo)
        # self.actionRehacer_2.triggered.connect(self.redo)

        self.btnSintactico.clicked.connect(self.sintax_analize)
        self.actionAnalisis_sintactico.triggered.connect(self.sintax_analize)
        self.actionCompSintax.triggered.connect(self.sintax_analize)

        # self.listNumeroLinea_2 = NoScrollTextEdit(self.centralwidget)
        # self.listNumeroLinea_2.setReadOnly(True)
        # self.listNumeroLinea_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.listNumeroLinea_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.listNumeroLinea_2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # self.listNumeroLinea_2.setMinimumWidth(20)
        # self.listNumeroLinea_2.setMaximumWidth(20)

        self.textCodigoFuente_2.textChanged.connect(self.onTextChanged)
        self.textCodigoFuente_2.cursorPositionChanged.connect(self.onCursorChange)

        # layoutPrincipal = QVBoxLayout(self.centralwidget)

        # layoutArriba = QHBoxLayout()
        # layoutArriba.addWidget(self.listNumeroLinea)
        # layoutArriba.addWidget(self.textCodigoFuente)
        # layoutArriba.addWidget(self.tabCompilacion)

        # layoutAbajo = QHBoxLayout()
        # layoutAbajo.addWidget(self.tabErroresResultado)
        # self.tabErroresResultado.setMaximumHeight(170)

        # layoutPrincipal.addLayout(layoutArriba)
        # layoutPrincipal.addLayout(layoutAbajo)

        # self.textCodigoFuente.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        # self.textCodigoFuente.verticalScrollBar().valueChanged.connect(self.syncScrollBars)
        # self.listNumeroLinea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # self.set_default_font_size()

        # self.textCodigoFuente.textChanged.connect(self.analyzeText)

        # self.band = 0
        layoutPrincipal = QVBoxLayout(self.centralwidget)

        layoutArriba = QHBoxLayout()
        layoutArriba.addWidget(self.listNumeroLinea_2)
        layoutArriba.addWidget(self.textCodigoFuente_2)
        layoutArriba.addWidget(self.tabCompilacion)

        layoutAbajo = QHBoxLayout()
        layoutAbajo.addWidget(self.tabErroresResultado)
        self.tabErroresResultado.setMaximumHeight(170)

        layoutPrincipal.addLayout(layoutArriba)
        layoutPrincipal.addLayout(layoutAbajo)

        self.textCodigoFuente_2.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.textCodigoFuente_2.verticalScrollBar().valueChanged.connect(
            self.syncScrollBars
        )
        self.listNumeroLinea_2.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.set_default_font_size()

        self.textCodigoFuente_2.textChanged.connect(self.analyzeText)

        self.band = 0

        self.token_formats = {
            "DOUBLE": QColor(45, 132, 214),
            "INTEGER": QColor(184, 22, 87),
            "IDENTIFICADOR": QColor(141, 22, 184),
            "COMENTARIO": QColor(189, 189, 189),
            "IF": QColor(184, 22, 87),
            "THEN": QColor(184, 22, 87),
            "ELSE": QColor(184, 22, 87),
            "DO": QColor(184, 22, 87),
            "WHILE": QColor(184, 22, 87),
            "UNTIL": QColor(184, 22, 87),
            "END": QColor(184, 22, 87),
            "SWITCH": QColor(184, 22, 87),
            "CASE": QColor(184, 22, 87),
            "INT": QColor(184, 22, 87),
            "REAL": QColor(184, 22, 87),
            "MAIN": QColor(184, 22, 87),
            "CIN": QColor(184, 22, 87),
            "COUT": QColor(184, 22, 87),
            "INC": QColor(2, 179, 8),
            "DEC": QColor(2, 179, 8),
            "SUMA": QColor(227, 9, 9),
            "RESTA": QColor(227, 9, 9),
            "DIVIDE": QColor(227, 9, 9),
            "MULT": QColor(227, 9, 9),
            "MOD": QColor(227, 9, 9),
            "POT": QColor(227, 9, 9),
            "MORETHAN": QColor(2, 179, 8),
            "LESSTHAN": QColor(2, 179, 8),
            "MOREEQUALS": QColor(2, 179, 8),
            "LESSEQUALS": QColor(2, 179, 8),
            "EQUALS": QColor(2, 179, 8),
            "NOTEQUALS": QColor(2, 179, 8),
            "AND": QColor(184, 22, 87),
            "OR": QColor(184, 22, 87),
        }

    def restart_timer(self):
        self.timer.start()

    def analyzeText(self):
        text = self.textCodigoFuente.toPlainText()

        if not text:  # Si el texto está vacío, no hay nada que analizar
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).setHtml("")
            return

        try:
            if self.band == 0:
                cursor = self.textCodigoFuente.textCursor()
                self.band = 1

            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(QTextCharFormat())  # Borrar formato existente
            cursor.clearSelection()

            lexer.input(text)

            lexemes = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                lexemes.append((tok.type, tok.value, tok.lineno, tok.lexpos))
                cursor.setPosition(tok.lexpos)
                start = tok.lexpos
                end = start + len(tok.value)
                # Aplicar formato solo si el tipo de token tiene un color definido
                if tok.type in self.token_formats:
                    self.apply_format(cursor, start, end, self.token_formats[tok.type])

            # Preparar el HTML de los lexemas encontrados
            html_table = "<table style='border-collapse: collapse;' width='100%'><tr style='color: #1155d4; font-size: 15px'><th style='padding: 8px;'>Tipo</th><th style='padding: 8px;'>Valor</th><th style='padding: 8px;'>Línea</th><th style='padding: 8px;'>Posición</th></tr>"
            for lexeme in lexemes:
                html_table += f"<tr><td style='text-align: center; padding: 5px; font-weight: bold;'>{lexeme[0]}</td><td style='text-align: center; padding: 5px; font-weight: bold; color: #c4213f;'>{lexeme[1]}</td><td style='text-align: center; padding: 5px;'>{lexeme[2]}</td><td style='text-align: center; padding: 5px;'>{lexeme[3]}</td></tr>"
            html_table += "</table>"

            # Asumiendo que `txtLexico` es el QTextEdit dentro de `tabLexico`
            # y `tabLexico` es una pestaña dentro de `tabCompilacion`
            scroll_position = (
                self.tabCompilacion.findChild(QWidget, "tabLexico")
                .findChild(QTextEdit, "txtLexico")
                .verticalScrollBar()
                .value()
            )
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).setHtml(html_table)
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).verticalScrollBar().setValue(scroll_position)
            self.band = 0
        except Exception as e:
            # Capturar cualquier error y mostrar un mensaje de error
            print("ERROR: ", e)

    def print_lexical_error(self, error_message):
        # Imprime el mensaje de error en txtErroresLexico
        self.txtErroresLexico.appendPlainText(error_message)

    def restart_timer(self):
        self.timer.start()

    def analyzeText(self):
        text = self.textCodigoFuente_2.toPlainText()

        if not text:  # Si el texto está vacío, no hay nada que analizar
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).setHtml("")
            return

        try:
            if self.band == 0:
                cursor = self.textCodigoFuente_2.textCursor()
                self.band = 1

            cursor.select(QTextCursor.SelectionType.Document)
            cursor.setCharFormat(QTextCharFormat())  # Borrar formato existente
            cursor.clearSelection()

            lexer.input(text)

            lexemes = []
            while True:
                tok = lexer.token()
                if not tok:
                    break
                lexemes.append((tok.type, tok.value, tok.lineno, tok.lexpos))
                cursor.setPosition(tok.lexpos)
                start = tok.lexpos
                end = start + len(tok.value)
                # Aplicar formato solo si el tipo de token tiene un color definido
                if tok.type in self.token_formats:
                    self.apply_format(cursor, start, end, self.token_formats[tok.type])

            # Preparar el HTML de los lexemas encontrados
            html_table = "<table ><tr><th></th><th></th><th></th><th></th></tr>"
            for lexeme in lexemes:
                html_table += f"<tr><td>Tipo: {lexeme[0]} ,</td><td>Valor: {lexeme[1]} ,</td><td>Linea: {lexeme[2]},</td><td>Posiscion: {lexeme[3]}</td></tr>"
            html_table += "</table>"

            # Asumiendo que txtLexico es el QTextEdit dentro de tabLexico
            # y tabLexico es una pestaña dentro de tabCompilacion
            scroll_position = (
                self.tabCompilacion.findChild(QWidget, "tabLexico")
                .findChild(QTextEdit, "txtLexico")
                .verticalScrollBar()
                .value()
            )
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).setHtml(html_table)
            self.tabCompilacion.findChild(QWidget, "tabLexico").findChild(
                QTextEdit, "txtLexico"
            ).verticalScrollBar().setValue(scroll_position)
            self.band = 0
        except Exception as e:
            # Capturar cualquier error y mostrar un mensaje de error
            print("ERROR: ", e)

    def sintax_analize(self):
        # Limpiar el QTextEdit de errores antes de analizar
        self.txtErroresSintactico.clear()
        

        text = self.textCodigoFuente_2.toPlainText()

        # Configurar el QTextEdit para errores en el parser
        # set_error_output(self.txtErroresSintactico)

        result = parser.parse(text)
        print(result)

        sintactic_errors = get_sintactic_errors()
        self.txtErroresSintactico.appendPlainText("\n".join(sintactic_errors))

        self.show_syntax_tree(result)
        self.show_syntax_treebien(result)
        self.show_symbol_table()  # Cambiado a no pasar argumentos


    def show_syntax_tree(self, tree):
        tree_view = self.tabCompilacion.findChild(QWidget, "tabSintactico").findChild(
            QTreeView, "txtSintactico"
        )

        # Ajustar el tamaño mínimo del QTreeView
        tree_view.setMinimumWidth(400)  # Ajusta este valor según sea necesario

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Árbol Sintáctico"])

        # Si quieres construir el árbol paso a paso:
        root_item = self.add_items(tree)
        model.appendRow(root_item)

        tree_view.setModel(model)
        tree_view.expandAll()

        tree_view.header().setDefaultAlignment(
            Qt.AlignCenter
        )  # Alineación centrada de los encabezados
        tree_view.header().setStretchLastSection(
            False
        ) 
        # Si todavía no tienes scroll horizontal, puedes asegurarte de que el tree view lo permite
        tree_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # Si hay un contenedor para el QTreeView, asegúrate de que también se maneje correctamente
        tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
               
        # Extender la última sección para ocupar todo el espacio disponible
        tree_view.header().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )  # Ajustar el tamaño de las secciones según el contenido


    def show_syntax_treebien(self, tree):
        tree_view = self.tabCompilacion.findChild(QWidget, "tabsintacticobien").findChild(
            QTreeView, "txtSintacticobien"
        )
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Árbol Sintáctico'])

        root_item = self.add_items2(tree)
        model.appendRow(root_item)

        tree_view.setModel(model)
        tree_view.expandAll()

        # Formato adicional para QTreeView
        #tree_view.setAlternatingRowColors(True)  # Colores alternados en las filas
        #tree_view.setStyleSheet("QTreeView { alternate-background-color: #f0f0f0; }")  # Color de fondo alternado
        tree_view.header().setDefaultAlignment(Qt.AlignCenter)  # Alineación centrada de los encabezados
        tree_view.header().setStretchLastSection(True)  # Extender la última sección para ocupar todo el espacio disponible
        tree_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)  # Ajustar el tamaño de las secciones según el contenido

    def show_symbol_table(self):
        # Encuentra el QTreeView en la pestaña de Tabla de Símbolos
        tabla_simbolos_view = self.tabCompilacion.findChild(QWidget, "tabTablaSimbolos").findChild(
            QTreeView, "txtTablaSimbolos"
        )

        # Ajustar el tamaño mínimo del QTreeView
        tabla_simbolos_view.setMinimumWidth(400)  # Ajusta este valor según sea necesario

        # Limpia el QTreeView antes de mostrar la tabla
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Tabla de Símbolos"])

        # Comienza a construir la salida
        for symbol in symbol_table:
            valor_str = symbol["valor"] if symbol["valor"] is not None else "Sin asignar"
            lineas_str = (
                ", ".join(map(str, symbol["lineas"])) if symbol["lineas"] else "None"
            )

            # Crear un nuevo item para cada símbolo
            item = QStandardItem(f"Nombre: {symbol['name']}, Tipo: {symbol['tipo']}, Valor: {valor_str}, Lineas: {lineas_str}")
            model.appendRow(item)

        # Asigna el modelo al QTreeView
        tabla_simbolos_view.setModel(model)
        tabla_simbolos_view.expandAll()

        # Formato adicional para QTreeView
        tabla_simbolos_view.header().setDefaultAlignment(Qt.AlignCenter)  # Alineación centrada de los encabezados
        tabla_simbolos_view.header().setStretchLastSection(False)  # No extender la última sección
        tabla_simbolos_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Habilitar scroll horizontal
        tabla_simbolos_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expandir el tamaño

        # Ajustar el tamaño de las secciones según el contenido
        tabla_simbolos_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)


    def add_items2(self, element):
        if element is None:  # Si el elemento es None, no lo añadimos al árbol
            return None

        if isinstance(element, tuple):
            item = QStandardItem(str(element[0]))
            for child in element[1:]:
                child_item = self.add_items2(child)
                if child_item is not None:  # Solo añadimos el hijo si no es None
                    item.appendRow(child_item)
        elif isinstance(element, list):
            item = QStandardItem("lista_declaraciones")
            for subelement in element:
                subitem = self.add_items2(subelement)
                if subitem is not None:  # Solo añadimos el subelemento si no es None
                    item.appendRow(subitem)
        else:
            item = QStandardItem(str(element))
        return item
    
    def add_items(self, element):
        if element is None:
            return None

        item_text = str(element[0]) if isinstance(element, tuple) else str(element)

        # Consultar la tabla de símbolos para obtener el nombre, tipo y valor
        if isinstance(element, tuple):
            # Si es una asignación, mostramos el nombre, tipo y valor de la variable
            if element[0] == "asignacion":
                variable_name = element[1]
                tipo = get_symbol_type(variable_name)
                valor = next(
                    (s["valor"] for s in symbol_table if s["name"] == variable_name),
                    "Sin asignar",
                )
                item_text += f" - {variable_name} (tipo: {tipo}, valor: {valor})"
            else:
                symbol_info = get_symbol_info(element[1]) if len(element) > 1 else None
                if symbol_info:
                    item_text += f" - {symbol_info}"

        item = QStandardItem(item_text)

        # Añadir hijos al árbol
        if isinstance(element, tuple):
            for child in element[1:]:
                child_item = self.add_items(child)
                if child_item is not None:
                    item.appendRow(child_item)
        elif isinstance(element, list):
            item = QStandardItem("lista_declaraciones")
            for subelement in element:
                subitem = self.add_items(subelement)
                if subitem is not None:
                    item.appendRow(subitem)
        return item

    def apply_format(self, cursor, start, end, color):
        format = QTextCharFormat()
        format.setForeground(color)
        cursor.setPosition(start)
        cursor.movePosition(
            QTextCursor.MoveOperation.Right,
            QTextCursor.MoveMode.KeepAnchor,
            end - start,
        )
        cursor.setCharFormat(format)

    def syncScrollBars(self):
        value = self.textCodigoFuente_2.verticalScrollBar().value()
        self.listNumeroLinea_2.verticalScrollBar().setValue(value)

    def newFile(self):
        self.textCodigoFuente_2.clear()
        self.textCodigoFuente_2.setReadOnly(False)
        self.setWindowTitle("eCompilador - Untitled")
        self.current_path = None

    def saveFile(self):
        if self.current_path is not None:
            fileText = self.textCodigoFuente_2.toPlainText()
            with open(self.current_path, "w") as f:
                f.write(fileText)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        try:
            documents_folder = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
            pathName = QFileDialog.getSaveFileName(
                self, "Save File", documents_folder, "Text files (*.txt)"
            )
            fileText = self.textCodigoFuente_2.toPlainText()
            with open(pathName[0], "w") as f:
                f.write(fileText)
            self.current_path = pathName[0]
            self.setWindowTitle(pathName[0])
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")

    def openFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "Archivos de Texto (*.txt);;Todos los Archivos (*)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                file_content = file.read()
                self.textCodigoFuente_2.setPlainText(file_content)  # Usa setPlainText para QPlainTextEdit
                self.current_path = fileName  # Guardar la ruta del archivo actual

    def closeFile(self):
        self.textCodigoFuente_2.clear()
        self.setWindowTitle("Compilador")
        self.listNumeroLinea_2.setPlainText("")

    def undo(self):
        self.textCodigoFuente_2.undo()

    def redo(self):
        self.textCodigoFuente_2.redo()

    def cut(self):
        self.textCodigoFuente_2.cut()

    def copy(self):
        self.textCodigoFuente_2.copy()

    def paste(self):
        self.textCodigoFuente_2.paste()

    def onTextChanged(self):
        text = self.textCodigoFuente_2.toPlainText()
        lines = text.split("\n")
        if len(lines) != len(self.line_numbers):
            self.line_numbers = list(range(1, len(lines) + 1))
            self.updateLineNumbers()

    # def onCursorChange(self):
    #     cursor = self.textCodigoFuente_2.textCursor()
    #     block_number = cursor.blockNumber() + 1
    #     column_number = cursor.columnNumber()
    #     self.statusbar.showMessage("Linea: " + str(block_number) + " Columna: " + str(column_number))

    def onCursorChange(self):
        cursor = self.textCodigoFuente_2.textCursor()
        block_number = cursor.blockNumber() + 1
        column_number = cursor.columnNumber()
        mensaje = "Linea: " + str(block_number) + " Columna: " + str(column_number)

    def updateLineNumbers(self):
        self.listNumeroLinea_2.blockSignals(True)
        scroll_position = self.listNumeroLinea_2.verticalScrollBar().value()
        self.listNumeroLinea_2.clear()
        lines = len(self.line_numbers)
        line_numbers = "\n".join(str(i + 1) for i in range(lines))
        self.listNumeroLinea_2.setPlainText(line_numbers)
        self.listNumeroLinea_2.verticalScrollBar().setValue(
            scroll_position
        )  # Restaurar la posición de la barra de desplazamiento
        self.listNumeroLinea_2.blockSignals(False)

    def set_default_font_size(self):
        # Establecer el tamaño de fuente por defecto para textEdit
        font = self.textCodigoFuente_2.font()
        font.setPointSize(self.current_fontSize)
        self.textCodigoFuente_2.setFont(font)

        # Establecer el tamaño de fuente por defecto para lineNumberTextEdit
        lineNumberFont = self.listNumeroLinea_2.font()
        lineNumberFont.setFamily("Consolas")
        lineNumberFont.setPointSize(self.current_fontSize)
        self.listNumeroLinea_2.setFont(lineNumberFont)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    sys.exit(app.exec())
