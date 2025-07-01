from pulp import LpProblem, LpVariable, LpMaximize, lpSum, LpStatus, LpBinary

def solve_optimization(data):
    E = data['Employees']
    D = data['Desks']
    S = data['Days']
    G = data['Groups']
    Z = data['Zones']
    DesksZ_raw = data['Desks_Z']
    DesksE = data['Desks_E']
    EmployeesG = data['Employees_G']
    DaysE_orig = data['Days_E']

    total_slots = len(D) * len(S)
    min_required = 2 * len(E)
    max_extra = total_slots - min_required

    DesksZ = {}
    for zonadesk, desks in DesksZ_raw.items():
        for d in desks:
            DesksZ[d] = zonadesk

    model = LpProblem("Asignacion_Hibrida", LpMaximize)

    # Variables de decisión
    x = LpVariable.dicts("x", (E, D, S), cat=LpBinary) # Asignación de empleado e a escritorio d en día s
    z = LpVariable.dicts("z", (E, S), cat=LpBinary) # Empleado e está en la oficina en el día s
    y = LpVariable.dicts("y", (G, S), cat=LpBinary) # Grupo g se reúne en el día s
    w = LpVariable.dicts("w", (G, Z, S), cat=LpBinary) # Grupo g se reúne en zona z en día s
    u = LpVariable.dicts("u", (G, E, S), cat=LpBinary) # Empleado e del grupo g asiste a reunión en día s
    extra = LpVariable.dicts("extra", E, cat=LpBinary) # Días extra asignados a empleado e

    # Restricciones

    # 1. Un empleado solo puede ser asignado a escritorios permitidos.
    for e in E:
        for d in D:
            for s in S:
                if d not in DesksE[e]:
                    model += x[e][d][s] == 0

    # 2. Un empleado puede ser asignado a un máximo de un escritorio por día.
    for e in E:
        for s in S:
            model += lpSum(x[e][d][s] for d in D) <= 1

    # 3. Un escritorio puede ser asignado a un máximo de un empleado por día.
    for d in D:
        for s in S:
            model += lpSum(x[e][d][s] for e in E) <= 1

    # 4. Cada empleado debe asistir al menos 2 días a la oficina.
    # 5. Se puede asignar un máximo de 2 días extra por empleado.
    for e in E:
        model += lpSum(z[e][s] for s in S) >= 2
        model += lpSum(z[e][s] for s in S) <= 2 + extra[e]
    # Restricción para el número total de días extra.
    model += lpSum(extra[e] for e in E) <= max_extra

    # 6. Cada grupo debe tener exactamente una reunión.
    for g in G:
        model += lpSum(y[g][s] for s in S) == 1

    # 7. Relación entre la asignación de escritorios y las reuniones de grupo en zonas.
    for g in G:
        for s in S:
            for z_id in Z:
                empleados = EmployeesG[g]
                escritorios_en_zona = [d for d in D if DesksZ[d] == z_id]
                model += lpSum(x[e][d][s] for e in empleados for d in escritorios_en_zona) <= len(escritorios_en_zona) * w[g][z_id][s]
                model += lpSum(x[e][d][s] for e in empleados for d in escritorios_en_zona) >= w[g][z_id][s]

    # 8. Relación entre la asignación de escritorios y la presencia de empleados.
    for e in E:
        for s in S:
            model += lpSum(x[e][d][s] for d in D) == z[e][s]

    # 9. Relación entre asistencia a la oficina y asistencia a reuniones de grupo.
    for g in G:
        for s in S:
            for e in EmployeesG[g]:
                model += u[g][e][s] <= z[e][s]
                model += u[g][e][s] <= y[g][s]
                model += u[g][e][s] >= z[e][s] + y[g][s] - 1

    # Función Objetivo: Maximizar la satisfacción general.
    # Coeficientes
    alpha_orig = 2.0
    alpha_fill = 0.5
    beta = 1.2
    gamma = 0.5
    theta = 1.0
    bonus_weight = 0.1

    orig_term = lpSum(alpha_orig * z[e][s] for e in E for s in DaysE_orig[e])
    fill_term = lpSum(alpha_fill * z[e][s] for e in E for s in S if s not in DaysE_orig[e])
    meet_term = beta * lpSum(y[g][s] for g in G for s in S)
    cover_term = theta * lpSum(u[g][e][s] for g in G for e in EmployeesG[g] for s in S)
    zone_term = -gamma * lpSum(w[g][z_id][s] for g in G for z_id in Z for s in S)
    bonus_term = bonus_weight * lpSum(extra[e] for e in E)

    model += orig_term + fill_term + meet_term + cover_term + zone_term + bonus_term

    # Resolver el modelo
    model.solve()

    return model, {
        'x': x, 'z': z, 'y': y, 'w': w, 'u': u, 'extra': extra,
        'DesksZ': DesksZ,
        'E': E, 'D': D, 'S': S, 'G': G, 'Z': Z, 'DesksE': DesksE, 'EmployeesG': EmployeesG, 'DaysE_orig': DaysE_orig
    }

