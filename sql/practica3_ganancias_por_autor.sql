-- Práctica 3 - Base de datos: tienda (Pubs)
-- Ganancias por autor (regalías sobre ventas reales)
--
-- Requisitos:
--   - Exactamente 3 tablas en el FROM (sin subconsultas, vistas ni procedimientos)
--   - Usa agregado SUM en la misma consulta
--
-- Fórmula por línea de venta:
--   ganancia = cantidad_vendida * precio_título * (royaltyper / 100)
--   royaltyper = % que le corresponde al autor en titleauthor

SELECT
    ta.au_id,
    ROUND(SUM(s.qty * t.price * ta.royaltyper / 100.0), 2) AS Ganancia
FROM titleauthor AS ta
INNER JOIN titles AS t
    ON ta.title_id = t.title_id
INNER JOIN sales AS s
    ON s.title_id = t.title_id
GROUP BY
    ta.au_id
ORDER BY
    Ganancia DESC;

-- Solo 3 tablas. El autor se identifica por au_id (titleauthor).
