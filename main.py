import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def es_separable(ecuacion):
    x, y = sp.symbols('x y')
    dx_dy = sp.sympify(ecuacion)

    # Verificamos si la ecuación se puede separar en dos partes
    f_x = dx_dy.as_independent(x)[0]
    g_y = dx_dy.as_independent(y)[0]

    # Verificamos si f_x y g_y son funciones de una variable cada una
    if f_x.has(x) and not f_x.has(y) and g_y.has(y) and not g_y.has(x):
        return True

    # Verificamos si la ecuación se puede escribir en la forma dx/dy = f(x) * g(y)
    if dx_dy.is_Mul:
        factors = dx_dy.args
        for f in factors:
            if f.has(x) and not f.has(y):
                f_x = f
            elif f.has(y) and not f.has(x):
                g_y = f
        if f_x and g_y:
            return True

    # Verificamos si la ecuación se puede escribir en la forma dx/dy = 1 / (f(x) * g(y))
    if dx_dy.is_Pow and dx_dy.exp == -1:
        base = dx_dy.base
        if base.is_Mul:
            factors = base.args
            for f in factors:
                if f.has(x) and not f.has(y):
                    f_x = f
                elif f.has(y) and not f.has(x):
                    g_y = f
            if f_x and g_y:
                return True

    # Verificamos si la ecuación se puede escribir en la forma dx/dy = f(x) ** g(y)
    if dx_dy.is_Pow:
        base, exponente = dx_dy.args
        if base.has(x) and not base.has(y) and exponente.has(y) and not exponente.has(x):
            return True

    # Verificamos si la ecuación se puede escribir en la forma dx/dy = f(y) ** g(x)
    if dx_dy.is_Pow:
        base, exponente = dx_dy.args
        if base.has(y) and not base.has(x) and exponente.has(x) and not exponente.has(y):
            return True

    # Verificamos si la ecuación se puede separar utilizando la función `separatevars`
    result = sp.separatevars(dx_dy, dict=True)
    if result is not None:
        for var, expr in result.items():
            if var == x:
                f_x = expr
            elif var == y:
                g_y = expr
        if f_x and g_y:
            return True

    return False
def resolver_ecuacion(ecuacion, x0, y0, h, n):
    x = np.zeros(n+1)
    y = np.zeros(n+1)
    x[0] = x0
    y[0] = y0

    for i in range(n):
        k1 = eval(ecuacion.replace('x', str(x[i])).replace('y', str(y[i])))
        k2 = eval(ecuacion.replace('x', str(x[i] + h*0.5)).replace('y', str(y[i] + h*k1*0.5)))
        k3 = eval(ecuacion.replace('x', str(x[i] + h*0.5)).replace('y', str(y[i] + h*k2*0.5)))
        k4 = eval(ecuacion.replace('x', str(x[i] + h)).replace('y', str(y[i] + h*k3)))

        y[i+1] = y[i] + (h/6)*(k1 + (2*k2) + (2*k3) + k4)
        x[i+1] = x[i] + h

    return x, y
def graficar_resultado(x, y):
    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfica de la ecuación diferencial')
    plt.grid(True)
    plt.show()

def main():
    ecuacion = input("Ingrese la ecuación diferencial (y' = f(x, y)): ")
    if es_separable(ecuacion):
        print("La ecuación es separable.")
        x0 = float(input("Ingrese el valor inicial de x: "))
        y0 = float(input("Ingrese el valor inicial de y: "))
        h = float(input("Ingrese el paso (h): "))
        n = int(input("Ingrese el número de iteraciones (n): "))
        x, y = resolver_ecuacion(ecuacion, x0, y0, h, n)
        print("x =", x)
        print("y =", y)
        graficar_resultado(x, y)  # <--- Agregamos la llamada a la función graficar_resultado
    else:
        print("La ecuación no es separable.")

if __name__ == "__main__":
    main()