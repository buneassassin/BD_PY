-- =============================================================================
-- PRACTICA 5 - Producto(s) con MAYOR venta por region (sin WITH)
-- Region via empleado del pedido. Venta linea = Quantity * UnitPrice
-- =============================================================================

SELECT
    p.RegionID,
    TRIM(r.RegionDescription) AS Region,
    p.Producto,
    p.Ventas
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
) AS p
INNER JOIN (
    SELECT RegionID, MAX(Ventas) AS Ventas_max
    FROM (
        SELECT
            er.RegionID,
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
    ) AS por_producto
    GROUP BY RegionID
) AS m ON p.RegionID = m.RegionID AND p.Ventas = m.Ventas_max
INNER JOIN region AS r ON p.RegionID = r.RegionID
ORDER BY p.RegionID, p.Producto;
