import ply.yacc as yacc
from lexer import tokens

# Lista para almacenar errores sintácticos
errores_sintacticos = []
# Tabla de símbolos
symbol_table = []


def add_symbol(name, tipo, valor=None, scope="global"):
    """Agrega un símbolo a la tabla de símbolos."""
    symbol = {
        "name": name,
        "tipo": tipo,
        "valor": valor,  # Valor inicial como None
        "scope": scope,
        "lineas": [],  # Lista de líneas donde se usa la variable
    }
    symbol_table.append(symbol)


def update_symbol_usage(name, line):
    """Actualiza la lista de líneas donde se usa la variable."""
    for symbol in symbol_table:
        if symbol["name"] == name and line not in symbol["lineas"]:
            symbol["lineas"].append(line)


def print_symbol_table():
    """Imprime la tabla de símbolos en la consola."""
    print("Tabla de Símbolos:")
    for symbol in symbol_table:
        valor_str = symbol["valor"] if symbol["valor"] is not None else "Sin asignar"
        lineas_str = (
            ", ".join(map(str, symbol["lineas"])) if symbol["lineas"] else "None"
        )
        print(
            f"Nombre: {symbol['name']}, Tipo: {symbol['tipo']}, Valor: {valor_str}, Lineas: {lineas_str}"
        )

def p_programa(p):
    "programa : MAIN LBRACE lista_declaraciones RBRACE"
    p[0] = ("programa", p[3])
    print_symbol_table()  # Imprimir la tabla de símbolos aquí


def p_lista_declaraciones(p):
    """lista_declaraciones : lista_declaraciones declaracion
    | declaracion"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_declaracion(p):
    """declaracion : declaracion_variable
    | lista_sentencias
    | comentario"""
    p[0] = p[1]


def p_comentario(p):
    "comentario : COMENTARIO"
    p[0] = None


def p_declaracion_variable(p):
    "declaracion_variable : tipo identificador SEMICOLON"
    # Agregar el símbolo a la tabla
    for id in p[2]:  # Asumiendo que p[2] es una lista de identificadores
        add_symbol(id, p[1], valor=None)  # Valor inicial como None
    p[0] = ("declaracion_variable", p[1], p[2])


def p_identificador(p):
    """identificador : identificador COMMA IDENTIFICADOR
    | IDENTIFICADOR"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tipo(p):
    """tipo : INT
    | DOUBLE
    | INTEGER
    | REAL"""
    p[0] = p[1]


def p_lista_sentencias(p):
    """lista_sentencias : lista_sentencias sentencia
    | sentencia
    | vacio"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_sentencia(p):
    """sentencia : seleccion
    | iteracion
    | repeticion
    | entrada
    | salida
    | asignacion
    | incremento
    | decremento"""
    p[0] = p[1]


def update_symbol_value(name, value):
    """Actualiza el valor de la variable en la tabla de símbolos."""
    for symbol in symbol_table:
        if symbol["name"] == name:
            symbol["valor"] = value  # Actualizar con el nuevo valor


def get_symbol_type(name):
    """Devuelve el tipo de una variable dada."""
    for symbol in symbol_table:
        if symbol["name"] == name:
            return symbol["tipo"]
    return None


def p_asignacion(p):
    "asignacion : IDENTIFICADOR ASSIGN p_expresion_finalizada"
    # Actualizar uso de la variable
    update_symbol_usage(p[1], p.lineno(1))
    # Obtener el tipo de la variable
    tipo_variable = get_symbol_type(p[1])
    if tipo_variable is None:
        raise ValueError(f"La variable '{p[1]}' no ha sido declarada.")

    valor_evaluado = eval_expression(p[3])  # Evaluar la expresión
    update_symbol_value(p[1], valor_evaluado)  # Actualizar el valor en la tabla
    p[0] = (
        "asignacion",
        p[1],
        {"tipo": tipo_variable, "valor": valor_evaluado},
    )


def p_incremento(p):
    "incremento : IDENTIFICADOR INC SEMICOLON"
    update_symbol_usage(p[1], p.lineno(1))  # Actualizar uso de la variable
    p[0] = ("asignacion", p[1], ("++", p[1], 1))


def p_decremento(p):
    "decremento : IDENTIFICADOR DEC SEMICOLON"
    update_symbol_usage(p[1], p.lineno(1))  # Actualizar uso de la variable
    p[0] = ("asignacion", p[1], ("--", p[1], 1))


def p_expresion_finalizada(p):
    """p_expresion_finalizada : expresion SEMICOLON
    | SEMICOLON"""
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = None


def p_seleccion(p):
    """seleccion : IF expresion THEN lista_sentencias END
    | IF expresion THEN lista_sentencias ELSE lista_sentencias END"""
    update_symbol_usage(p[2], p.lineno(1))  # Actualizar uso de la expresión
    if len(p) == 6:
        p[0] = ("if", p[2], p[4])
    else:
        p[0] = ("if-else", p[2], p[4], p[6])


def p_iteracion(p):
    "iteracion : WHILE expresion DO lista_sentencias END"
    update_symbol_usage(p[2], p.lineno(1))  # Actualizar uso de la expresión
    p[0] = ("while", p[2], p[4])


def p_repeticion(p):
    "repeticion : DO lista_sentencias UNTIL expresion SEMICOLON"
    update_symbol_usage(p[4], p.lineno(1))  # Actualizar uso de la expresión
    p[0] = ("do-until", p[2], p[4])


def p_entrada(p):
    "entrada : CIN expresion SEMICOLON"
    update_symbol_usage(p[2], p.lineno(1))  # Actualizar uso de la expresión
    p[0] = ("cin", p[2])


def p_salida(p):
    "salida : COUT expresion SEMICOLON"
    update_symbol_usage(p[2], p.lineno(1))  # Actualizar uso de la expresión
    p[0] = ("cout", p[2])


def p_expresion(p):
    """expresion : expresion AND expresion
    | expresion OR expresion
    | expresion_simple operacion_relacional expresion_simple
    | expresion_simple"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_operacion_relacional(p):
    """operacion_relacional : MORETHAN
    | LESSTHAN
    | MOREEQUALS
    | LESSEQUALS
    | EQUALS
    | NOTEQUALS
    | AND
    | OR"""
    p[0] = p[1]


