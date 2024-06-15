# Lester Noé Duarte Nolasco
# 0909-21-18812


import matplotlib.pyplot as plt
import numpy as np

# Función para ampliar el numerador del polinomio L_i(x)
def ampliarNumerador(puntos, i):
    n = len(puntos)
    coeficienteVariable = np.zeros(n)
    coeficienteVariable[0] = 1  # Inicializa el primer coeficiente en 1

    # Construye el numerador expandiendo el producto (x - x_j)
    for j in range(n):
        if i != j:
            for k in range(n-1, 0, -1):
                coeficienteVariable[k] = coeficienteVariable[k] * -puntos[j][0] + (coeficienteVariable[k-1] if k > 0 else 0)
            coeficienteVariable[0] *= -puntos[j][0]

    # se crea una lista de términos de ceros del numerador
    respuestaAmpliada = []
    for k in range(n-1, -1, -1):
        if coeficienteVariable[k] != 0:
            respuestaAmpliada.append(f"{coeficienteVariable[k]:.1f}x^{k}")

    return " + ".join(respuestaAmpliada)  # Retorna el numerador como una cadena de texto

# Función para escalar el numerador del polinomio L_i(x) por el denominador
def numeradorEscalador(numerador_expandido, denominador):
    terminos = numerador_expandido.split(" + ")  # O sea Separa los términos del numerador
    escalado = []

    # Escala cada término del numerador por el denominador
    for termino in terminos:
        if "x^" in termino:
            coef = float(termino.split("x^")[0].strip())  #Aca Extrae el coeficiente
            potencia = int(termino.split("x^")[1])  #Aca Extrae la potencia de x
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}x^{potencia}")
        else:
            coef = float(termino.split("x")[0].strip())  #Aca Extrae el coeficiente
            escalado.append(f"(1 / {denominador:.1f}) * {coef:.1f}")

    return " + ".join(escalado)  #Aca se Retorna el numerador escalado como una cadena de texto

#Esta es la Función para realizar la interpolación de Lagrange
def lagrange_interpolation(puntos_x, puntos_y):
    def L(k, x):
        termino = 1
        for i in range(len(puntos_x)):
            if i != k:
                termino *= (x - puntos_x[i]) / (puntos_x[k] - puntos_x[i])
        return termino

    def P(x):
        polinomio = 0
        for k in range(len(puntos_x)):
            polinomio += puntos_y[k] * L(k, x)
        return polinomio

    valores_x = np.linspace(min(puntos_x) - 1, max(puntos_x) + 1, 1000)  # Son los Valores de x para graficar
    valores_y = [P(x) for x in valores_x]  # Evalúa P(x) para cada valor de x osea para y o f(x)

    return P, valores_x, valores_y  # Retorna la función P(x) y los valores calculados por el programa

# Función para imprimir las iteraciones individuales de Lagrange 
def imprimir_polinomios(puntos_x, puntos_y):
    n = len(puntos_x)
    puntos = list(zip(puntos_x, puntos_y))  # Crea una lista de puntos (x, y)

    P_str = "Polinomios individuales L_i(x):\n"
    for i in range(n):
        numerador, denominador = ampliarNumerador(puntos, i), 1  # Expande el numerador y calcula el denominador
        for j in range(n):
            if j != i:
                denominador *= (puntos_x[i] - puntos_x[j])  # Calcula el denominador del polinomio L_i(x)
        numerador_escalado = numeradorEscalador(numerador, denominador)  # Escala el numerador por el denominador

        if i > 0:
            P_str += "\n"
        P_str += f"L{i}(x):\n"
        P_str += f"L{i}(x) = ({numerador}) / ({denominador})\n"  # Se Muestra el polinomio L_i(x)
        P_str += f"L{i}(x) = {numerador_escalado}\n"  # Se Muestra el polinomio L_i(x) escalado

    print(P_str)  # SeImprime todos los polinomios individuales L_i(x) O sea las iteraciones

def main():
    num_puntos = int(input("Ingresa la cantidad de puntos (3 o 4): "))  # Se Ingresa la cantidad de puntos a interpolar yo solo defini 3 o 4
    puntos_x = []
    puntos_y = []

    print("Ingresa los puntos (x, y) uno por uno:")
    for i in range(num_puntos):
        x = float(input(f"Punto {i + 1} - x: "))  # Se Ingresa el valor de x
        y = float(input(f"Punto {i + 1} - y: "))  # Se Ingresa el valor de y
        puntos_x.append(x)  # Se Agrega x a la lista de puntos_x
        puntos_y.append(y)  # Se Agrega y a la lista de puntos_y

    print("\nPolinomios de Lagrange:")
    for i in range(num_puntos):
        print(f"I[{i}]: ({puntos_x[i]}, {puntos_y[i]})")  # Muestra los puntos ingresados

    # Interpolación de Lagrange
    P, valores_x, valores_y = lagrange_interpolation(puntos_x, puntos_y)

    # Imprimir polinomios individuales de Lagrange
    imprimir_polinomios(puntos_x, puntos_y)

    # Evaluación del polinomio en puntos específicos
    print("\nIngresa los valores de x donde quieres evaluar el polinomio (separados por espacios):")
    valores_x_evaluados = list(map(float, input().split()))  # Valores de x para evaluar P(x)
    valores_y_evaluados = [P(x) for x in valores_x_evaluados]  # Evalúa P(x) para cada valor de x

    print("\nValores de P(x) para los puntos evaluados:")
    for x, y in zip(valores_x_evaluados, valores_y_evaluados):
        print(f"P({x:.1f}) = {y:.6f}")  # Imprime el resultado de P(x)

    # Graficar los resultados
    plt.figure(figsize=(10, 6))
    plt.plot(valores_x, valores_y, label='Polinomio Interpolante')  # Grafica el polinomio interpolante
    plt.scatter(puntos_x, puntos_y, color='red', s=100, label='Puntos de Datos')  # Grafica los puntos de datos
    plt.scatter(valores_x_evaluados, valores_y_evaluados, color='green', label='Puntos Evaluados')  # Grafica los puntos evaluados
    plt.axhline(0, color='black', linewidth=1.5)  # Línea horizontal en y=0 más oscura
    plt.axvline(0, color='black', linewidth=1.5)  # Línea vertical en x=0 más oscura
    plt.xlabel('x')  # La Etiqueta del eje x
    plt.ylabel('P(x)')  # La Etiqueta del eje y
    plt.legend()  # Muestra la leyenda
    plt.title('Polinomio de Interpolación de Lagrange')  # Se muestra el Título del gráfico
    plt.grid(True)  #Se Activa la cuadrícula en el gráfico
    plt.show()  # Se Muestra el gráfico

if __name__ == "__main__":
    main()  #Se Llama a la función principal al ejecutar el script