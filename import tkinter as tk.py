import tkinter as tk
import chess

# --- CONFIGURACIÓN EDITABLE ---
COLOR_1, COLOR_2 = "#f0d9b5", "#b58863"  # Colores del tablero
COLOR_S = "#7fffd4"                      # Color de casilla seleccionada
TAMANO = 60                              # Tamaño de cada casilla en píxeles

# Mapeo de piezas a símbolos Unicode reales de ajedrez
PIEZAS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

def click(event):
    global origen
    # Convertir las coordenadas del click a fila y columna del tablero
    c, f = event.x // TAMANO, 7 - (event.y // TAMANO)
    casilla = chess.square(c, f)
    
    if origen is None:
        if board.piece_at(casilla) and board.piece_at(casilla).color == board.turn:
            origen = casilla
    else:
        # Intentar mover (incluye coronación automática a Reina si es peón)
        move = chess.Move(origen, casilla)
        if move not in board.legal_moves and chess.Move(origen, casilla, chess.QUEEN) in board.legal_moves:
            move = chess.Move(origen, casilla, chess.QUEEN)
            
        if move in board.legal_moves:
            board.push(move)
        origen = None
    actualizar_tablero()

def actualizar_tablero():
    canvas.delete("all")
    for f in range(8):
        for c in range(8):
            sq = chess.square(c, 7 - f)
            # Elegir color base o color de selección
            color = COLOR_S if sq == origen else (COLOR_1 if (f + c) % 2 == 0 else COLOR_2)
            canvas.create_rectangle(c*TAMANO, f*TAMANO, (c+1)*TAMANO, (f+1)*TAMANO, fill=color, outline="")
            
            pieza = board.piece_at(sq)
            if pieza:
                canvas.create_text(c*TAMANO + TAMANO//2, f*TAMANO + TAMANO//2, text=PIEZAS[pieza.symbol()], font=(None, TAMANO//2))

# Inicialización del juego y la ventana
board = chess.Board()
origen = None

root = tk.Tk()
root.title("Mini Ajedrez")
canvas = tk.Canvas(root, width=TAMANO*8, height=TAMANO*8)
canvas.pack()
canvas.bind("<Button-1>", click)

actualizar_tablero()
root.mainloop()