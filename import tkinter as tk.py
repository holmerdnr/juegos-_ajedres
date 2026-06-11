import tkinter as tk
import chess 
import random
import math

# --- 1. CONFIGURACIÓN ESTÉTICA (ESTILO CYBER-NEON) ---
COLOR_1 = "#0b0885"            # Casillas oscuras (Gris Grafito)
COLOR_2 = "#FFFFFF"            # Casillas claras (Azul Eléctrico Neón)
COLOR_S = "#31a83b"            # Indicador de movimientos (Verde Neón Radiante)
BG_PANELES = "#0d0d0d"         # Fondo general de la app (Negro Absoluto)
TEXTO_PANEL = "#003cff"        # Color de acento secundario (Rosa Neón)
TAMANO = 65                    
TIEMPO_INICIAL = 300           

PIEZAS = {
    'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
    'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
}

PIEZAS_INICIALES_BLANCAS = ['P']*8 + ['R']*2 + ['N']*2 + ['B']*2 + ['Q'] + ['K']
PIEZAS_INICIALES_NEGRAS = ['p']*8 + ['r']*2 + ['n']*2 + ['b']*2 + ['q'] + ['k']

PASOS_FADE = ["#ffffff", "#658eca", "#aa0055", "#55002b", "#1a000d", "#0d0d0d"]

def formatear_tiempo(segundos):
    minutos = segundos // 60
    secs = segundos % 60
    return f"{minutos:02d}:{secs:02d}"

