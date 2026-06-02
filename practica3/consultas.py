"""
Consultas de la practica (solo titleauthor, titles, sales):

  1) CONSULTA_SQL       -> MySQL hace SUM (resultado principal)
  2) CONSULTA_PY        -> detalle fila a fila para Python
  3) CONSULTA_NO_REFLEJADAS     -> ventas sin autor en titleauthor
  4) CONSULTA_TOTAL_AUTORES        -> suma global con titleauthor
  5) CONSULTA_TOTAL_VENTAS         -> suma global solo sales + titles
  6) CONSULTA_ROYALTY_FALTANTE     -> detalle % editorial (royalty < 100)
  7) CONSULTA_TOTAL_SIN_AUTOR      -> suma ventas sin titleauthor
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

CONSULTA_NO_REFLEJADAS = """
SELECT
    s.title_id,
    SUM(s.qty * t.price) AS Ganancia
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
LEFT JOIN titleauthor AS ta ON ta.title_id = s.title_id
WHERE ta.title_id IS NULL
GROUP BY s.title_id
"""

CONSULTA_TOTAL_AUTORES = """
SELECT SUM(s.qty * t.price * ta.royaltyper / 100.0) AS Ganancia_autores
FROM titleauthor AS ta
INNER JOIN titles AS t ON ta.title_id = t.title_id
INNER JOIN sales AS s ON s.title_id = t.title_id
"""

CONSULTA_TOTAL_VENTAS = """
SELECT SUM(s.qty * t.price) AS Ganancia_ventas_general
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
"""

CONSULTA_TOTAL_SIN_AUTOR = """
SELECT SUM(s.qty * t.price) AS total_sin_autor
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
LEFT JOIN titleauthor AS ta ON ta.title_id = s.title_id
WHERE ta.title_id IS NULL
"""

CONSULTA_ROYALTY_FALTANTE = """
SELECT
    fal.title_id,
    SUM(s.qty * t.price) AS venta_bruta,
    fal.pct_autores,
    fal.pct_editorial,
    SUM(s.qty * t.price * fal.pct_editorial / 100.0) AS parte_editorial
FROM sales AS s
INNER JOIN titles AS t ON t.title_id = s.title_id
INNER JOIN (
    SELECT
        t.title_id,
        IFNULL(SUM(ta.royaltyper), 0) AS pct_autores,
        IFNULL(100 - SUM(ta.royaltyper), 100) AS pct_editorial
    FROM titles AS t
    LEFT JOIN titleauthor AS ta ON ta.title_id = t.title_id
    GROUP BY t.title_id
    HAVING pct_autores > 0 AND pct_autores < 100
) AS fal ON fal.title_id = s.title_id
GROUP BY fal.title_id, fal.pct_autores, fal.pct_editorial
ORDER BY fal.title_id
"""
