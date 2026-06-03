import tkinter as tk
import chess 

# --- CONFIGURACIÓN EDITABLE ---
COLOR_1 = "#ffffff"  
COLOR_2 = "#b58863"  
COLOR_S = "#769656"  # Color del triángulo central de destino (Verde)
TAMANO = 60          
TIEMPO_INICIAL = 300  

# Mapeo de piezas a símbolos Unicode
PIEZAS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

def formatear_tiempo(segundos):
    minutos = segundos // 60
    secs = segundos % 60
    return f"{minutos:02d}:{secs:02d}"

def actualizar_reloj():
    global tiempo_blancas, tiempo_negras, juego_activo
    if not juego_activo:
        return

    if tiempo_blancas <= 0:
        label_info.config(text="¡Tiempo agotado! Ganan las Negras (Jugador 2)", fg="red")
        juego_activo = False
        return
    elif tiempo_negras <= 0:
        label_info.config(text="¡Tiempo agotado! Ganan las Blancas (Jugador 1)", fg="red")
        juego_activo = False
        return

    if board.turn == chess.WHITE:
        tiempo_blancas -= 1
    else:
        tiempo_negras -= 1

    label_j1.config(text=f"Jugador 1 (Blancas): {formatear_tiempo(tiempo_blancas)}")
    label_j2.config(text=f"Jugador 2 (Negras): {formatear_tiempo(tiempo_negras)}")
    root.after(1000, actualizar_reloj)

def click(event):
    global origen, juego_activo, movimientos_posibles
    if not juego_activo:
        return

    c, f = event.x // TAMANO, 7 - (event.y // TAMANO)
    casilla = chess.square(c, f)
    
    if origen is None:
        if board.piece_at(casilla) and board.piece_at(casilla).color == board.turn:
            origen = casilla
            # Guardamos los destinos posibles de la pieza seleccionada
            movimientos_posibles = [movimiento.to_square for movimiento in board.legal_moves if movimiento.from_square == origen]
    else:
        move = chess.Move(origen, casilla)
        if move not in board.legal_moves and chess.Move(origen, casilla, chess.QUEEN) in board.legal_moves:
            move = chess.Move(origen, casilla, chess.QUEEN)
            
        if move in board.legal_moves:
            board.push(move)
            
            if board.is_game_over():
                juego_activo = False
                label_info.config(text=f"Fin de la partida: {board.result()}", fg="blue")
            else:
                turno = "Jugador 1 (Blancas)" if board.turn == chess.WHITE else "Jugador 2 (Negras)"
                label_info.config(text=f"Turno de: {turno}", fg="black")

        origen = None
        movimientos_posibles = []  # Limpiamos los destinos al soltar la pieza
        
    actualizar_tablero()

def actualizar_tablero():
    canvas.delete("all")
    for f in range(8):
        for c in range(8):
            sq = chess.square(c, 7 - f)
            
            # Fondo base de la casilla
            color_fondo = COLOR_1 if (f + c) % 2 == 0 else COLOR_2
            
            # Dibujar la casilla estándar (sin bordes raros)
            canvas.create_rectangle(
                c*TAMANO, f*TAMANO, (c+1)*TAMANO, (f+1)*TAMANO, 
                fill=color_fondo, outline=""
            )
            
            # --- MODIFICADO: Si la casilla es un DESTINO posible, dibujamos el triángulo en medio ---
            if sq in movimientos_posibles:
                centro_x = c * TAMANO + TAMANO // 2
                centro_y = f * TAMANO + TAMANO // 2
                
                # Coordenadas del triángulo pequeño central (de 8 píxeles para que sea discreto)
                x1, y1 = centro_x, centro_y - 10       # Vértice superior
                x2, y2 = centro_x - 10, centro_y + 8   # Vértice inferior izquierdo
                x3, y3 = centro_x + 10, centro_y + 8   # Vértice inferior derecho
                
                canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=COLOR_S, outline="")

            # Dibujar la pieza
            pieza = board.piece_at(sq)
            if pieza:
                canvas.create_text(c*TAMANO + TAMANO//2, f*TAMANO + TAMANO//2, text=PIEZAS[pieza.symbol()], font=(None, TAMANO//2))

# Inicialización de variables
board = chess.Board()
origen = None
movimientos_posibles = []
tiempo_blancas = TIEMPO_INICIAL
tiempo_negras = TIEMPO_INICIAL
juego_activo = True

# Interfaz gráfica
root = tk.Tk()
root.title("Ajedrez - Guía de Destinos")

frame_superior = tk.Frame(root, padx=10, pady=10) 
frame_superior.pack(fill="x")

label_j1 = tk.Label(frame_superior, text=f"Jugador 1 (Blancas): {formatear_tiempo(tiempo_blancas)}", font=("Arial", 11, "bold"))
label_j1.pack(side="left", padx=20)

label_j2 = tk.Label(frame_superior, text=f"Jugador 2 (Negras): {formatear_tiempo(tiempo_negras)}", font=("Arial", 11, "bold"))
label_j2.pack(side="right", padx=20)

label_info = tk.Label(root, text="Turno de: Jugador 1 (Blancas)", font=("Arial", 10, "italic"), pady=5)
label_info.pack()

canvas = tk.Canvas(root, width=TAMANO*8, height=TAMANO*8)
canvas.pack()
canvas.bind("<Button-1>", click)

actualizar_tablero()
actualizar_reloj()

root.mainloop()
