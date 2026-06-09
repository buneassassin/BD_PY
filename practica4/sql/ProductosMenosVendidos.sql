-- =============================================================================
-- PRODUCTOS MENOS VENDIDOS (solo SQL, sin Python) - Northwind
-- =============================================================================
-- Contexto: mismo enunciado que practica 4 pero buscando la MENOR ganancia
-- (Quantity * UnitPrice) por anio y por cada una de las 4 regiones:
--
--   1 Eastern   |  2 Westerns   |  3 Northern   |  4 Southern
--
-- Region del pedido = region del empleado que lo registro
--   orders.EmployeeID -> employeeterritories -> territories -> region
--
-- Archivos relacionados:
--   Northwind.sql                      -> script de la base de datos
--   practica4_max_producto_anio_region.sql -> misma logica con MAX + Python
--   practica4_consulta_control.sql     -> auditoria de ventas totales
-- =============================================================================


-- -----------------------------------------------------------------------------
-- PASO 0: Subconsulta reutilizable (empleado -> RegionID)
-- -----------------------------------------------------------------------------
SELECT DISTINCT
    et.EmployeeID,
    t.RegionID
FROM employeeterritories AS et
INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID;


-- -----------------------------------------------------------------------------
-- PASO 1: Ranking completo (todas las ganancias por anio, region y producto)
--         RN = 1 sera el producto con MENOR ganancia en ese anio/region
-- -----------------------------------------------------------------------------
SELECT
    YEAR(o.OrderDate) AS Anio,
    TRIM(r.RegionDescription) AS Region,
    er.RegionID,
    p.ProductName,
    SUM(od.Quantity * od.UnitPrice) AS GananciaTotal,
    ROW_NUMBER() OVER (
        PARTITION BY YEAR(o.OrderDate), er.RegionID
        ORDER BY SUM(od.Quantity * od.UnitPrice) ASC
    ) AS RN
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
GROUP BY Anio, er.RegionID, Region, p.ProductName
ORDER BY Anio DESC, RegionID, GananciaTotal ASC;


-- -----------------------------------------------------------------------------
-- PASO 2: Solo el minimo por anio/region (RN = 1, sin manejar empates)
-- -----------------------------------------------------------------------------
SELECT *
FROM (
    SELECT
        YEAR(o.OrderDate) AS Anio,
        TRIM(r.RegionDescription) AS Region,
        er.RegionID,
        p.ProductName,
        SUM(od.Quantity * od.UnitPrice) AS GananciaTotal,
        ROW_NUMBER() OVER (
            PARTITION BY YEAR(o.OrderDate), er.RegionID
            ORDER BY SUM(od.Quantity * od.UnitPrice) ASC
        ) AS RN
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
    GROUP BY Anio, er.RegionID, Region, p.ProductName
) AS ranked
WHERE RN = 1
ORDER BY Anio DESC, RegionID;


-- -----------------------------------------------------------------------------
-- PASO 3: CONSULTA PRINCIPAL (pivote + empates)
--         1 fila por anio, 4 columnas (Eastern, Westerns, Northern, Southern)
--         Si varios productos empatan en el minimo, se listan con GROUP_CONCAT
-- -----------------------------------------------------------------------------
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
            GROUP_CONCAT(ProductName ORDER BY ProductName SEPARATOR ', '),
            ' (',
            GananciaTotal,
            ')'
        ) AS Producto_Info
    FROM (
        SELECT
            Anio,
            RegionID,
            ProductName,
            GananciaTotal,
            DENSE_RANK() OVER (
                PARTITION BY Anio, RegionID
                ORDER BY GananciaTotal ASC
            ) AS dr
        FROM (
            SELECT
                YEAR(o.OrderDate) AS Anio,
                er.RegionID,
                p.ProductName,
                SUM(od.Quantity * od.UnitPrice) AS GananciaTotal
            FROM `order details` AS od
            INNER JOIN orders AS o ON od.OrderID = o.OrderID
            INNER JOIN products AS p ON od.ProductID = p.ProductID
            INNER JOIN (
                SELECT DISTINCT et.EmployeeID, t.RegionID
                FROM employeeterritories AS et
                INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
            ) AS er ON o.EmployeeID = er.EmployeeID
            WHERE o.OrderDate IS NOT NULL
            GROUP BY Anio, er.RegionID, p.ProductName
        ) AS ventas_agrupadas
    ) AS ranking
    WHERE dr = 1
    GROUP BY Anio, RegionID, GananciaTotal
) AS productos_empatados
GROUP BY Anio
ORDER BY Anio DESC;


-- -----------------------------------------------------------------------------
-- PASO 4: Consultas de control (auditoria)
-- -----------------------------------------------------------------------------

-- 4A) Ventas por producto y anio (sin region, 2 tablas)
SELECT
    YEAR(o.OrderDate) AS Anio,
    od.ProductID,
    SUM(od.Quantity * od.UnitPrice) AS GananciaTotal
FROM orders AS o
INNER JOIN `order details` AS od ON o.OrderID = od.OrderID
WHERE o.OrderDate IS NOT NULL
GROUP BY Anio, od.ProductID
ORDER BY Anio DESC, GananciaTotal ASC;

-- 4B) Ventas por producto, anio y region (con descuento opcional)
SELECT
    YEAR(o.OrderDate) AS Anio,
    TRIM(r.RegionDescription) AS Region,
    od.ProductID,
    ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount)), 2) AS GananciaTotal
FROM orders AS o
INNER JOIN `order details` AS od ON o.OrderID = od.OrderID
INNER JOIN (
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
GROUP BY Anio, Region, od.ProductID
ORDER BY Anio DESC, GananciaTotal ASC;
