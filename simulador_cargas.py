import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

K = 8.99e9 

class Carga:
    def __init__(self, q, x, y=0.0):
        self.q = q
        self.x = x
        self.y = y

def calcular_fuerza(c1, c2):
    r = math.sqrt((c2.x - c1.x)**2 + (c2.y - c1.y)**2)
    if r == 0:
        return 0.0, 0.0
    
    f_mag = K * abs(c1.q * c2.q) / (r**2)
    theta = math.atan2(c2.y - c1.y, c2.x - c1.x)
    
    if c1.q * c2.q > 0:
        f_mag = -f_mag
        
    fx = f_mag * math.cos(theta)
    fy = f_mag * math.sin(theta)
    return fx, fy

def calcular_campo(cargas, px, py):
    ex = 0.0
    ey = 0.0
    for c in cargas:
        r = math.sqrt((px - c.x)**2 + (py - c.y)**2)
        if r == 0:
            continue
        e_mag = K * abs(c.q) / (r**2)
        theta = math.atan2(py - c.y, px - c.x)
        if c.q < 0:
            e_mag = -e_mag
        ex += e_mag * math.cos(theta)
        ey += e_mag * math.sin(theta)
    return ex, ey

st.set_page_config(page_title="Simulador Electroestatico", layout="wide")
st.title("Simulador de Cargas Electricas")

st.sidebar.header("Configuracion del Sistema")
modo = st.sidebar.radio("Seleccione el espacio:", ["1D", "2D"])
num_cargas = st.sidebar.number_input("Numero de cargas:", min_value=2, max_value=10, value=3)

st.sidebar.subheader("Visualizacion")
mostrar_mapa = st.sidebar.checkbox("Mostrar mapa de campo vectorial", value=True)
mostrar_transparencia = st.sidebar.checkbox("Activar intensidad por transparencia", value=True)
mostrar_comp_fuerza = st.sidebar.checkbox("Mostrar componentes de fuerza", value=True)
mostrar_comp_campo = st.sidebar.checkbox("Mostrar componentes de campo electrico", value=True)

cargas = []
st.sidebar.subheader("Valores de las Cargas")
for i in range(num_cargas):
    with st.sidebar.expander(f"Carga {i+1}", expanded=(i<3)):
        q = st.number_input(f"Carga (Coulombs) q{i+1}", value=1e-6, format="%e", key=f"q{i}")
        x = st.number_input(f"Posicion X q{i+1}", value=float(i*2), key=f"x{i}")
        y = 0.0
        if modo == "2D":
            y = st.number_input(f"Posicion Y q{i+1}", value=float(i), key=f"y{i}")
        cargas.append(Carga(q, x, y))

posiciones_cargas = set()
for i, c in enumerate(cargas):
    if (c.x, c.y) in posiciones_cargas:
        st.error(f"Error: La carga q{i+1} se encuentra exactamente en la misma posicion que otra carga ({c.x}, {c.y}). Por favor modifique las coordenadas para continuar.")
        st.stop()
    posiciones_cargas.add((c.x, c.y))

st.sidebar.subheader("Puntos de Campo Electrico")
num_puntos = st.sidebar.number_input("Numero de puntos:", min_value=3, max_value=10, value=3)
puntos_campo = []
for i in range(num_puntos):
    with st.sidebar.expander(f"Punto {i+1}", expanded=False):
        px = st.number_input(f"Posicion X P{i+1}", value=float(i*2 + 1), key=f"px_c{i}")
        py = 0.0
        if modo == "2D":
            py = st.number_input(f"Posicion Y P{i+1}", value=float(i + 1), key=f"py_c{i}")
        puntos_campo.append((px, py))

st.sidebar.subheader("Analisis de Fuerza")
idx_analisis = st.sidebar.selectbox("Seleccione la carga a analizar:", range(1, num_cargas + 1)) - 1
carga_objetivo = cargas[idx_analisis]

