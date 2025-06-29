import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap_uso(vars, data):
    x = vars['x']
    DesksZ = vars['DesksZ']
    E = vars['E']
    D = vars['D']
    S = vars['S']
    DesksE = vars['DesksE']

    usage_matrix = pd.DataFrame(0, index=D, columns=S)
    for e in E:
        for d in DesksE[e]:
            for s in S:
                if x[e][d][s].varValue == 1:
                    usage_matrix.loc[d, s] += 1

    plt.figure(figsize=(12, 6))
    sns.heatmap(usage_matrix, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Empleados asignados'})
    plt.title("🔲 Uso de escritorios por día")
    plt.xlabel("Día")
    plt.ylabel("Escritorio")
    plt.tight_layout()
    plt.show()

def plot_asignaciones_gantt(vars, data):
    x = vars['x']
    DesksZ = vars['DesksZ']
    E = vars['E']
    D = vars['D']
    S = vars['S']
    DesksE = vars['DesksE']

    data_gantt = []
    for e in E:
        for s in S:
            for d in DesksE[e]:
                if x[e][d][s].varValue == 1:
                    zona = DesksZ.get(d, "N/A")
                    data_gantt.append({"Empleado": e, "Día": s, "Escritorio": d, "Zona": zona})

    df_gantt = pd.DataFrame(data_gantt)
    df_gantt["Empleado"] = pd.Categorical(df_gantt["Empleado"], categories=sorted(E), ordered=True)
    df_gantt["Día"] = pd.Categorical(df_gantt["Día"], categories=S, ordered=True)

    plt.figure(figsize=(12, len(E) * 0.4))
    sns.scatterplot(data=df_gantt, x="Día", y="Empleado", hue="Zona", style="Escritorio", s=100)
    plt.title("📅 Asignaciones por Empleado (día, escritorio y zona)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

