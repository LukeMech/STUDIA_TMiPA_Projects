import sympy as sp
import numpy as np
import control as ctrl
from matplotlib.path import Path

def get_system_functions(k1, k2, k3):
    # Symbolika (SymPy)
    s = sp.symbols('s')
    G_s = 1 / (4*s + 1)
    Gr_s = 1 / s
    
    # Tor sprzezenia - H(s)
    H_wew = k1 * (Gr_s + k2)
    H_total = sp.simplify(k3 * H_wew)
    
    # Uklad otwarty L(s) i zamkniety G_cl(s)
    L_sym = sp.simplify(G_s * H_total)
    G_cl_sym = sp.simplify(G_s / (1 + G_s * H_total))

    # Numerycznie (Control)
    sn = ctrl.TransferFunction.s
    Gn = 1 / (4*sn + 1)
    Grn = 1 / sn
    Hn = k3 * k1 * (Grn + k2)
    G_cl_num = ctrl.feedback(Gn, Hn)
    L_num = Gn * Hn

    return {
        "G_s": G_s, "Gr_s": Gr_s, "G_cl_sym": G_cl_sym,
        "G_cl_num": G_cl_num, "L_num": L_num, "L_sym": L_sym,
        "H_s": H_total
    }

def get_characteristic_polynomial(G_cl_sym):
    """
    Extract characteristic polynomial coefficients from the closed-loop transfer function.
    :param G_cl_sym: Closed-loop transfer function (symbolic).
    :return: List of coefficients of the characteristic polynomial.
    """
    s = sp.symbols('s')
    char_poly = sp.Poly(G_cl_sym.as_numer_denom()[1], s)
    coefficients = char_poly.all_coeffs()

    return coefficients

def hurwitz_criterion(coefficients):
    """
    Check stability using Hurwitz criterion.
    coefficients: [a_n, a_{n-1}, ..., a_0] - od najwyższej potęgi s
    """
    # 1. Warunek konieczny: wszystkie współczynniki muszą być > 0
    if any(c <= 0 for c in coefficients):
        print("Błąd: Nie wszystkie współczynniki są dodatnie!")
        return False

    n_order = len(coefficients) - 1  # stopień wielomianu
    # Macierz Hurwitza jest kwadratowa o wymiarze n_order x n_order
    H = sp.zeros(n_order, n_order)

    # 2. Budowanie macierzy Hurwitza
    # Współczynniki: a_n, a_{n-1}, a_{n-2}, ...
    # Standardowa macierz Hurwitza (H):
    # [ a_{n-1}  a_{n-3}  a_{n-5} ... ]
    # [ a_n      a_{n-2}  a_{n-4} ... ]
    # [ 0        a_{n-1}  a_{n-3} ... ]
    # [ 0        a_n      a_{n-2} ... ]

    for i in range(n_order): # wiersze
        for j in range(n_order): # kolumny
            # Indeks współczynnika: 
            # Dla wierszy nieparzystych (0, 2, ...): (2*j + 1) - (i // 2) * 0? Nie.
            # Użyjemy prostszej logiki przesunięcia:
            idx = 2 * j - (i // 2) if i % 2 == 0 else 2 * j - (i // 2)
            
            # Formuła ogólna dla współczynnika a_{n - k}:
            k = (2 * j + 1 - i)
            
            if 0 <= k <= n_order:
                # coefficients[0] to a_n, coefficients[1] to a_{n-1}...
                # indeks w liście = k
                H[i, j] = coefficients[k]
            else:
                H[i, j] = 0

    # 3. Obliczanie minorów (determinant)
    determinants = []
    for i in range(1, n_order + 1):
        det = H[:i, :i].det()
        determinants.append(det)
    
    return all(d > 0 for d in determinants)


def is_point_outside_nyquist(L_num, point=(-1, 0)):
    """
    Check if a given point is outside the Nyquist plot enclosure.
    """
    # 1. Generate Nyquist data (returns a NyquistResponseData object)
    response_data = ctrl.nyquist_response(L_num)
    
    # 2. Access the complex values via the .response attribute
    # response_data.response contains the complex numbers for the contour
    complex_values = response_data.response.flatten()
    
    # 3. Extract real and imaginary parts from the complex array
    real_parts = complex_values.real
    imag_parts = complex_values.imag
    
    # 4. Create a path (polygon) and check for enclosure
    vertices = np.column_stack((real_parts, imag_parts))
    nyquist_path = Path(vertices)
    
    # contains_point returns True if the point is inside the loop
    is_inside = nyquist_path.contains_point(point)
    
    return not is_inside