fx_neta, fy_neta = 0.0, 0.0
for i, c in enumerate(cargas):
    if i != idx_analisis:
        fx, fy = calcular_fuerza(carga_objetivo, c)
        fx_neta += fx
        fy_neta += fy
        
f_neta_mag = math.sqrt(fx_neta**2 + fy_neta**2)

if f_neta_mag < 1e-12:
    fx_neta = 0.0
    fy_neta = 0.0
    f_neta_mag = 0.0

st.subheader("Plano Interactivo")
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_title("Simulador de Cargas, Fuerza y Campo Electrico", pad=20)

all_x_calc = [c.x for c in cargas] + [p[0] for p in puntos_campo]
all_y_calc = [c.y for c in cargas] + [p[1] for p in puntos_campo] if modo == "2D" else [0]
rango_x = max(all_x_calc) - min(all_x_calc)
rango_y = max(all_y_calc) - min(all_y_calc) if modo == "2D" else 0
rango_max = max(rango_x, rango_y)

if rango_max == 0:
    rango_max = 2.0

margen_x = max(rango_max * 0.3, 1.0)
lim_x_min = min(all_x_calc) - margen_x
lim_x_max = max(all_x_calc) + margen_x

if modo == "2D":
    margen_y = max(rango_max * 0.3, 1.0)
    lim_y_min = min(all_y_calc) - margen_y
    lim_y_max = max(all_y_calc) + margen_y
else:
    lim_y_min = -2
    lim_y_max = 2

if mostrar_mapa:
    if modo == "2D":
        X_grid, Y_grid = np.meshgrid(np.linspace(lim_x_min, lim_x_max, 20), np.linspace(lim_y_min, lim_y_max, 20))
        Ex_grid, Ey_grid = np.zeros_like(X_grid), np.zeros_like(Y_grid)
        Mag_grid = np.zeros_like(X_grid)
        
        for i in range(X_grid.shape[0]):
            for j in range(X_grid.shape[1]):
                ex, ey = calcular_campo(cargas, X_grid[i,j], Y_grid[i,j])
                mag = math.sqrt(ex**2 + ey**2)
                Mag_grid[i,j] = mag
                if mag > 0:
                    Ex_grid[i,j] = ex / mag
                    Ey_grid[i,j] = ey / mag
                    
        X_flat = X_grid.flatten()
        Y_flat = Y_grid.flatten()
        Ex_flat = Ex_grid.flatten()
        Ey_flat = Ey_grid.flatten()
        Mag_flat = Mag_grid.flatten()
        
        rgba_colors = np.zeros((len(Mag_flat), 4))
        
        if mostrar_transparencia and Mag_flat.max() > 0:
            log_mag = np.log10(Mag_flat + 1e-12)
            min_val = np.min(log_mag)
            max_val = np.max(log_mag)
            if max_val > min_val:
                norm = (log_mag - min_val) / (max_val - min_val)
                color_intensity = 0.85 - 0.75 * norm
                rgba_colors[:, 0] = color_intensity
                rgba_colors[:, 1] = color_intensity
                rgba_colors[:, 2] = color_intensity
                rgba_colors[:, 3] = 0.05 + 0.95 * (norm ** 2)
            else:
                rgba_colors[:, 0:3] = [0.4, 0.4, 0.4]
                rgba_colors[:, 3] = 0.5
        else:
            rgba_colors[:, 0:3] = [0.4, 0.4, 0.4]
            rgba_colors[:, 3] = 0.3
            
        ax.quiver(X_flat, Y_flat, Ex_flat, Ey_flat, color=rgba_colors, pivot='middle', scale=30)
    else:
        X_grid = np.linspace(lim_x_min, lim_x_max, 25)
        Y_grid = np.zeros_like(X_grid)
        Ex_grid, Ey_grid = np.zeros_like(X_grid), np.zeros_like(Y_grid)
        Mag_grid = np.zeros_like(X_grid)
        
        for i in range(len(X_grid)):
            ex, ey = calcular_campo(cargas, X_grid[i], Y_grid[i])
            mag = math.sqrt(ex**2 + ey**2)
            Mag_grid[i] = mag
            if mag > 0:
                Ex_grid[i] = ex / mag
                
        rgba_colors = np.zeros((len(Mag_grid), 4))
        
        if mostrar_transparencia and Mag_grid.max() > 0:
            log_mag = np.log10(Mag_grid + 1e-12)
            min_val = np.min(log_mag)
            max_val = np.max(log_mag)
            if max_val > min_val:
                norm = (log_mag - min_val) / (max_val - min_val)
                color_intensity = 0.85 - 0.75 * norm
                rgba_colors[:, 0] = color_intensity
                rgba_colors[:, 1] = color_intensity
                rgba_colors[:, 2] = color_intensity
                rgba_colors[:, 3] = 0.05 + 0.95 * (norm ** 2)
            else:
                rgba_colors[:, 0:3] = [0.4, 0.4, 0.4]
                rgba_colors[:, 3] = 0.5
        else:
            rgba_colors[:, 0:3] = [0.4, 0.4, 0.4]
            rgba_colors[:, 3] = 0.3
            
        ax.quiver(X_grid, Y_grid, Ex_grid, Ey_grid, color=rgba_colors, pivot='middle', scale=25)

