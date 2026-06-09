"""
Consultas de la practica 4 (Northwind):

  1) CONSULTA_SQL          -> MySQL: producto(s) con MAX ganancia por anio y region
  2) CONSULTA_PY           -> detalle fila a fila para Python
  3) CONSULTA_TOTAL_REGION -> suma global con region de empleado
  4) CONSULTA_TOTAL_VENTAS -> suma global Northwind (order details + orders)
  5) CONSULTA_RANKING     -> todas las ganancias + Posicion (auditoria sin WHERE)

Region = employeeterritories -> territories -> region (via orders.EmployeeID)
Ganancia linea = Quantity * UnitPrice
Empates: varios productos con la misma ganancia maxima en el mismo anio/region.
"""

_EMPLEADO_REGION = """
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
"""

CONSULTA_SQL = f"""
SELECT
    ventas.Anio,
    ventas.RegionID,
    TRIM(r.RegionDescription) AS Region,
    ventas.Producto,
    ventas.Ganancia
FROM (
    SELECT
        YEAR(o.OrderDate) AS Anio,
        er.RegionID,
        p.ProductName AS Producto,
        SUM(od.Quantity * od.UnitPrice) AS Ganancia,
        DENSE_RANK() OVER (
            PARTITION BY YEAR(o.OrderDate), er.RegionID
            ORDER BY SUM(od.Quantity * od.UnitPrice) DESC
        ) AS dr
    FROM `order details` AS od
    INNER JOIN orders AS o ON od.OrderID = o.OrderID
    INNER JOIN products AS p ON od.ProductID = p.ProductID
    INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
    WHERE o.OrderDate IS NOT NULL
    GROUP BY Anio, er.RegionID, p.ProductName
) AS ventas
INNER JOIN region AS r ON ventas.RegionID = r.RegionID
WHERE ventas.dr = 1
ORDER BY ventas.Anio, ventas.RegionID, ventas.Producto
"""

CONSULTA_PY = f"""
SELECT
    YEAR(o.OrderDate) AS Anio,
    er.RegionID,
    TRIM(r.RegionDescription) AS Region,
    p.ProductName AS Producto,
    od.Quantity,
    od.UnitPrice
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN products AS p ON od.ProductID = p.ProductID
INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
INNER JOIN region AS r ON er.RegionID = r.RegionID
WHERE o.OrderDate IS NOT NULL
ORDER BY Anio, RegionID, Producto
"""

CONSULTA_TOTAL_REGION = f"""
SELECT SUM(od.Quantity * od.UnitPrice) AS Ventas_total
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
WHERE o.OrderDate IS NOT NULL
"""

CONSULTA_TOTAL_VENTAS = """
SELECT SUM(od.Quantity * od.UnitPrice) AS Ventas_total
FROM `order details` AS od
INNER JOIN orders AS o ON od.OrderID = o.OrderID
WHERE o.OrderDate IS NOT NULL
"""

# Auditoria: lista completa con ranking por (anio, region). Posicion = 1 es el maximo.
CONSULTA_RANKING = f"""
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
    INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
    WHERE o.OrderDate IS NOT NULL
    GROUP BY Anio, er.RegionID, p.ProductName
) AS ventas
INNER JOIN region AS r ON ventas.RegionID = r.RegionID
ORDER BY ventas.Anio, ventas.RegionID, Posicion, ventas.Ganancia DESC, ventas.Producto
"""
