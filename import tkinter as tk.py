import tkinter as tk
import chess 

# --- 1. CONFIGURACIÓN ESTÉTICA ---
COLOR_1 = "#f0d9b5"            # Crema clásico de torneos
COLOR_2 = "#b58863"            # Marrón madera clásico
COLOR_S = "#81b64c"            # Verde oliva moderno para los destinos
BG_PANELES = "#262522"         # Gris oscuro elegante (Estilo Chess.com)
TEXTO_PANEL = "#ffffff"        # Texto blanco para contraste
TAMANO = 65                    # Tamaño de las casillas
TIEMPO_INICIAL = 300           # Tiempo en segundos (5 minutos por jugador)

# Símbolos Unicode estilizados para las piezas
PIEZAS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

# Listas para verificar piezas capturadas
PIEZAS_INICIALES_BLANCAS = ['P']*8 + ['R']*2 + ['N']*2 + ['B']*2 + ['Q'] + ['K']
PIEZAS_INICIALES_NEGRAS = ['p']*8 + ['r']*2 + ['n']*2 + ['b']*2 + ['q'] + ['k']

def formatear_tiempo(segundos):
    minutos = segundos // 60
    secs = segundos % 60
    return f"{minutos:02d}:{secs:02d}"

def determinar_ganador_y_finalizar(motivo):
    """Muestra un cartel llamativo con el WINNER y detiene el juego"""
    global juego_activo
    juego_activo = False
    
    if motivo == "tiempo_blancas":
        label_info.config(text="🏆 WINNER: JUGADOR 2 (NEGRAS) 🏆 [Por Tiempo]", bg="#81b64c", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "tiempo_negras":
        label_info.config(text="🏆 WINNER: JUGADOR 1 (BLANCAS) 🏆 [Por Tiempo]", bg="#81b64c", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "mate":
        # Si es el turno de las blancas y hay mate, significa que perdieron las blancas (gana el negro)
        if board.turn == chess.WHITE:
            label_info.config(text="🏆 WINNER: JUGADOR 2 (NEGRAS) 🏆 [Por Jaque Mate]", bg="#81b64c", fg="#ffffff", font=("Helvetica", 12, "bold"))
        else:
            label_info.config(text="🏆 WINNER: JUGADOR 1 (BLANCAS) 🏆 [Por Jaque Mate]", bg="#81b64c", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "tablas":
        label_info.config(text="🤝 PARTIDA EN TABLAS (EMPATE) 🤝", bg="#444444", fg="#ffffff", font=("Helvetica", 12, "bold"))

def actualizar_reloj():
    global tiempo_blancas, tiempo_negras, juego_activo
    if not juego_activo:
        return

    # Verificar si a alguien se le acabó el tiempo
    if tiempo_blancas <= 0:
        determinar_ganador_y_finalizar("tiempo_blancas")
        return
    elif tiempo_negras <= 0:
        determinar_ganador_y_finalizar("tiempo_negras")
        return

    if board.turn == chess.WHITE:
        tiempo_blancas -= 1
        label_j1.config(bg="#ffffff", fg="#000000")
        label_j2.config(bg="#312e2b", fg="#aaaaaa")
    else:
        tiempo_negras -= 1
        label_j2.config(bg="#ffffff", fg="#000000")
        label_j1.config(bg="#312e2b", fg="#aaaaaa")

    label_j1.config(text=f" JUGADOR 1  |  {formatear_tiempo(tiempo_blancas)} ")
    label_j2.config(text=f" JUGADOR 2  |  {formatear_tiempo(tiempo_negras)} ")
    root.after(1000, actualizar_reloj)

def obtener_piezas_eliminadas():
    piezas_vivas = [pieza.symbol() for pieza in board.piece_map().values()]
    blancas_eliminadas = PIEZAS_INICIALES_BLANCAS.copy()
    negras_eliminadas = PIEZAS_INICIALES_NEGRAS.copy()
    
    for p in piezas_vivas:
        if p.isupper() and p in blancas_eliminadas:
            blancas_eliminadas.remove(p)
        elif p.islower() and p in negras_eliminadas:
            negras_eliminadas.remove(p)
            
    orden = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    blancas_eliminadas.sort(key=lambda x: orden.index(x))
    negras_eliminadas.sort(key=lambda x: orden.index(x))
    
    return blancas_eliminadas, negras_eliminadas

def click(event):
    global origen, juego_activo, movimientos_posibles
    if not juego_activo:
        return

    c, f = event.x // TAMANO, 7 - (event.y // TAMANO)
    casilla = chess.square(c, f)
    
    if origen is None:
        if board.piece_at(casilla) and board.piece_at(casilla).color == board.turn:
            origen = casilla
            movimientos_posibles = [m.to_square for m in board.legal_moves if m.from_square == origen]
    else:
        move = chess.Move(origen, casilla)
        if move not in board.legal_moves and chess.Move(origen, casilla, chess.QUEEN) in board.legal_moves:
            move = chess.Move(origen, casilla, chess.QUEEN)
            
        if move in board.legal_moves:
            board.push(move)
            
            # --- NUEVO: Verificar si el juego terminó por reglas de ajedrez ---
            if board.is_checkmate():
                determinar_ganador_y_finalizar("mate")
            elif board.is_game_over():  # Tablas, ahogado, etc.
                determinar_ganador_y_finalizar("tablas")
            else:
                turno = "Blancas (Jugador 1)" if board.turn == chess.WHITE else "Negras (Jugador 2)"
                label_info.config(text=f"Turno actual: {turno}", fg="#ffffff")

        origen = None
        movimientos_posibles = []
        
    actualizar_tablero()

def actualizar_tablero():
    canvas.delete("all")
    
    for f in range(8):
        for c in range(8):
            sq = chess.square(c, 7 - f)
            color_fondo = COLOR_1 if (f + c) % 2 == 0 else COLOR_2
            
            canvas.create_rectangle(
                c*TAMANO, f*TAMANO, (c+1)*TAMANO, (f+1)*TAMANO, 
                fill=color_fondo, outline=""
            )
            
            if sq in movimientos_posibles:
                centro_x = c * TAMANO + TAMANO // 2
                centro_y = f * TAMANO + TAMANO // 2
                x1, y1 = centro_x, centro_y - 8
                x2, y2 = centro_x - 8, centro_y + 6
                x3, y3 = centro_x + 8, centro_y + 6
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=COLOR_S, outline="")

            pieza = board.piece_at(sq)
            if pieza:
                canvas.create_text(
                    c*TAMANO + TAMANO//2, f*TAMANO + TAMANO//2, 
                    text=PIEZAS[pieza.symbol()], font=("Helvetica", int(TAMANO * 0.6))
                )

    blancas_elim, negras_elim = obtener_piezas_eliminadas()
    label_eliminadas_izq.config(text=" ".join([PIEZAS[p] for p in negras_elim]))
    label_eliminadas_der.config(text=" ".join([PIEZAS[p] for p in blancas_elim]))

# --- 2. ASIGNACIÓN DE VARIABLES GLOBALES ---
board = chess.Board()
origen = None
movimientos_posibles = []
tiempo_blancas = TIEMPO_INICIAL  
tiempo_negras = TIEMPO_INICIAL
juego_activo = True

# --- 3. CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA ---
root = tk.Tk()
root.title("Ajedrez Profesional con Detección de Ganador")
root.configure(bg=BG_PANELES)

frame_superior = tk.Frame(root, bg=BG_PANELES, pady=15) 
frame_superior.pack(fill="x")

label_j1 = tk.Label(frame_superior, font=("Courier", 14, "bold"), bg="#312e2b", fg="#ffffff", padx=15, pady=8, bd=1, relief="solid")
label_j1.pack(side="left", padx=30)

label_j2 = tk.Label(frame_superior, font=("Courier", 14, "bold"), bg="#312e2b", fg="#ffffff", padx=15, pady=8, bd=1, relief="solid")
label_j2.pack(side="right", padx=30)

frame_juego = tk.Frame(root, bg=BG_PANELES)
frame_juego.pack(padx=10)

frame_izq = tk.Frame(frame_juego, width=120, bg=BG_PANELES, padx=10)
frame_izq.pack(side="left", fill="y")
tk.Label(frame_izq, text="CAPTURAS J1", font=("Helvetica", 9, "bold"), bg=BG_PANELES, fg="#8b8987").pack(anchor="w")
label_eliminadas_izq = tk.Label(frame_izq, text="", font=("Helvetica", 16), bg=BG_PANELES, fg="#ffffff", wraplength=100, justify="left")
label_eliminadas_izq.pack(pady=5, anchor="w")

canvas = tk.Canvas(frame_juego, width=TAMANO*8, height=TAMANO*8, bd=0, highlightthickness=0)
canvas.pack(side="left")
canvas.bind("<Button-1>", click)

frame_der = tk.Frame(frame_juego, width=120, bg=BG_PANELES, padx=10)
frame_der.pack(side="right", fill="y")
tk.Label(frame_der, text="CAPTURAS J2", font=("Helvetica", 9, "bold"), bg=BG_PANELES, fg="#8b8987").pack(anchor="w")
label_eliminadas_der = tk.Label(frame_der, text="", font=("Helvetica", 16), bg=BG_PANELES, fg="#ffffff", wraplength=100, justify="left")
label_eliminadas_der.pack(pady=5, anchor="w")

label_info = tk.Label(root, text="Turno actual: Blancas (Jugador 1)", font=("Helvetica", 11), bg="#1e1c1a", fg="#ffffff", pady=8)
label_info.pack(fill="x", pady=15)

# --- 4. EJECUCIÓN DE PROCESOS ---
actualizar_tablero()
actualizar_reloj()

root.mainloop()