for i, c in enumerate(cargas):
    if c.q == 0:
        color = 'gray'
    elif c.q > 0:
        color = 'red'
    else:
        color = 'blue'
    ax.scatter(c.x, c.y, c=color, s=400, zorder=5)
    ax.text(c.x + rango_max*0.02, c.y + rango_max*0.02, f'q{i+1}', fontsize=12, fontweight='bold')

for i, (px, py) in enumerate(puntos_campo):
    ax.scatter(px, py, c='black', marker='x', s=50, zorder=4)
    ax.text(px + rango_max*0.02, py - rango_max*0.02, f'P{i+1}', fontsize=10)

fx_visual = 0.0
fy_visual = 0.0
datos_campo = []

for i, (px, py) in enumerate(puntos_campo):
    ex, ey = calcular_campo(cargas, px, py)
    mag = math.sqrt(ex**2 + ey**2)
    if mag < 1e-12:
        ex, ey, mag = 0.0, 0.0, 0.0
    datos_campo.append((px, py, ex, ey, mag))

if f_neta_mag > 0:
    factor_fuerza = (rango_max * 0.4) / f_neta_mag
    fx_visual = fx_neta * factor_fuerza
    fy_visual = fy_neta * factor_fuerza

    ax.annotate('', 
                xy=(carga_objetivo.x + fx_visual, carga_objetivo.y + fy_visual), 
                xytext=(carga_objetivo.x, carga_objetivo.y),
                arrowprops=dict(arrowstyle="-|>", color='green', lw=3, mutation_scale=25),
                zorder=6)
    ax.plot([], [], color='green', label='Fuerza Neta')

    if modo == "2D" and mostrar_comp_fuerza:
        ax.plot([carga_objetivo.x, carga_objetivo.x + fx_visual], 
                [carga_objetivo.y, carga_objetivo.y], 
                color='orange', linestyle='--', linewidth=2, zorder=3, label='Componente Fx')
        ax.plot([carga_objetivo.x + fx_visual, carga_objetivo.x + fx_visual], 
                [carga_objetivo.y, carga_objetivo.y + fy_visual], 
                color='purple', linestyle='--', linewidth=2, zorder=3, label='Componente Fy')

campo_comp_x_agregado = False
campo_comp_y_agregado = False

