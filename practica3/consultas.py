"""
Hay DOS consultas distintas:
  1) CONSULTA_SQL  -> MySQL hace SUM
  2) CONSULTA_PY   -> trae fila por fila SIN agrupar (Python hará la suma)
"""

CONSULTA_SQL = """
SELECT
    ta.au_id,
    SUM(s.qty * t.price * ta.royaltyper / 100.0) AS Ganancia
FROM titleauthor AS ta
INNER JOIN titles AS t ON ta.title_id = t.title_id
INNER JOIN sales AS s ON s.title_id = t.title_id
GROUP BY ta.au_id
ORDER BY Ganancia DESC
"""

CONSULTA_PY = """
SELECT
    ta.au_id,
    ta.title_id,
    ta.royaltyper,
    t.price,
    s.ord_num,
    s.qty
FROM titleauthor AS ta
INNER JOIN titles AS t ON ta.title_id = t.title_id
INNER JOIN sales AS s ON s.title_id = t.title_id
ORDER BY ta.au_id, s.ord_num
"""
