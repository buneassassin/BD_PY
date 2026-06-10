-- =============================================================================
-- VERIFICACION PASO A PASO (practica 5) - exportar a Excel
-- =============================================================================
-- Posicion = 1 en ranking_productos  ->  producto(s) top de la region.
-- Posicion = 1 en ranking_clientes   ->  cliente(s) top en (anio, region)
--   para el producto top de esa region.
-- =============================================================================

-- A) Ranking de productos por region (sin filtrar)
SELECT
    ventas.RegionID,
    TRIM(r.RegionDescription) AS Region,
    ventas.Producto,
    ventas.Ventas,
    DENSE_RANK() OVER (
        PARTITION BY ventas.RegionID
        ORDER BY ventas.Ventas DESC
    ) AS Posicion
FROM (
    SELECT
        er.RegionID,
        p.ProductName AS Producto,
        SUM(od.Quantity * od.UnitPrice) AS Ventas
    FROM `order details` AS od
    INNER JOIN orders AS o ON od.OrderID = o.OrderID
    INNER JOIN products AS p ON od.ProductID = p.ProductID
    INNER JOIN (
        SELECT DISTINCT et.EmployeeID, t.RegionID
        FROM employeeterritories AS et
        INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
    ) AS er ON o.EmployeeID = er.EmployeeID
    WHERE o.OrderDate IS NOT NULL
    GROUP BY er.RegionID, p.ProductName
) AS ventas
INNER JOIN region AS r ON ventas.RegionID = r.RegionID
ORDER BY ventas.RegionID, Posicion, ventas.Ventas DESC, ventas.Producto;

-- B) Ranking de clientes por anio y region (solo producto top de la region)
-- (misma logica que CONSULTA_RANKING_CLIENTES en consultas.py)

-- C) Comprobacion rapida del producto top por region:
-- SELECT RegionID, Producto, Ventas FROM (... ranking ...) WHERE Posicion = 1;