for px, py, ex, ey, mag in datos_campo:
    if mag == 0:
        continue
    
    factor_campo = (rango_max * 0.3) / mag
    ex_v = ex * factor_campo
    ey_v = ey * factor_campo
        
    ax.annotate('', 
                xy=(px + ex_v, py + ey_v), 
                xytext=(px, py),
                arrowprops=dict(arrowstyle="->", color='magenta', lw=2, mutation_scale=15),
                zorder=4)

    if modo == "2D" and mostrar_comp_campo:
        etiqueta_x = 'Componente Ex' if not campo_comp_x_agregado else None
        etiqueta_y = 'Componente Ey' if not campo_comp_y_agregado else None
        
        ax.plot([px, px + ex_v], 
                [py, py], 
                color='dodgerblue', linestyle=':', linewidth=1.5, zorder=3, label=etiqueta_x)
        ax.plot([px + ex_v, px + ex_v], 
                [py, py + ey_v], 
                color='hotpink', linestyle=':', linewidth=1.5, zorder=3, label=etiqueta_y)
        
        campo_comp_x_agregado = True
        campo_comp_y_agregado = True

if len(datos_campo) > 0:
    ax.plot([], [], color='magenta', label='Campo en Puntos')

ax.legend(loc='upper right')
ax.axhline(0, color='black', linewidth=1)

lim_x_max = max(lim_x_max, carga_objetivo.x + fx_visual + margen_x)
lim_x_min = min(lim_x_min, carga_objetivo.x + fx_visual - margen_x)
for px, py, ex, ey, mag in datos_campo:
    if mag > 0:
        fc = (rango_max * 0.3) / mag
        lim_x_max = max(lim_x_max, px + (ex * fc) + margen_x)
        lim_x_min = min(lim_x_min, px + (ex * fc) - margen_x)
        
ax.set_xlim(lim_x_min, lim_x_max)

if modo == "2D":
    lim_y_max = max(lim_y_max, carga_objetivo.y + fy_visual + margen_y)
    lim_y_min = min(lim_y_min, carga_objetivo.y + fy_visual - margen_y)
    for px, py, ex, ey, mag in datos_campo:
        if mag > 0:
            fc = (rango_max * 0.3) / mag
            lim_y_max = max(lim_y_max, py + (ey * fc) + margen_y)
            lim_y_min = min(lim_y_min, py + (ey * fc) - margen_y)
            
    ax.set_ylim(lim_y_min, lim_y_max)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_ylabel("Eje Y (m)")
else:
    ax.get_yaxis().set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(lim_y_min, lim_y_max)
    
ax.set_aspect('equal', adjustable='box')
ax.set_xlabel("Eje X (m)")

st.pyplot(fig)

st.markdown("---")

col_fuerza, col_distancias = st.columns(2)

with col_fuerza:
    st.subheader("Resultados de Fuerza")
    st.info(f"Fuerza Neta sobre q{idx_analisis+1}:\n\n ${f_neta_mag:.2e}N$")
    
    if f_neta_mag > 0:
        angulo = math.degrees(math.atan2(fy_neta, fx_neta))
        if angulo < 0:
            angulo += 360
        st.write(f"Direccion: {angulo:.2f} grados")
        
    st.write(f"Componente $F_{{x}}$: ${fx_neta:.2e}N$")
    if modo == "2D":
        st.write(f"Componente $F_{{y}}$: ${fy_neta:.2e}N$")

with col_distancias:
    st.subheader("Distancias")
    for i, c in enumerate(cargas):
        if i != idx_analisis:
            dist = math.sqrt((c.x - carga_objetivo.x)**2 + (c.y - carga_objetivo.y)**2)
            st.write(f"De q{idx_analisis+1} a q{i+1}: {dist:.2f} m")

st.subheader("Resultados de Campo Electrico")
col_campo = st.columns(len(puntos_campo))

for i, (px, py, ex, ey, mag) in enumerate(datos_campo):
    with col_campo[i]:
        st.write(f"**Punto {i+1}:** Magnitud = ${mag:.2e} N/C$")
        st.write(f"Componente $E_{{x}}$: ${ex:.2e} N/C$")
        if modo == "2D":
            st.write(f"Componente $E_{{y}}$: ${ey:.2e} N/C$")
