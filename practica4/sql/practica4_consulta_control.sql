-- =============================================================================
-- CONTROL DE VENTAS - Northwind (practica 4)
-- Consultas utiles para auditar totales antes y despues del MAX/MIN por region
-- =============================================================================

-- A) Ventas totales por anio (todas las regiones)
SELECT
    YEAR(o.OrderDate) AS Anio,
    SUM(od.Quantity * od.UnitPrice) AS Ventas_total,
    COUNT(DISTINCT od.OrderID) AS num_pedidos,
    COUNT(*) AS num_lineas
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN products AS p ON od.ProductID = p.ProductID
INNER JOIN (
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
GROUP BY Anio
ORDER BY Anio;

-- B) Ventas por anio y region (4 regiones)
SELECT
    YEAR(o.OrderDate) AS Anio,
    er.RegionID,
    TRIM(r.RegionDescription) AS Region,
    SUM(od.Quantity * od.UnitPrice) AS Ventas_total,
    COUNT(DISTINCT od.OrderID) AS num_pedidos
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN products AS p ON od.ProductID = p.ProductID
INNER JOIN (
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
GROUP BY Anio, er.RegionID, Region
ORDER BY Anio, RegionID;

-- C) Ganancia por producto, anio y region (base del ranking MAX/MIN)
SELECT
    YEAR(o.OrderDate) AS Anio,
    er.RegionID,
    TRIM(r.RegionDescription) AS Region,
    p.ProductName AS Producto,
    SUM(od.Quantity * od.UnitPrice) AS Ganancia,
    COUNT(*) AS num_lineas
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN products AS p ON od.ProductID = p.ProductID
INNER JOIN (
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
GROUP BY Anio, er.RegionID, Region, Producto
ORDER BY Anio, RegionID, Ganancia DESC, Producto;

-- D) Empates en el MAX (cambiar DESC por ASC para ver empates del MIN)
SELECT
    Anio,
    RegionID,
    Region,
    Ganancia,
    COUNT(*) AS num_productos,
    GROUP_CONCAT(Producto ORDER BY Producto SEPARATOR ', ') AS productos
FROM (
    SELECT
        p.Anio,
        p.RegionID,
        p.Region,
        p.Producto,
        p.Ganancia
    FROM (
        SELECT
            YEAR(o.OrderDate) AS Anio,
            er.RegionID,
            TRIM(r.RegionDescription) AS Region,
            p.ProductName AS Producto,
            SUM(od.Quantity * od.UnitPrice) AS Ganancia
        FROM `order details` AS od
        INNER JOIN orders AS o ON od.OrderID = o.OrderID
        INNER JOIN products AS p ON od.ProductID = p.ProductID
        INNER JOIN (
            SELECT DISTINCT et.EmployeeID, t.RegionID
            FROM employeeterritories AS et
            INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
        ) AS er ON o.EmployeeID = er.EmployeeID
        INNER JOIN region AS r ON er.RegionID = r.RegionID
        WHERE o.OrderDate IS NOT NULL
        GROUP BY Anio, er.RegionID, Region, Producto
    ) AS p
    INNER JOIN (
        SELECT Anio, RegionID, MAX(Ganancia) AS Ganancia_max
        FROM (
            SELECT
                YEAR(o.OrderDate) AS Anio,
                er.RegionID,
                p.ProductName AS Producto,
                SUM(od.Quantity * od.UnitPrice) AS Ganancia
            FROM `order details` AS od
            INNER JOIN orders AS o ON od.OrderID = o.OrderID
            INNER JOIN products AS p ON od.ProductID = p.ProductID
            INNER JOIN (
                SELECT DISTINCT et.EmployeeID, t.RegionID
                FROM employeeterritories AS et
                INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
            ) AS er ON o.EmployeeID = er.EmployeeID
            INNER JOIN region AS r ON er.RegionID = r.RegionID
            WHERE o.OrderDate IS NOT NULL
            GROUP BY Anio, er.RegionID, Producto
        ) AS x
        GROUP BY Anio, RegionID
    ) AS m ON p.Anio = m.Anio
        AND p.RegionID = m.RegionID
        AND p.Ganancia = m.Ganancia_max
) AS ganadores
GROUP BY Anio, RegionID, Region, Ganancia
HAVING COUNT(*) > 1
ORDER BY Anio, RegionID;
