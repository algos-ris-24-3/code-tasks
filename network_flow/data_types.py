from collections import namedtuple


NetworkCutData = namedtuple("NetworkCutData", "source_set sink_set capacity")
"""
Данные о разрезе сети.

:ivar source_set: Множество вершин, относящихся к источнику.
:type source_set: set[int]
:ivar sink_set: Множество вершин, относящихся к стоку.
:type sink_set: set[int]
:ivar capacity: Пропускная способность разреза.
:type capacity: int
"""

NetworkVerticesData = namedtuple("NetworkVerticesData", "sources sinks transits")
"""
Данные о вершинах сети.

:ivar sources: Список индексов вершин-источников.
:type sources: list[int]
:ivar sinks: Список индексов вершин-стоков.
:type sinks: list[int]
:ivar transits: Список индексов транзитных вершин.
:type transits: list[int]
"""