def determinar_ganador_y_finalizar(motivo):
    global juego_activo
    juego_activo = False
    if motivo == "tiempo_blancas":
        label_info.config(text="🛸 WINNER: JUGADOR 2 (NEGRAS) 🛸 [Por Tiempo]", bg="#ff007f", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "tiempo_negras":
        label_info.config(text="🛸 WINNER: JUGADOR 1 (BLANCAS) 🛸 [Por Tiempo]", bg="#ff007f", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "mate":
        if board.turn == chess.WHITE:
            label_info.config(text="🛸 WINNER: JUGADOR 2 (NEGRAS) 🛸 [Jaque Mate]", bg="#ff007f", fg="#ffffff", font=("Helvetica", 12, "bold"))
        else:
            label_info.config(text="🛸 WINNER: JUGADOR 1 (BLANCAS) 🛸 [Jaque Mate]", bg="#ff007f", fg="#ffffff", font=("Helvetica", 12, "bold"))
    elif motivo == "tablas":
        label_info.config(text="🌐 SISTEMA EN TABLAS (EMPATE) 🌐", bg="#333333", fg="#ffffff", font=("Helvetica", 12, "bold"))

def actualizar_reloj():
    global tiempo_blancas, tiempo_negras, juego_activo
    if not juego_activo:
        return

    if tiempo_blancas <= 0:
        determinar_ganador_y_finalizar("tiempo_blancas")
        return
    elif tiempo_negras <= 0:
        determinar_ganador_y_finalizar("tiempo_negras")
        return

    if board.turn == chess.WHITE:
        tiempo_blancas -= 1
        label_j1.config(bg="#00f0ff", fg="#000000")
        label_j2.config(bg="#1a1a1a", fg="#666666")
    else:
        tiempo_negras -= 1
        label_j2.config(bg="#00f0ff", fg="#000000")
        label_j1.config(bg="#1a1a1a", fg="#666666")

    label_j1.config(text=f" CORE 01 (B) ⚡ {formatear_tiempo(tiempo_blancas)} ")
    label_j2.config(text=f" CORE 02 (N) ⚡ {formatear_tiempo(tiempo_negras)} ")
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

def animar_desvanecimiento(label_objetivo, texto_base, pieza_nueva, paso=0):
    if paso < len(PASOS_FADE):
        color_actual = PASOS_FADE[paso]
        root.after(60, lambda: label_objetivo.config(text=texto_base, fg="#ffffff"))
        label_objetivo.config(text=f"{texto_base} {pieza_nueva}", fg=color_actual)
        root.after(80, lambda: animar_desvanecimiento(label_objetivo, texto_base, pieza_nueva, paso + 1))
    else:
        label_objetivo.config(text=f"{texto_base} {pieza_nueva}", fg="#ffffff")

def animar_corte(c, f, paso=0):
    x_ini = c * TAMANO
    y_ini = f * TAMANO
    x_fin = (c + 1) * TAMANO
    y_fin = (f + 1) * TAMANO
    
    if paso == 0:
        canvas.create_line(x_ini + 5, y_ini + 5, x_fin - 5, y_fin - 5, fill=TEXTO_PANEL, width=4, tags="efecto_corte")
        root.after(60, lambda: animar_corte(c, f, 1))
    elif paso == 1:
        canvas.delete("efecto_corte")
        canvas.create_line(x_ini + 2, y_ini + 2, x_fin - 2, y_fin - 2, fill="#ffffff", width=5, tags="efecto_corte")
        root.after(60, lambda: animar_corte(c, f, 2))
    elif paso == 2:
        canvas.delete("efecto_corte")

# --- NUEVO: EFECTO DE EXPLOSIÓN DE PARTICULAS CYBER ---
def animar_explosion(cx, cy, particulas=None, paso=0):
    """ Genera una explosión expansiva de partículas neón en el Canvas """
    MAX_PASOS = 12
    if paso == 0:
        # Inicializar partículas con ángulos y velocidades aleatorias
        particulas = []
        colores = ["#ff007f", "#00f0ff", "#39ff14", "#ffffff"] # Colores neón
        for _ in range(25): # Cantidad de partículas
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(2, 7)
            color = random.choice(colores)
            tamano = random.randint(2, 5)
            particulas.append({'ang': angulo, 'vel': velocidad, 'col': color, 'tam': tamano})
    
    # Limpiar partículas del paso anterior
    canvas.delete("explosion")
    
    if paso < MAX_PASOS:
        for p in particulas:
            # Calcular la nueva posición expandida
            distancia = p['vel'] * paso
            px = cx + de_escala_x_y(distancia, p['ang'])[0]
            py = cy + de_escala_x_y(distancia, p['ang'])[1]
            
            # Dibujar cada partícula (pequeños rectángulos/óvalos cibernéticos)
            t = p['tam']
            canvas.create_rectangle(px - t, py - t, px + t, py + t, fill=p['col'], outline="", tags="explosion")
        
        # Siguiente frame de la animación
        root.after(30, lambda: animar_explosion(cx, cy, particulas, paso + 1))
    else:
        canvas.delete("explosion")

def de_escala_x_y(distancia, angulo):
    """ Función auxiliar para calcular coordenadas polares """
    return distancia * math.cos(angulo), distancia * math.sin(angulo)


def click(event):
    global origen, juego_activo, movimientos_posibles, ultimas_blancas_elim, ultimas_negras_elim
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
            habia_captura = board.piece_at(casilla) is not None
            
            board.push(move)
            
            if habia_captura:
                animar_corte(c, 7 - f)
                # --- LLAMADA A LA EXPLOSIÓN ---
                # Calculamos el centro de la casilla cliqueada
                centro_x = c * TAMANO + TAMANO // 2
                centro_y = (7 - f) * TAMANO + TAMANO // 2
                animar_explosion(centro_x, centro_y)
            
            nuevas_blancas, nuevas_negras = obtener_piezas_eliminadas()
            
            if len(nuevas_negras) > len(ultimas_negras_elim):
                pieza_capturada = PIEZAS[nuevas_negras[-1]]
                texto_previo = " ".join([PIEZAS[p] for p in ultimas_negras_elim])
                animar_desvanecimiento(label_eliminadas_izq, texto_previo, pieza_capturada)
                
            elif len(nuevas_blancas) > len(ultimas_blancas_elim):
                pieza_capturada = PIEZAS[nuevas_blancas[-1]]
                texto_previo = " ".join([PIEZAS[p] for p in ultimas_blancas_elim])
                animar_desvanecimiento(label_eliminadas_der, texto_previo, pieza_capturada)

            if board.is_checkmate():
                determinar_ganador_y_finalizar("mate")
            elif board.is_game_over():
                determinar_ganador_y_finalizar("tablas")
            else:
                turno = "Blancas (Core 01)" if board.turn == chess.WHITE else "Negras (Core 02)"
                label_info.config(text=f"SISTEMA OPERATIVO // Turno de: {turno}", fg="#ffffff")

            ultimas_blancas_elim, ultimas_negras_elim = nuevas_blancas, nuevas_negras
            origen = None
            movimientos_posibles = []
        else:
            # Si hace clic en otro lado o movimiento inválido, resetea la selección
            origen = None
            movimientos_posibles = []
        
    actualizar_tablero()

def actualizar_tablero():
    canvas.delete("all")
    for f in range(8):
        for c in range(8):
            sq = chess.square(c, 7 - f)
            color_fondo = COLOR_1 if (f + c) % 2 == 0 else COLOR_2
            canvas.create_rectangle(c*TAMANO, f*TAMANO, (c+1)*TAMANO, (f+1)*TAMANO, fill=color_fondo, outline="")
            
            if sq in movimientos_posibles:
                centro_x = c * TAMANO + TAMANO // 2
                centro_y = f * TAMANO + TAMANO // 2
                canvas.create_oval(centro_x-14, centro_y-14, centro_x+14, centro_y+14, outline=COLOR_S, width=3)

            pieza = board.piece_at(sq)
            if pieza:
                x = c * TAMANO + TAMANO // 2
                y = f * TAMANO + TAMANO // 2
                simbolo = PIEZAS[pieza.symbol()]
                fuente = ("Helvetica", int(TAMANO * 0.65), "bold")
                
                if pieza.color == chess.WHITE:
                    color_cuerpo = "#ffffff"
                    color_borde = "#000000"
                else:
                    color_cuerpo = "#000000"
                    color_borde = "#00f0ff"
                
                for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2), (0,-2), (0,2), (-2,0), (2,0)]:
                    canvas.create_text(x + dx, y + dy, text=simbolo, font=fuente, fill=color_borde)
                
                canvas.create_text(x, y, text=simbolo, font=fuente, fill=color_cuerpo)

