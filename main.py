import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

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

def resolver_ecuacion_simbolica(ecuacion):
    x, y = sp.symbols('x y')
    dx_dy = sp.sympify(ecuacion)
    sol = sp.integrate(dx_dy, x)
    return sol

def main():
    ecuacion = input("Ingrese la ecuación diferencial (dy/dx = f(x, y)): ")
    x, y = sp.symbols('x y')
    dx_dy = sp.sympify(ecuacion)
    if es_separable(ecuacion):
        print("La ecuación es separable.")
        sol = resolver_ecuacion_simbolica(ecuacion)
        print("La solución es: ", sol)
        # Pedimos los valores iniciales de x y y
        x0 = float(input("Ingrese el valor inicial de x: "))
        y0 = float(input("Ingrese el valor inicial de y: "))

            # Definimos la solución particular
        sol_particular = sp.Eq(sol, y)
        soluciones = sp.solve(sol_particular, y)

        if soluciones:
            sol_particular = soluciones[0]

            # Ajustamos la solución particular para que pase por el punto (x0, y0)
            ajuste = sol_particular.subs(x, x0) - y0
            sol_particular = sol_particular - ajuste

            # Generamos la gráfica de la solución particular
            x_valores = np.linspace(x0-10, x0+10, 10000)  # Aumentamos el número de puntos a 10000
            y_valores = []
            for x_valor in x_valores:
                y_valor = sol_particular.subs(x, x_valor)
                y_valores.append(y_valor)

            # Utilizamos una función de interpolación para suavizar la gráfica
            from scipy.interpolate import interp1d
            f = interp1d(x_valores, y_valores , kind='cubic')
            x_valores_suavizados = np.linspace(x0-10, x0+10, 1000)
            y_valores_suavizados = f(x_valores_suavizados)

            # Ajustamos la escala de la gráfica para que sea más similar a la de GeoGebra
            plt.plot(x_valores_suavizados, y_valores_suavizados)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Gráfica de la solución particular')
            plt.grid(True)
            plt.xlim(x0-5, x0+5)  # Ajustamos el límite inferior y superior del eje x
            plt.ylim(y0-2, y0+2)  # Ajustamos el límite inferior y superior del eje y
            plt.show()
        else:
            print("No se encontró ninguna solución particular.")
    else:
        print("La ecuación no es separable.")

if __name__ == "__main__":
    main()