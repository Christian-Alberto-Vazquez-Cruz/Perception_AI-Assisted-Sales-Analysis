import calendar
import json
import random
from datetime import date, timedelta
from pathlib import Path

from pydantic import TypeAdapter
from Backend.schemas.models import DatasetInput
from Backend.services.metrics import summarize


def main():
    rng = random.Random(20261019)
    categories = {
        'Bebidas': (55, 22.0),
        'Botanas': (38, 18.0),
        'Abarrotes': (30, 32.0),
        'Lácteos': (24, 28.0),
        'Limpieza': (12, 48.0),
        'Panadería': (45, 9.5),
    }
    demand = {
        'Bebidas': [0.90, 1.00, 1.03, 1.23, 1.12, 1.20],
        'Botanas': [0.98, 1.00, 0.66, 0.83, 1.00, 1.02],
        'Abarrotes': [0.97, 1.00, 1.01, 1.02, 1.02, 1.04],
        'Lácteos': [1.00, 1.00, 1.00, 1.01, 1.02, 1.02],
        'Limpieza': [0.95, 1.00, 1.04, 1.02, 1.08, 1.07],
        'Panadería': [0.98, 1.00, 1.00, 0.98, 1.02, 1.03],
    }
    rows = []
    day = date(2026, 1, 1)
    while day <= date(2026, 6, 30):
        month_end = calendar.monthrange(day.year, day.month)[1]
        payday = 1.15 if day.day in (14, 15, 16, month_end - 1, month_end) else 1.0
        traffic = rng.uniform(0.90, 1.10)
        event = 1.65 if day == date(2026, 5, 10) else 1.0
        for category, (base_units, base_price) in categories.items():
            weekend = (1.25 if category in ('Bebidas', 'Botanas') else 1.08) if day.weekday() >= 5 else 1.0
            units = max(1, round(base_units * demand[category][day.month - 1] * weekend * payday * traffic * event * rng.uniform(0.85, 1.15)))
            price_factor = 0.72 if category == 'Bebidas' and day.month == 4 else 1.0
            if category == 'Limpieza' and day.month >= 5:
                price_factor = 1.08
            unit_value = base_price * price_factor * rng.uniform(0.90, 1.10)
            rows.append({'fecha': day.isoformat(), 'categoria': category, 'unidades': units, 'importe': round(units * unit_value, 2)})
        day += timedelta(days=1)

    records = TypeAdapter(DatasetInput).validate_python(rows)
    summary = summarize(records)
    destination = Path(__file__).resolve().parent / 'ventas_realistas_2026.json'
    destination.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Archivo:', destination)
    print('Registros:', len(records), '| Días:', len({r.fecha for r in records}), '| Categorías:', len(categories))
    print('Unidades:', summary['totals']['unidades'], '| Importe:', summary['totals']['importe'])
    for row in summary['comparisons']:
        if (row['mes'], row['categoria']) in [('2026-03', 'Botanas'), ('2026-04', 'Bebidas')]:
            print(row['mes'], row['categoria'], '| Unidades:', row['variacion_unidades_pct'], '% | Importe:', row['variacion_importe_pct'], '%')


if __name__ == '__main__':
    main()
