-- =============================================================================
-- VERIFICACION PASO A PASO (practica 4) - exportar a Excel
-- =============================================================================
-- Problema con la lista plana (solo Año, RegionID, ProductName, GananciaTotal):
--   Si en Excel filtras RegionID=1 y ordenas GananciaTotal de mayor a menor,
--   la primera fila es 1998 (46112.5), NO el top de 1996 (18972).
--   Mezclar años al ordenar da la impresion de que el dato "esta mal".
--
-- Solucion: esta consulta muestra TODOS los productos (sin WHERE) pero agrega
--   Posicion = ranking dentro de cada (Año, RegionID).
--   Posicion = 1  ->  producto(s) con mayor ganancia en ese año y región.
--   Orden: Año, RegionID, Posicion, Ganancia DESC  ->  comprobación visual rápida.
-- =============================================================================

SELECT
    ventas.Anio,
    ventas.RegionID,
    TRIM(r.RegionDescription) AS Region,
    ventas.Producto,
    ventas.Ganancia,
    DENSE_RANK() OVER (
        PARTITION BY ventas.Anio, ventas.RegionID
        ORDER BY ventas.Ganancia DESC
    ) AS Posicion
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
    WHERE o.OrderDate IS NOT NULL
    GROUP BY Anio, er.RegionID, p.ProductName
) AS ventas
INNER JOIN region AS r ON ventas.RegionID = r.RegionID
ORDER BY ventas.Anio, ventas.RegionID, Posicion, ventas.Ganancia DESC, ventas.Producto;

-- Comprobacion del total global (debe dar 1,354,458.59):
-- SELECT SUM(Ganancia) FROM ( ... subconsulta ventas sin DENSE_RANK ... ) AS t;
