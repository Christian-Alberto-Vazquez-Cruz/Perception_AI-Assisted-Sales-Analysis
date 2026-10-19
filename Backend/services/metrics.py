import pandas as pd


def summarize(records):
    df = pd.DataFrame([r.model_dump() for r in records])
    df['fecha'] = pd.to_datetime(df.fecha)
    df['mes'] = df.fecha.dt.strftime('%Y-%m')
    df['dia_semana'] = df.fecha.dt.dayofweek
    months, categories = sorted(df.mes.unique()), sorted(df.categoria.unique())
    if len(months) > 60 or len(categories) > 30:
        raise ValueError('Máximo 60 meses y 30 categorías para mantener compacto el contexto.')
    sources = []

    def metric(identifier, title, data):
        sources.append({'id': identifier, 'title': title, 'kind': 'metric', 'data': data.copy() if isinstance(data, dict) else data})
        return identifier

    def change(current, previous):
        return round((current / previous - 1) * 100, 2) if previous else None

    def adjacent(a, b):
        return b is not None and pd.Period(a, 'M').ordinal - pd.Period(b, 'M').ordinal == 1

    monthly = []
    prev = None
    for month, group in df.groupby('mes', sort=True):
        row = {'mes': month, 'importe': round(float(group.importe.sum()), 2), 'unidades': int(group.unidades.sum()), 'dias_con_registros': int(group.fecha.nunique())}
        comparable = prev is not None and adjacent(month, prev['mes'])
        row['comparado_con'] = prev['mes'] if comparable else None
        for col in ['importe', 'unidades']:
            row[f'variacion_{col}_pct'] = change(row[col], prev[col]) if comparable else None
        row['source_id'] = metric(f'm-mes-{month}', f'Ventas de {month}', row)
        monthly.append(row)
        prev = row
    by_category = []
    for category, group in df.groupby('categoria', sort=True):
        row = {'categoria': category, 'importe': round(float(group.importe.sum()), 2), 'unidades': int(group.unidades.sum())}
        row['source_id'] = metric(f'm-cat-{len(by_category)}', f'Total categoría {category}', row)
        by_category.append(row)
    comparisons = []
    for i, month in enumerate(months):
        previous = months[i - 1] if i else None
        for j, category in enumerate(categories):
            current = df[(df.mes == month) & (df.categoria == category)]
            prior = df[(df.mes == previous) & (df.categoria == category)]
            amount = round(float(current.importe.sum()), 2) if len(current) else None
            before = round(float(prior.importe.sum()), 2) if len(prior) and adjacent(month, previous) else None
            units = int(current.unidades.sum()) if len(current) else None
            units_before = int(prior.unidades.sum()) if len(prior) and adjacent(month, previous) else None
            row = {'mes': month, 'categoria': category, 'importe': amount, 'unidades': units, 'comparado_con': previous if adjacent(month, previous) else None, 'importe_anterior': before, 'variacion_importe_pct': change(amount, before) if amount is not None and before is not None else None, 'variacion_unidades_pct': change(units, units_before) if units is not None and units_before is not None else None, 'diferencia_importe': round(amount - before, 2) if amount is not None and before is not None else None}
            row['source_id'] = metric(f'm-comparacion-{i}-{j}', f'{category} · {month}', row)
            comparisons.append(row)
    weekdays = []
    names = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    for day, group in df.groupby('dia_semana'):
        row = {'dia': names[day], 'importe': round(float(group.importe.sum()), 2), 'unidades': int(group.unidades.sum()), 'dias_con_registros': int(group.fecha.nunique()), 'promedio_importe_dia_observado': round(float(group.importe.sum() / group.fecha.nunique()), 2)}
        row['source_id'] = metric(f'm-dia-{day}', f'Ventas en {names[day]}', row)
        weekdays.append(row)
    daily = df.groupby('fecha')[['importe', 'unidades']].sum()
    peaks = [{'fecha': d.date().isoformat(), 'importe': round(float(r.importe), 2), 'unidades': int(r.unidades)} for d, r in daily.nlargest(3, 'importe').iterrows()]
    metric('m-picos', 'Tres mayores importes diarios observados', peaks)
    total = {'importe': round(float(df.importe.sum()), 2), 'unidades': int(df.unidades.sum()), 'registros': len(df), 'desde': df.fecha.min().date().isoformat(), 'hasta': df.fecha.max().date().isoformat()}
    metric('m-total', 'Totales y cobertura del dataset', total)
    patterns = [f"{r['mes']} {r['categoria']}: importe {r['variacion_importe_pct']}% frente a {r['comparado_con']}" for r in comparisons if r['variacion_importe_pct'] is not None and abs(r['variacion_importe_pct']) >= 5]
    return {'totals': total, 'monthly': monthly, 'categories': by_category, 'weekdays': weekdays, 'comparisons': comparisons, 'peaks': peaks, 'patterns': patterns, 'sources': sources, 'limitations': ['Ventas significa importe y unidades; no conocemos tickets, margen, inventario ni precios por producto.', 'Días y categorías sin registros son desconocidos, no ventas cero. No se garantiza que los meses estén completos.', 'Las variaciones comparan meses calendario consecutivos observados; base cero produce porcentaje nulo. Meses parciales no son directamente comparables.', 'Tendencia expresada como serie mensual y variaciones; picos son los tres días con mayor importe observado.']}
