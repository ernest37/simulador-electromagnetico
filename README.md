# Simulador de Cargas Eléctricas y Campo Electromagnético

**Integrantes del Equipo:**
- Hernández Campos Diego Ronaldo
- Islas Granillo Jose Ernesto
- Montiel Espinosa Hugo Santiago

## Acceso al Simulador en Línea
El simulador se encuentra desplegado en la nube utilizando Streamlit Community Cloud. Puede acceder a la versión completamente funcional sin necesidad de instalación a través del siguiente enlace:
🔗 **[Abrir Simulador Electromagnético](https://simulador-electromagnetico-proyectofisica.streamlit.app/)**

## Descripción breve del simulador
Aplicación web interactiva desarrollada para simular sistemas de cargas eléctricas puntuales en una (1D) y dos (2D) dimensiones. El simulador permite a los usuarios definir múltiples cargas (indicando su magnitud y posición) y calcula de manera automatizada la fuerza eléctrica entre pares de cargas, la fuerza neta resultante sobre una carga específica mediante el principio de superposición, y el campo eléctrico en coordenadas puntuales o en todo el espacio evaluado a través de un mapa vectorial interactivo.

## Lenguaje y librerías utilizadas
El núcleo lógico e interactivo del simulador está construido íntegramente en **Python 3**. Se implementaron las siguientes librerías para cubrir los requerimientos matemáticos y de interfaz:
- **Streamlit:** Utilizada para construir la interfaz gráfica de usuario (GUI) interactiva en formato de aplicación web, gestionando el panel lateral de variables y la actualización de los resultados en tiempo real.
- **NumPy:** Empleada para el manejo eficiente de arreglos multidimensionales y la generación de mallas espaciales (grids) requeridas para renderizar el mapa de campo vectorial continuo.
- **Matplotlib:** Responsable de la creación del plano cartesiano dinámico, dibujando las cargas eléctricas, trazando los vectores directores (fuerzas y campos) y proyectando los componentes ortogonales.
- **Math:** Librería estándar empleada para las operaciones trigonométricas fundamentales, obtención de distancias euclidianas y cálculos de ángulos vectoriales.

## Instrucciones para instalar y ejecutar (Uso Local)
Si desea ejecutar el código fuente en su propia máquina en lugar de usar la versión en línea:
1. Asegúrese de tener **Python 3.8 o superior** instalado en su sistema operativo.
2. Abra una terminal de comandos.
3. Instale las dependencias necesarias ejecutando:
   `pip install streamlit numpy matplotlib`
4. Navegue en la terminal hasta el directorio donde se encuentra guardado el archivo del código fuente (`simulador_cargas.py`).
5. Inicie el servidor local del simulador con el siguiente comando:
   `python -m streamlit run simulador_cargas.py`
6. El programa se ejecutará y abrirá automáticamente una pestaña en su navegador web predeterminado.

## Ejemplos de uso y Casos de Prueba
Para verificar el correcto funcionamiento del modelo físico, el sistema puede evaluarse mediante los siguientes tres casos de prueba:
- **Caso 1D:** Seleccionar el espacio "1D" en el panel. Ingresar dos cargas colineales (por ejemplo, $1\times10^{-6}C$ en la posición $x=-2$, y $-1\times10^{-6}C$ en $x=2$). Al analizar la primera carga, se visualizará un vector de fuerza de atracción puramente horizontal.
- **Caso 2D:** Seleccionar el espacio "2D". Definir tres cargas formando un triángulo en el plano (por ejemplo: $q_{1}$ en el origen, $q_{2}$ sobre el eje X y $q_{3}$ en el eje Y). El programa descompondrá matemáticamente las fuerzas individuales que actúan sobre la carga objetivo para mostrar el vector de fuerza neta resultante y sus proyecciones.
- **Caso de Campo Eléctrico:** Mientras se evalúa un sistema de cargas, dirigirse a la sección "Puntos de Campo Eléctrico" y definir 3 coordenadas distintas en el espacio vacío ( por ejemplo, $(1,1)$, $(-2,3)$, $(4,0)$ ). El sistema calculará la magnitud exacta en esas coordenadas e ilustrará un vector magenta que indicará la dirección y sentido de la línea de campo.

## Explicación breve de los cálculos implementados
El motor de cálculo del programa se cimienta en los siguientes principios:
- **Ley de Coulomb:** La magnitud de la interacción electrostática entre cada par de cargas se determina utilizando la fórmula $F=k\frac{|q_1q_2|}{r^2}$, utilizando la constante $k=8.99\times10^9N\cdot m^2/C^2$.
- **Principio de Superposición y Fuerza Neta:** Para hallar la fuerza total sobre una partícula objetivo, se suman vectorialmente las contribuciones de todas las demás cargas: $\vec{F}_{neta}=\Sigma\vec{F}_i$. Para lograrlo programáticamente, la fuerza individual se divide en componentes ortogonales ( $F_x=F\cos(\theta)$ y $F_y=F\sin(\theta)$ ). 
- **Campo Eléctrico:** La contribución al campo eléctrico provista por cada carga en un punto específico se obtiene con $E=k\frac{|q|}{r^2}$. El campo vectorial total sobre la coordenada dada es $\vec{E}_{total}=\sum\vec{E}_i$.

## Validaciones del Sistema
Para garantizar la integridad matemática de la simulación, el programa cuenta con validaciones internas:
- Bloqueo de entradas no numéricas en los campos de magnitud y posición.
- Prevención de superposición de cargas, arrojando una alerta visual y deteniendo la ejecución si el usuario intenta colocar dos partículas en la misma coordenada exacta.
- Prevención de división entre cero ($r=0$) al evitar calcular la fuerza de una carga sobre sí misma o al calcular el campo eléctrico exactamente en el centro de una partícula emisora.
- Filtrado de errores de precisión de punto flotante para resultados virtualmente nulos (magnitudes menores a $1\times10^{-12}$).

## Visualizaciones
El entorno gráfico del simulador emplea la siguiente convención visual interactiva, controlable desde el menú lateral de "Visualización":
- **Cargas Eléctricas:** Esferas color rojo para denotar cargas positivas (+) y color azul para cargas negativas (-). Las cargas de valor $0C$ se representan en gris.
- **Fuerza Neta:** Representada por un vector verde oscuro anclado a la carga analizada.
- **Componentes de Fuerza (Interactivo):** Líneas discontinuas en naranja ($F_{x}$) y morado ($F_{y}$) que demuestran la descomposición rectangular.
- **Vectores de Campo Eléctrico:** Representados por cruces ('x') negras de las cuales surge un vector magenta. Sus proyecciones se pueden visualizar de manera opcional con líneas punteadas (celeste para $E_{x}$ y rosa para $E_{y}$).
- **Mapa Vectorial General (Interactivo):** Fondo cuadriculado compuesto por flechas grises semitransparentes que demuestran la dirección del campo electromagnético en todo el plano cartesiano.
