-- =============================================================================
-- PRACTICA 4 (Python + SQL) - Northwind
-- Producto(s) con MAYOR ganancia por anio y region (4 regiones)
--
-- Base identica a ProductosMenosVendidos.sql, pero:
--   - Aqui: MAX(Ganancia)  |  ProductosMenosVendidos.sql: MIN(Ganancia)
--   - Empates: GROUP_CONCAT de todos los productos con la misma ganancia extrema
--
-- Region: employeeterritories -> territories -> region (via orders.EmployeeID)
-- Ganancia linea: Quantity * UnitPrice
-- =============================================================================

-- Detalle: todos los productos empatados en el maximo
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
    ) AS por_producto
    GROUP BY Anio, RegionID
) AS m ON p.Anio = m.Anio
    AND p.RegionID = m.RegionID
    AND p.Ganancia = m.Ganancia_max
ORDER BY p.Anio, p.RegionID, p.Producto;

-- Vista pivote con empates (1 fila por anio, 4 columnas de region)
SELECT
    Anio,
    MAX(CASE WHEN RegionID = 1 THEN Producto_Info END) AS Eastern,
    MAX(CASE WHEN RegionID = 2 THEN Producto_Info END) AS Westerns,
    MAX(CASE WHEN RegionID = 3 THEN Producto_Info END) AS Northern,
    MAX(CASE WHEN RegionID = 4 THEN Producto_Info END) AS Southern
FROM (
    SELECT
        Anio,
        RegionID,
        CONCAT(
            GROUP_CONCAT(Producto ORDER BY Producto SEPARATOR ', '),
            ' (',
            Ganancia,
            ')'
        ) AS Producto_Info
    FROM (
        SELECT
            Anio,
            RegionID,
            Producto,
            Ganancia,
            DENSE_RANK() OVER (
                PARTITION BY Anio, RegionID
                ORDER BY Ganancia DESC
            ) AS dr
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
        ) AS ventas
    ) AS ranking
    WHERE dr = 1
    GROUP BY Anio, RegionID, Ganancia
) AS empatados
GROUP BY Anio
ORDER BY Anio;
