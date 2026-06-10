"""
Consultas de la practica 5 (Northwind):

  CONSULTA_TOP_PRODUCTOS_SQL  -> producto(s) con MAX ventas por region
  CONSULTA_TOP_CLIENTES_SQL   -> cliente(s) que mas compraron esos productos por region y anio
  CONSULTA_PY                 -> detalle fila a fila para Python
  CONSULTA_TOTAL_REGION       -> suma global con region de empleado
  CONSULTA_RANKING_PRODUCTOS  -> todos los productos con Posicion por region (auditoria)
  CONSULTA_RANKING_CLIENTES   -> todos los clientes con Posicion por region y anio (auditoria)

Region = employeeterritories -> territories -> region (via orders.EmployeeID)
Venta linea = Quantity * UnitPrice
"""

_EMPLEADO_REGION = """
    SELECT DISTINCT et.EmployeeID, t.RegionID
    FROM employeeterritories AS et
    INNER JOIN territories AS t ON et.TerritoryID = t.TerritoryID
"""

_VENTAS_POR_PRODUCTO_REGION = f"""
    SELECT
        er.RegionID,
        p.ProductName AS Producto,
        SUM(od.Quantity * od.UnitPrice) AS Ventas
    FROM `order details` AS od
    INNER JOIN orders AS o ON od.OrderID = o.OrderID
    INNER JOIN products AS p ON od.ProductID = p.ProductID
    INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
    WHERE o.OrderDate IS NOT NULL
    GROUP BY er.RegionID, p.ProductName
"""

_TOP_PRODUCTOS_SUB = f"""
    SELECT RegionID, Producto
    FROM (
        SELECT
            RegionID,
            Producto,
            DENSE_RANK() OVER (
                PARTITION BY RegionID
                ORDER BY Ventas DESC
            ) AS dr
        FROM ({_VENTAS_POR_PRODUCTO_REGION}) AS ventas
    ) AS ranked
    WHERE dr = 1
"""

CONSULTA_TOP_PRODUCTOS_SQL = f"""
    SELECT RegionID, Region, Producto, Ventas
    FROM (
        SELECT
            v.RegionID,
            TRIM(r.RegionDescription) AS Region,
            v.Producto,
            v.Ventas,
            DENSE_RANK() OVER (
                PARTITION BY v.RegionID
                ORDER BY v.Ventas DESC
            ) AS dr
        FROM ({_VENTAS_POR_PRODUCTO_REGION}) AS v
        INNER JOIN region AS r ON v.RegionID = r.RegionID
    ) AS ventas
    WHERE dr = 1
    ORDER BY RegionID, Producto
"""

CONSULTA_TOP_CLIENTES_SQL = f"""
    SELECT Anio, RegionID, Region, Producto, CustomerID, Cliente, Compras
    FROM (
        SELECT
            YEAR(o.OrderDate) AS Anio,
            er.RegionID,
            TRIM(r.RegionDescription) AS Region,
            p.ProductName AS Producto,
            o.CustomerID,
            TRIM(c.CompanyName) AS Cliente,
            SUM(od.Quantity * od.UnitPrice) AS Compras,
            DENSE_RANK() OVER (
                PARTITION BY YEAR(o.OrderDate), er.RegionID
                ORDER BY SUM(od.Quantity * od.UnitPrice) DESC
            ) AS dr
        FROM `order details` AS od
        INNER JOIN orders AS o ON od.OrderID = o.OrderID
        INNER JOIN products AS p ON od.ProductID = p.ProductID
        INNER JOIN customers AS c ON o.CustomerID = c.CustomerID
        INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
        INNER JOIN region AS r ON er.RegionID = r.RegionID
        INNER JOIN ({_TOP_PRODUCTOS_SUB}) AS tp
            ON er.RegionID = tp.RegionID AND p.ProductName = tp.Producto
        WHERE o.OrderDate IS NOT NULL
        GROUP BY YEAR(o.OrderDate), er.RegionID, r.RegionDescription,
                p.ProductName, o.CustomerID, c.CompanyName
    ) AS ranked
    WHERE dr = 1
    ORDER BY Anio, RegionID, Cliente;
"""

CONSULTA_PY = f"""
    SELECT
        YEAR(o.OrderDate) AS Anio,
        er.RegionID,
        TRIM(r.RegionDescription) AS Region,
        p.ProductName AS Producto,
        o.CustomerID,
        TRIM(c.CompanyName) AS Cliente,
        od.Quantity,
        od.UnitPrice
    FROM `order details` AS od
    INNER JOIN orders AS o ON od.OrderID = o.OrderID
    INNER JOIN products AS p ON od.ProductID = p.ProductID
    INNER JOIN customers AS c ON o.CustomerID = c.CustomerID
    INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
    INNER JOIN region AS r ON er.RegionID = r.RegionID
    WHERE o.OrderDate IS NOT NULL
    ORDER BY Anio, RegionID, Producto, CustomerID
"""

CONSULTA_TOTAL_REGION = f"""
    SELECT SUM(od.Quantity * od.UnitPrice) AS Ventas_total
    FROM `order details` AS od
    INNER JOIN orders AS o ON od.OrderID = o.OrderID
    INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
    WHERE o.OrderDate IS NOT NULL
"""

CONSULTA_RANKING_PRODUCTOS = f"""
    SELECT
        RegionID,
        Region,
        Producto,
        Ventas,
        DENSE_RANK() OVER (
            PARTITION BY RegionID
            ORDER BY Ventas DESC
        ) AS Posicion
    FROM (
        SELECT
            v.RegionID,
            TRIM(r.RegionDescription) AS Region,
            v.Producto,
            v.Ventas
        FROM ({_VENTAS_POR_PRODUCTO_REGION}) AS v
        INNER JOIN region AS r ON v.RegionID = r.RegionID
    ) AS ventas
    ORDER BY RegionID, Posicion, Ventas DESC, Producto
"""

CONSULTA_RANKING_CLIENTES = f"""
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
        ) AS Posicion
    FROM (
        SELECT
            YEAR(o.OrderDate) AS Anio,
            er.RegionID,
            TRIM(r.RegionDescription) AS Region,
            p.ProductName AS Producto,
            o.CustomerID,
            TRIM(c.CompanyName) AS Cliente,
            SUM(od.Quantity * od.UnitPrice) AS Compras
        FROM `order details` AS od
        INNER JOIN orders AS o ON od.OrderID = o.OrderID
        INNER JOIN products AS p ON od.ProductID = p.ProductID
        INNER JOIN customers AS c ON o.CustomerID = c.CustomerID
        INNER JOIN ({_EMPLEADO_REGION}) AS er ON o.EmployeeID = er.EmployeeID
        INNER JOIN region AS r ON er.RegionID = r.RegionID
        INNER JOIN ({_TOP_PRODUCTOS_SUB}) AS tp
            ON er.RegionID = tp.RegionID AND p.ProductName = tp.Producto
        WHERE o.OrderDate IS NOT NULL
        GROUP BY YEAR(o.OrderDate), er.RegionID, r.RegionDescription,
                p.ProductName, o.CustomerID, c.CompanyName
    ) AS compras
    ORDER BY compras.Anio, compras.RegionID, Posicion, compras.Compras DESC, compras.Cliente
"""