def iniciar_partida():
    frame_menu.pack_forget()
    frame_juego_principal.pack(fill="both", expand=True)
    global juego_activo
    juego_activo = True
    actualizar_tablero()
    actualizar_reloj()

# --- 2. ASIGNACIÓN DE VARIABLES GLOBALES ---
board = chess.Board()
origen = None
movimientos_posibles = []
tiempo_blancas = TIEMPO_INICIAL  
tiempo_negras = TIEMPO_INICIAL
juego_activo = False 

ultimas_blancas_elim = []
ultimas_negras_elim = []

# --- 3. CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA ---
root = tk.Tk()
root.title("CHESS_MATRIX // Sistema Cuántico de Ajedrez")
root.configure(bg=BG_PANELES)
root.geometry(f"{TAMANO*8 + 260}x{TAMANO*8 + 160}")

# ==========================================
# PANTALLA DE INICIO
# ==========================================
frame_menu = tk.Frame(root, bg=BG_PANELES)
frame_menu.pack(fill="both", expand=True)

box_intro = tk.Frame(frame_menu, bg="#111111", highlightbackground=COLOR_2, highlightthickness=2, padx=40, pady=40)
box_intro.pack(pady=80)

label_titulo = tk.Label(box_intro, text="⚡ CHESS_MATRIX ⚡", font=("Courier", 26, "bold"), bg="#111111", fg=COLOR_2)
label_titulo.pack()

label_subtitulo = tk.Label(box_intro, text="[ INITIALIZE TACTICAL SIMULATION ]", font=("Courier", 10), bg="#111111", fg=TEXTO_PANEL)
label_subtitulo.pack(pady=(10, 30))

label_decoracion = tk.Label(box_intro, text="♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜", font=("Helvetica", 24), bg="#111111", fg="#ffffff")
label_decoracion.pack(pady=10)

btn_iniciar = tk.Button(
    box_intro, 
    text="► ENTRAR AL SISTEMA", 
    font=("Courier", 12, "bold"), 
    bg=TEXTO_PANEL, 
    fg="#ffffff", 
    activebackground="#ff66b2", 
    activeforeground="#ffffff",
    padx=25, 
    pady=10, 
    bd=0, 
    cursor="cross",  
    command=iniciar_partida
)
btn_iniciar.pack(pady=(30, 0))


# ==========================================
# INTERFAZ DEL JUEGO PRINCIPAL
# ==========================================
frame_juego_principal = tk.Frame(root, bg=BG_PANELES)

frame_superior = tk.Frame(frame_juego_principal, bg=BG_PANELES, pady=15) 
frame_superior.pack(fill="x")

label_j1 = tk.Label(frame_superior, font=("Courier", 13, "bold"), bg="#1a1a1a", fg="#ffffff", padx=15, pady=8, bd=1, relief="flat")
label_j1.pack(side="left", padx=30)
label_j1.config(text=f" CORE 01 (B) ⚡ {formatear_tiempo(tiempo_blancas)} ")

label_j2 = tk.Label(frame_superior, font=("Courier", 13, "bold"), bg="#1a1a1a", fg="#ffffff", padx=15, pady=8, bd=1, relief="flat")
label_j2.pack(side="right", padx=30)
label_j2.config(text=f" CORE 02 (N) ⚡ {formatear_tiempo(tiempo_negras)} ")

frame_juego = tk.Frame(frame_juego_principal, bg=BG_PANELES)
frame_juego.pack(padx=10)

frame_izq = tk.Frame(frame_juego, width=120, bg=BG_PANELES, padx=10)
frame_izq.pack(side="left", fill="y")
tk.Label(frame_izq, text="DATA_LOST J1", font=("Courier", 9, "bold"), bg=BG_PANELES, fg="#555555").pack(anchor="w")
label_eliminadas_izq = tk.Label(frame_izq, text="", font=("Helvetica", 16), bg=BG_PANELES, fg="#ffffff", wraplength=100, justify="left")
label_eliminadas_izq.pack(pady=5, anchor="w")

canvas = tk.Canvas(frame_juego, width=TAMANO*8, height=TAMANO*8, bd=0, highlightthickness=0)
canvas.pack(side="left")
canvas.bind("<Button-1>", click)

frame_der = tk.Frame(frame_juego, width=120, bg=BG_PANELES, padx=10)
frame_der.pack(side="right", fill="y")
tk.Label(frame_der, text="DATA_LOST J2", font=("Courier", 9, "bold"), bg=BG_PANELES, fg="#092D64").pack(anchor="w")
label_eliminadas_der = tk.Label(frame_der, text="", font=("Helvetica", 16), bg=BG_PANELES, fg="#124670", wraplength=100, justify="left")
label_eliminadas_der.pack(pady=5, anchor="w")

label_info = tk.Label(frame_juego_principal, text="SISTEMA OPERATIVO // Turno de: Blancas (Core 01)", font=("Courier", 11), bg="#197D85", fg=COLOR_2, pady=8)
label_info.pack(fill="x", pady=15)

root.mainloop()
