# [Simulador de cargas eléctricas, fuerza eléctrica y campo eléctrico]

**Integrantes del Equipo:**
- Hernández Campos Diego Ronaldo
- Islas Granillo Jose Ernesto
- Montiel Espinosa Hugo Santiago

## Descripción breve del simulador
Aplicación web interactiva desarrollada para simular sistemas de cargas eléctricas puntuales en una (1D) y dos (2D) dimensiones. El simulador permite a los usuarios definir múltiples cargas (indicando su magnitud y posición) y calcula de manera automatizada la fuerza eléctrica entre pares de cargas, la fuerza neta resultante sobre una carga específica mediante el principio de superposición, y el campo eléctrico en coordenadas puntuales o en todo el espacio evaluado a través de un mapa vectorial. El proyecto integra un entorno gráfico en tiempo real que facilita la visualización e interpretación física de los resultados matemáticos.

## Lenguaje y librerías utilizadas
El núcleo lógico e interactivo del simulador está construido íntegramente en **Python 3**. Se implementaron las siguientes librerías para cubrir los requerimientos matemáticos y de interfaz:
- **Streamlit:** Utilizada para construir la interfaz gráfica de usuario (GUI) interactiva en formato de aplicación web, gestionando el panel lateral de variables y la actualización de los resultados en tiempo real.
- **NumPy:** Empleada para el manejo eficiente de arreglos multidimensionales y la generación de mallas espaciales (grids) requeridas para renderizar el mapa de campo vectorial continuo.
- **Matplotlib:** Responsable de la creación del plano cartesiano dinámico, dibujando las cargas eléctricas, trazando los vectores directores (fuerzas y campos) y proyectando los componentes ortogonales.
- **Math:** Librería estándar empleada para las operaciones trigonométricas fundamentales, obtención de distancias euclidianas y cálculos de ángulos vectoriales.

## Instrucciones para instalar y ejecutar
1. Asegúrese de tener **Python 3.8 o superior** instalado en su sistema operativo.
2. Abra una terminal de comandos (Símbolo del sistema, PowerShell o terminal de Linux/macOS).
3. Instale las dependencias necesarias ejecutando:
   `pip install streamlit numpy matplotlib`
4. Navegue en la terminal hasta el directorio donde se encuentra guardado el archivo del código fuente (`simulador_cargas.py`).
5. Inicie el servidor local del simulador con el siguiente comando:
   `python -m streamlit run simulador_cargas.py`
6. El programa se ejecutará y abrirá automáticamente una pestaña en su navegador web predeterminado.

## Ejemplos de uso
Para verificar el correcto funcionamiento del modelo físico, el sistema puede evaluarse mediante los siguientes tres casos de prueba principales:
- **Caso 1D:** Seleccionar el espacio "1D" en el panel. Ingresar dos cargas colineales (por ejemplo, $1\times10^{-6}C$ en la posición $x=-2$, y $-1\times10^{-6}C$ en $x=2$). Al analizar la primera carga, se visualizará un vector de fuerza de atracción puramente horizontal, suprimiendo la necesidad de analizar el eje Y.
- **Caso 2D:** Seleccionar el espacio "2D". Definir tres cargas formando un triángulo en el plano (por ejemplo: $q_{1}$ en el origen, $q_{2}$ sobre el eje X y $q_{3}$ en el eje Y). El programa descompondrá matemáticamente las fuerzas individuales que actúan sobre la carga objetivo para mostrar el vector de fuerza neta resultante y sus proyecciones.
- **Caso de Campo Eléctrico:** Mientras se evalúa un sistema de cargas, dirigirse a la sección "Puntos de Campo Eléctrico" y definir 3 coordenadas distintas en el espacio vacío (por ejemplo, $(1,1)$, $(-2,3)$, $(4,0)$). El sistema calculará la magnitud exacta en esas coordenadas e ilustrará un vector magenta que indicará la dirección y sentido de la línea de campo en ese instante espaciotemporal.

## Explicación breve de los cálculos implementados
El motor de cálculo del programa se cimienta en los siguientes principios de la Mecánica y el Electromagnetismo:
- **Ley de Coulomb:** La magnitud de la interacción electrostática entre cada par de cargas se determina utilizando la fórmula $F=k|q_{1}q_{2}|/r^{2}$, utilizando la constante $k=8.99\times10^{9}N\cdot m^{2}/C^{2}$ y calculando $r$ como la distancia euclidiana entre ambas partículas.
- **Principio de Superposición y Fuerza Neta:** Para hallar la fuerza total sobre una partícula objetivo, se suman vectorialmente las contribuciones de todas las demás cargas: $\vec{F}_{neta}=\sum_{i}\vec{F}_{i}$. Para lograrlo programáticamente, la fuerza individual se divide en componentes ortogonales usando trigonometría ($F_{x}=F\cos(\theta)$ y $F_{y}=F\sin(\theta)$) y se suman independientemente antes de recombinarse en la magnitud final.
- **Campo Eléctrico:** La contribución escalar al campo eléctrico provista por cada carga en un punto específico se obtiene con $E=k|q|/r^{2}$. El campo vectorial total sobre la coordenada dada es $\vec{E}_{total}=\sum_{i}\vec{E}_{i}$, obedeciendo que el campo emerge radiando de las cargas positivas y converge hacia las negativas. Se incorporaron validaciones matemáticas para evitar divisiones entre cero ($r=0$) y atenuar imprecisiones de punto flotante subatómicas.

## Capturas y descripción de las visualizaciones
*(Reemplace este texto por imágenes o capturas de pantalla de su simulador funcionando)*

El entorno gráfico del simulador emplea la siguiente convención visual para interpretar los datos:
- **Cargas Eléctricas:** Esferas color rojo para denotar cargas positivas (+), esferas color azul para cargas negativas (-), y color gris para cargas neutras ($0C$).
- **Fuerza Neta:** Representada por un vector verde oscuro anclado a la carga analizada. 
- **Componentes Vectoriales de Fuerza:** Líneas discontinuas en naranja (eje X) y morado (eje Y) que demuestran la descomposición rectangular de la fuerza neta.
- **Vectores de Campo Eléctrico Puntuales:** Representados por cruces ('x') negras que denotan el punto a evaluar, de los cuales surge un vector color magenta que señala la dirección de las líneas de campo. Sus proyecciones rectangulares se muestran con líneas punteadas celestes y rosas.
- **Mapa Vectorial General:** Fondo cuadriculado compuesto por flechas grises semitransparentes que demuestran el comportamiento topológico y el "flujo" del campo electromagnético en todo el espacio del plano cartesiano circundante.