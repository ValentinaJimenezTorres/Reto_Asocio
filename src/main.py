import json
import os
from src.data.loader import load_instance
from src.optimizer.model.model import solve_optimization
from src.metrics.evaluation import evaluar_resultados
from src.visualization.plots import plot_heatmap_uso, plot_asignaciones_gantt

def main():
    instance_path = "data/instances/instance1.json"

    if not os.path.exists(instance_path):
        print(f"❌ No se encontró la instancia: {instance_path}")
        return

    print("📥 Cargando instancia...")
    data = load_instance(instance_path)

    print("⚙️ Resolviendo modelo de optimización...")
    model, variables = solve_optimization(data)

    print("📊 Evaluando resultados...")
    evaluar_resultados(variables, data)

    print("📈 Generando visualizaciones...")
    plot_heatmap_uso(variables, data)
    plot_asignaciones_gantt(variables, data)

if __name__ == '__main__':
    main()

