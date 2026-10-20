# Моделирование полёта камня

Проект моделирует бросок камня под углом к горизонту в земном поле тяжести с заданной начальной скоростью.

## Запуск

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/main.py
```

## Сценарии

```
python3 src/main.py "Viscous: basic"
```

- `Viscous: basic`
- `Viscous: heavy stone`
- `Viscous: light stone`
- `Viscous: high speed`
- `Viscous: strong resistance`
- `Headon: basic`
- `Headon: heavy stone`
- `Headon: light stone`
- `Headon: vertical throw`
- `Headon: strong resistance`

## Управление

- `▶` — пуск / пауза.
- `■` — сброс.
- `F ~ v` и `F ~ v²` — смена модели сопротивления.

## Вклад участников

- **Кочетов Вячеслав:** физический движок симуляции, сценарии, сравнение численного и аналитического решения.
- **Горохов Глеб:** визуализация, отчёт по результатам моделирования.
