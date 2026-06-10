-- =============================================================================
-- CONTROL DE VENTAS - Northwind (practica 5)
-- Consultas utiles para auditar totales y comprobar resultados
-- =============================================================================

-- A) Ventas totales por region (base del producto top)
SELECT
    er.RegionID,
    TRIM(r.RegionDescription) AS Region,
    SUM(od.Quantity * od.UnitPrice) AS Ventas_total,
    COUNT(DISTINCT od.OrderID) AS num_pedidos
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN (
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
GROUP BY er.RegionID, Region
ORDER BY RegionID;

-- B) Top 3 productos por region (comprobar que el #1 es el esperado)
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
HAVING Posicion <= 3
ORDER BY ventas.RegionID, Posicion, ventas.Producto;

-- C) Compras del producto top por cliente, anio y region (sin filtrar al maximo)
-- Util para ver empates antes del DENSE_RANK final.
