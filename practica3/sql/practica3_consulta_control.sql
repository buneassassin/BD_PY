-- La suma de ganancia_linea por au_id debe coincidir con Ganancia en practica3_ganancias_por_autor.sql

SELECT
    ta.au_id,
    s.ord_num,
    s.title_id,
    s.qty,
    t.price,
    ta.royaltyper,
    ROUND(s.qty * t.price * ta.royaltyper / 100.0, 4) AS ganancia_linea
FROM titleauthor AS ta
INNER JOIN titles AS t ON ta.title_id = t.title_id
INNER JOIN sales AS s ON s.title_id = t.title_id
ORDER BY ta.au_id, s.ord_num;
