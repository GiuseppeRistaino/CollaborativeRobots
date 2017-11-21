import sympy as sy
import numpy as nmp

'''
Calcola la retta tengente a una data circonferenza
Si conoscono un punto della retta (x0, y0) e la posizione (xc, yc) e il raggio (r) della circonferenza.
Per il calcolo del coefficiente angolare si è utilizzata l'equazione del delta pari a zero dell'intersezione
della retta con la circonferenza.
l'equazione è la seguente:
2m^4*x0^2 + m^3 (y0*x0 - yc*x0) + m^2(y0*yc + x0*xc +x0^2 - xc + r^2) + m (yc*xc -y0 *xc +2x0y0-2x0yc) + 2y0yc-y0^2-yc^2+r^2=0
RETURN: coefficiente angolare della retta tangente
'''
def tangent_of_circle(x0, y0, xc, yc, r):
    m = sy.symbols('m', real=True)
    #poniamo il delta uguale a zero dopo aver svolto a mano il risultato del sistema tra la retta e la circonferenza
    eq_delta = (2 * m * y0 - 2 * xc - 2 * m ** 2 * x0 - 2 * m * yc) ** 2 - 4 * (1 + m ** 2) * (
    xc ** 2 + x0 ** 2 * m ** 2 + y0 ** 2 + yc ** 2 - 2 * m * y0 * x0 + 2 * m * yc * x0 - 2 * y0 * yc - r ** 2)
    #la seguente non restituisce le tangenti perpendicolari all'asse x
    result = []
    try:
        slopes = sy.solveset(eq_delta, m, domain=sy.S.Reals)
        #invece di trovare l'intersezione con il cerchio troviamo l'intersezione con la retta perpendicolare passante per il raggio
        #qui troviamo i punti di intersezione tra la retta con coefficiente angolare appena trovato e la retta perpendicolare a questa passante per il centro della circonferenza
        for slope in slopes:
            slope = float(sy.sympify(slope))
            x, y = sy.symbols('x y', real=True)
            #equazione della retta passante per il punto x0, y0 con coefficiente angolare "slope" -> y-y0 = m (x-x0)
            eq_line = y - slope * x + slope * x0 - y0
            #ora dobbiamo trovare la retta perpendicolare a questa
            #equazione della retta se slope è zero
            eq_line_r = x - xc
            if slope != 0:
                #equaione della retta se slope è diverso da zero
                eq_line_r = y - (-1 / slope) * x + (-1 / slope) * xc - yc
            info = sy.solve([eq_line, eq_line_r])
            #utilizziamo un dizionario per ordinare le informazioni della retta tangente alla circonferenza
            res = {}
            res['m'] = slope
            for key, value in info.items():
                if str(key) == 'x':
                    res['x'] = value
                elif str(key) == 'y':
                    res['y'] = value
            result.append(res)
        #verifica del'esistenza di tangenti perpendicolari all'asse x
        resX = tangent_x_circle(x0, xc, yc, r)
        if len(resX) == 1:  #vuol dire che vi è una tangente
            res = {}
            for value in resX:
                res['m'] = nmp.inf
                res['x'] = x0
                res['y'] = value
            result.append(res)
    except:
        print("NON RIESCO A RISOLVERE L'EQUAZIONE")
    return result

'''
Calcola i punti di intersezione tra una circonferenza e una retta perpendicolare all'asse x passante per x0.
xc, yc, r: centro della circonferenza e il raggio.
RETURN: la coordinata y del punto di intersezione
'''
def tangent_x_circle(x0, xc, yc, r):
    y = sy.symbols('y', real=True)
    eq_system = (x0-xc)**2+(y-yc)**2-r**2
    result = sy.solveset(eq_system, y)
    return result

'''
NON UTILIZZATA
Calcola i punti di intersezione tra una circonferenza e una retta che passa per il punto x0, y0.
x0Line, y0Line: punto della retta
xCircle, yCircle, ray: centro della circonferenza e il raggio.
RETURN: le coordinate x, y della intersezione della retta con la circonferenza
'''
def intersect_line_circle(mLine, x0Line, y0Line, xCircle, yCircle, ray):
    x, y = sy.symbols('x y', real = True)
    eq_line = y-mLine*x +mLine*x0Line -y0Line
    eq_circle = y**2 + x**2 -2*y*yCircle -2*x*xCircle -ray**2 +xCircle**2 +yCircle**2
    result = sy.solve([eq_line, eq_circle])
    return result

'''
Calcola il coefficiente angolare della retta passante per due punti.
x0, y0, x1, y1: coordinate dei due punti per cui passa la retta.
RETURN: Coefficiente angolare della retta
'''
def line_slope(x0, y0, x1, y1):
    if x1 - x0 == 0:    #controllo del campo di esistenza
        x0, x1 = sy.symbols('x0 x1')
        f = (y1-y0)/(x1-x0)
        return sy.limit(f, x1, x0)
    return (y1-y0)/(x1-x0)

'''
funzione per il caloclo del punto di intersezione tra una retta passante per il punto x0, y0 con coefficiente
angolare m e la retta perpendicolare a questa passante per il punto xc, yc
RETURN: coordinate del punto di intersezione in una lista (result) di dizionario
'''
def intersect_line_line_inc(m, x0, y0, xc, yc):
    x, y = sy.symbols('x y', real=True)
    eq_line = None
    eq_line_r = None
    if m != 0 and str(m) != 'inf' and str(m) != '-inf':
        eq_line = y - m * x + m * x0 - y0
        eq_line_r = y - (-1 / m) * x + (-1 / m) * xc - yc
    elif str(m) == 'inf' or str(m) == '-inf':
        eq_line = x - x0
        eq_line_r = y - yc
    elif m == 0:
        eq_line = y - m * x + m * x0 - y0
        eq_line_r = x - xc
    result = sy.solve([eq_line, eq_line_r])
    return result

'''
funzione per il calcolo della lunghezza dell'arco di circonferenza.
x0c: è la cordinata x del punto sulla circonferenza da cui parte l'arco.
y0c: è la cordinata y del punto sulla circonferenza da cui parte l'arco.
x1c: è la cordinata x del punto sulla circonferenza a cui arriva l'arco.
y1c: è la cordinata y del punto sulla circonferenza a cui arriva l'arco.
r: raggio della circonferenza
RETURN: lunghezza dell'arco di circonferenza
'''
def bow_circumference(x0c, y0c, x1c, y1c, r):
    p1 = sy.Point(x0c, y0c)
    p2 = sy.Point(x1c, y1c)
    cat = p1.distance(p2)
    ipo = 2 * r
    sin_alfa = float(cat/ipo)
    if sin_alfa > 1:
        sin_alfa = 1
    bow = 2 * nmp.arcsin(sin_alfa) * r
    return bow
