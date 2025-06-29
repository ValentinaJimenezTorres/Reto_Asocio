def evaluar_resultados(vars, data):
    x = vars['x']
    z = vars['z']
    y = vars['y']
    w = vars['w']
    DesksZ = vars['DesksZ']
    E = vars['E']
    D = vars['D']
    S = vars['S']
    G = vars['G']
    Z = vars['Z']
    DesksE = vars['DesksE']
    EmployeesG = vars['EmployeesG']
    DaysE_orig = vars['DaysE_orig']

    preferidos_totales = 0
    asignaciones_totales = 0
    empleados_completamente_satisfechos = 0
    empleados_mismo_escritorio = 0
    grupos_con_unica_zona = 0
    uso_diario = {s: 0 for s in S}

    for e in E:
        dias_asignados = [s for s in S if z[e][s].varValue == 1]
        dias_preferidos = DaysE_orig[e]
        preferidos = [s for s in dias_asignados if s in dias_preferidos]
        preferidos_totales += len(preferidos)
        asignaciones_totales += len(dias_asignados)
        if set(dias_asignados).issubset(set(dias_preferidos)):
            empleados_completamente_satisfechos += 1

    for e in E:
        escritorios = set()
        for s in S:
            for d in D:
                if x[e][d][s].varValue == 1:
                    escritorios.add(d)
        if len(escritorios) == 1:
            empleados_mismo_escritorio += 1

    for s in S:
        for d in D:
            for e in E:
                if x[e][d][s].varValue == 1:
                    uso_diario[s] += 1

    for g in G:
        for s in S:
            if y[g][s].varValue == 1:
                zonas_activas = [z_id for z_id in Z if w[g][z_id][s].varValue == 1]
                if len(zonas_activas) == 1:
                    grupos_con_unica_zona += 1

    print(f"% días asignados preferidos: {100 * preferidos_totales / asignaciones_totales:.2f}%")
    print(f"% empleados con todos los días preferidos: {100 * empleados_completamente_satisfechos / len(E):.2f}%")
    print(f"% empleados con mismo escritorio todos los días: {100 * empleados_mismo_escritorio / len(E):.2f}%")
    promedio_uso = sum(uso_diario.values()) / len(S)
    print(f"Uso promedio de escritorios por día: {promedio_uso:.2f} escritorios")
    print(f"% reuniones de grupo con todos en una sola zona: {100 * grupos_con_unica_zona / len(G):.2f}%")
