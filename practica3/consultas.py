"""
Consultas de la practica (solo titleauthor, titles, sales):

  1) CONSULTA_SQL       -> MySQL hace SUM (resultado principal)
  2) CONSULTA_PY        -> detalle fila a fila para Python
  3) CONSULTA_EDITORIAL -> ventas en sales que el INNER JOIN no muestra
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

CONSULTA_EDITORIAL = """
SELECT
    s.title_id,
    SUM(s.qty * t.price) AS Ganancia
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
LEFT JOIN titleauthor AS ta ON ta.title_id = s.title_id
WHERE ta.title_id IS NULL
GROUP BY s.title_id
"""