def eval_expression(expr):
    """Evalúa una expresión recursivamente y retorna su valor final."""
    if isinstance(expr, tuple):
        op = expr[0]
        left = eval_expression(expr[1])
        right = eval_expression(expr[2])

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "mod":
            return left % right
        elif op == "pot":
            return left**right
    else:
        # Si es un número literal, lo retornamos convertido a int o float
        if isinstance(expr, str) and expr.isdigit():
            return int(expr)
        try:
            return float(expr)  # Para manejar decimales
        except ValueError:
            # Si es un identificador, obtenemos su valor de la tabla de símbolos
            for symbol in symbol_table:
                if symbol["name"] == expr:
                    if symbol["valor"] is not None:  # Solo retornamos si tiene un valor
                        return symbol["valor"]
                    else:
                        raise ValueError(
                            f"La variable '{expr}' no tiene un valor asignado."
                        )
    return expr


def p_expresion_simple(p):
    """expresion_simple : expresion_simple primer_operador term
    | term"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_primer_operador(p):
    """primer_operador : SUMA
    | RESTA"""
    p[0] = p[1]


def p_term(p):
    """term : term segundo_operador factor
    | factor"""
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_segundo_operador(p):
    """segundo_operador : MULT
    | DIVIDE
    | MOD"""
    p[0] = p[1]


def p_factor(p):
    """factor : factor tercer_operador componente
    | componente"""
    if len(p) == 4:
        p[0] = ("pot", p[1], p[3])
    else:
        p[0] = p[1]


def p_tercer_operador(p):
    "tercer_operador : POT"
    p[0] = p[1]


def p_componente(p):
    """componente : LPARENT expresion RPARENT
    | numero
    | IDENTIFICADOR"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        if isinstance(p[1], str):  # Si es un identificador
            update_symbol_usage(p[1], p.lineno(1))  # Actualizar uso de la variable
        p[0] = p[1]


def p_numero(p):
    """numero : INT
    | DOUBLE
    | LPARENT RESTA INT RPARENT
    | LPARENT RESTA DOUBLE RPARENT"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = -p[3]


def p_vacio(p):
    "vacio :"
    p[0] = []


def p_error(p):
    if p:
        error_message = f"Syntax error at '{p.value}', line {p.lineno}"
        errores_sintacticos.append(error_message)
        # Recuperar el análisis después de un error
        parser.errok()
    else:
        error_message = "Syntax error at EOF"
        errores_sintacticos.append(error_message)


# Función para establecer el QTextEdit para errores
def set_error_output(output_widget):
    parser.error_output = output_widget


def get_sintactic_errors():
    return errores_sintacticos


def get_symbol_info(name):
    """Busca en la tabla de símbolos y devuelve un string con el nombre, tipo y valor de la variable."""
    for symbol in symbol_table:
        if symbol["name"] == name:
            return f"{symbol['name']} (tipo: {symbol['tipo']}, valor: {symbol['valor'] if symbol['valor'] is not None else 'none'})"
    return None


parser = yacc.yacc(errorlog=yacc.NullLogger())
