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

    x = LpVariable.dicts("x", (E, D, S), cat=LpBinary)
    z = LpVariable.dicts("z", (E, S), cat=LpBinary)
    y = LpVariable.dicts("y", (G, S), cat=LpBinary)
    w = LpVariable.dicts("w", (G, Z, S), cat=LpBinary)
    u = LpVariable.dicts("u", (G, E, S), cat=LpBinary)
    extra = LpVariable.dicts("extra", E, cat=LpBinary)

    for e in E:
        for d in D:
            for s in S:
                if d not in DesksE[e]:
                    model += x[e][d][s] == 0

    for e in E:
        for s in S:
            model += lpSum(x[e][d][s] for d in D) <= 1

    for d in D:
        for s in S:
            model += lpSum(x[e][d][s] for e in E) <= 1

    for e in E:
        model += lpSum(z[e][s] for s in S) >= 2
        model += lpSum(z[e][s] for s in S) <= 2 + extra[e]
    model += lpSum(extra[e] for e in E) <= max_extra

    for g in G:
        model += lpSum(y[g][s] for s in S) == 1

    for g in G:
        for s in S:
            for z_id in Z:
                empleados = EmployeesG[g]
                escritorios_en_zona = [d for d in D if DesksZ[d] == z_id]
                model += lpSum(x[e][d][s] for e in empleados for d in escritorios_en_zona) <= len(escritorios_en_zona) * w[g][z_id][s]
                model += lpSum(x[e][d][s] for e in empleados for d in escritorios_en_zona) >= w[g][z_id][s]

    for e in E:
        for s in S:
            model += lpSum(x[e][d][s] for d in D) == z[e][s]

    for g in G:
        for s in S:
            for e in EmployeesG[g]:
                model += u[g][e][s] <= z[e][s]
                model += u[g][e][s] <= y[g][s]
                model += u[g][e][s] >= z[e][s] + y[g][s] - 1

    alpha_orig = 2.0
    alpha_fill = 0.5
    beta = 1.2
    gamma = 0.5
    theta = 1.0

    orig_term = lpSum(alpha_orig * z[e][s] for e in E for s in DaysE_orig[e])
    fill_term = lpSum(alpha_fill * z[e][s] for e in E for s in S if s not in DaysE_orig[e])
    meet_term = beta * lpSum(y[g][s] for g in G for s in S)
    cover_term = theta * lpSum(u[g][e][s] for g in G for e in EmployeesG[g] for s in S)
    zone_term = -gamma * lpSum(w[g][z_id][s] for g in G for z_id in Z for s in S)
    bonus_term = 0.1 * lpSum(extra[e] for e in E)

    model += orig_term + fill_term + meet_term + cover_term + zone_term + bonus_term

    model.solve()

    return model, {
        'x': x, 'z': z, 'y': y, 'w': w, 'u': u, 'extra': extra,
        'DesksZ': DesksZ,
        'E': E, 'D': D, 'S': S, 'G': G, 'Z': Z, 'DesksE': DesksE, 'EmployeesG': EmployeesG, 'DaysE_orig': DaysE_orig
    }

