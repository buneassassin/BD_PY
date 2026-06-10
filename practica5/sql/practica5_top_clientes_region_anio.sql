-- =============================================================================
-- PRACTICA 5 - Cliente(s) top del producto top, por anio y region (sin WITH)
-- =============================================================================

SELECT
    ranked.Anio,
    ranked.RegionID,
    ranked.Region,
    ranked.Producto,
    ranked.CustomerID,
    ranked.Cliente,
    ranked.Compras
FROM (
    SELECT
        compras.Anio,
        compras.RegionID,
        compras.Region,
        compras.Producto,
        compras.CustomerID,
        compras.Cliente,
        compras.Compras,
        DENSE_RANK() OVER (
            PARTITION BY compras.Anio, compras.RegionID
            ORDER BY compras.Compras DESC
        ) AS dr
    FROM (
        SELECT
            YEAR(o.OrderDate) AS Anio,
            er.RegionID,
            TRIM(r.RegionDescription) AS Region,
            tp.Producto,
            o.CustomerID,
            TRIM(c.CompanyName) AS Cliente,
            SUM(od.Quantity * od.UnitPrice) AS Compras
        FROM `order details` AS od
        INNER JOIN orders AS o ON od.OrderID = o.OrderID
        INNER JOIN products AS p ON od.ProductID = p.ProductID
        INNER JOIN customers AS c ON o.CustomerID = c.CustomerID
        INNER JOIN (
            SELECT DISTINCT et.EmployeeID, t.RegionID
            FROM employeeterritories AS et
            INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
        ) AS er ON o.EmployeeID = er.EmployeeID
        INNER JOIN region AS r ON er.RegionID = r.RegionID
        INNER JOIN (
            SELECT prod.RegionID, prod.Producto
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
            ) AS prod
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
            ) AS max_prod
                ON prod.RegionID = max_prod.RegionID
                AND prod.Ventas = max_prod.Ventas_max
        ) AS tp ON er.RegionID = tp.RegionID AND p.ProductName = tp.Producto
        WHERE o.OrderDate IS NOT NULL
        GROUP BY Anio, er.RegionID, Region, tp.Producto, o.CustomerID, Cliente
    ) AS compras
) AS ranked
WHERE ranked.dr = 1
ORDER BY ranked.Anio, ranked.RegionID, ranked.Cliente;
