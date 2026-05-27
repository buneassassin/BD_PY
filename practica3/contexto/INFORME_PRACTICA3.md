# Práctica 3 — Ganancias por autor (base de datos `tienda` / Pubs)

## 1. Objetivo

Obtener las ganancias por autor usando una consulta con **3 tablas** (`titleauthor`, `titles`, `sales`), con agregado **SUM**, sin subconsultas, procedimientos ni vistas. Replicar el mismo resultado en **Python** y validar que coincida con SQL.

---

## 2. Fórmula de ganancia

Por cada línea que une las tres tablas:

```
ganancia_línea = qty × price × (royaltyper / 100)
```

| Campo        | Tabla         | Significado                                      |
|--------------|---------------|--------------------------------------------------|
| `qty`        | `sales`       | Unidades vendidas en ese pedido                  |
| `price`      | `titles`      | Precio del libro                                 |
| `royaltyper` | `titleauthor` | Porcentaje de regalía que le corresponde al autor |

- **Ganancia** = `SUM(ganancia_línea)` por autor (`au_id`).

No se usa la tabla `roysched` ni el campo `titles.ytd_sales`; solo ventas registradas en `sales`.

---

## 3. Consulta principal (entrega SQL)

Archivo: `sql/practica3_ganancias_por_autor.sql`

```sql
SELECT
    ta.au_id,
    ROUND(SUM(s.qty * t.price * ta.royaltyper / 100.0), 2) AS Ganancia
FROM titleauthor AS ta
INNER JOIN titles AS t ON ta.title_id = t.title_id
INNER JOIN sales AS s ON s.title_id = t.title_id
GROUP BY ta.au_id
ORDER BY Ganancia DESC;
```

---

## 4. Auditoría venta por venta

En `sales` hay **10** registros. **9** títulos tienen autor en `titleauthor`; **1** venta queda fuera (ver sección 5).

### 4.1 TC3218 — Sylvia Panteley (`807-91-6654`), royaltyper 100%

| ord_num | qty | price | Cálculo           | ganancia_línea |
|---------|-----|-------|-------------------|----------------|
| P2121   | 40  | 20.95 | 40 × 20.95 × 1    | **838.00**       |

**Ganancia total = 838.00**

### 4.2 PS2091 — Albert Ringer (`998-72-3567`), royaltyper 50%

| ord_num   | qty | price | Cálculo              | ganancia_línea |
|-----------|-----|-------|----------------------|----------------|
| 722a      | 3   | 10.95 | 3 × 10.95 × 0.5      | 16.425         |
| QA7442.3  | 75  | 10.95 | 75 × 10.95 × 0.5     | **410.625**    |
| D4482     | 10  | 10.95 | 10 × 10.95 × 0.5     | 54.75          |
| N914008   | 20  | 10.95 | 20 × 10.95 × 0.5     | 109.50         |

- **SUM** = 591.30

### 4.3 PC8888 — coautores al 50% (una venta: qty 50, price 20.00)

| au_id         | Autor          | royaltyper | ganancia_línea |
|---------------|----------------|------------|----------------|
| 427-17-2319   | Ann Dull       | 50         | **500.00**     |
| 846-92-7186   | Sheryl Hunter  | 50         | **500.00**     |

Cada autor recibe su 50%; no es doble conteo para un solo autor.

### 4.4 BU7832 — Dean Straight (`274-80-9391`), royaltyper 100%

| ord_num | qty | price | ganancia_línea |
|---------|-----|-------|----------------|
| QQ2299  | 15  | 19.99 | **299.85**     |

### 4.5 BU1111 — Michael O'Leary (`267-41-2394`), royaltyper 40%

| ord_num | qty | price | ganancia_línea |
|---------|-----|-------|----------------|
| P723    | 25  | 11.95 | **119.50**     |

### 4.6 MC3021 — coautores 75% / 25% (qty 15, price 2.99)

| au_id         | Autor           | royaltyper | Cálculo              | ganancia_línea |
|---------------|-----------------|------------|----------------------|----------------|
| 722-51-5454   | Michel DeFrance | 75         | 15 × 2.99 × 0.75     | **33.64**      |
| 899-46-2035   | Anne Ringer     | 25         | 15 × 2.99 × 0.25     | **11.21**      |

Comprobación: 33.6375 + 11.2125 = 44.85 = 15 × 2.99 (reparto 100%).

---

## 5. Venta excluida: PS7777 (P3087a)

| Campo    | Valor                          |
|----------|--------------------------------|
| Pedido   | P3087a                         |
| Tienda   | 7131                           |
| qty      | 25                             |
| title_id | **PS7777**                     |

**Motivo:** en `titleauthor` no existe ninguna fila con `title_id = 'PS7777'`. Con `INNER JOIN`, esa venta no entra en el resultado.


---

## 6. Resultado final verificado

| au_id       | Ganancia |
|-------------|----------|
| 807-91-6654 | 838.00   |
| 998-72-3567 | 591.30   |
| 427-17-2319 | 500.00   |
| 846-92-7186 | 500.00   |
| 274-80-9391 | 299.85   |
| 267-41-2394 | 119.50   |
| 722-51-5454 | 33.64    |
| 899-46-2035 | 11.21    |

Solo aparecen **8 autores** de 23 en `authors`: hace falta estar en `titleauthor` y que su libro tenga al menos una venta en `sales`. Los demás autores tienen libros asignados pero sin filas en `sales`.

---

## 7. Validación con Python

| Archivo | Descripción |
|---------|-------------|
| `practica3_validacion.py` | Programa principal (arranque) |
| `practica3/conexion.py` | Lee datos de MySQL |
| `practica3/calculo.py` | Fórmula y SUM en Python |
| `practica3/comparacion.py` | Compara SQL vs Python |
| `salida_validacion.txt` | Captura de terminal con veredicto **VALIDACION OK** |

Comandos:

```powershell
$env:MYSQL_PASSWORD = "tu_contraseña"
$env:MYSQL_DATABASE = "tienda"
python practica3_validacion.py --explicar    # texto para explicar al profesor
python practica3_validacion.py               # validacion
python practica3_validacion.py --guardar-salida
```

Fragmento del veredicto (completo en `salida_validacion.txt`):

```
VALIDACION OK: Python reproduce exactamente la consulta SQL.
Mayor ganancia total: au_id 807-91-6654 -> 838.00
```

---

## 8. Consulta de control (Navicat)

Archivo: `sql/practica3_consulta_control.sql`

Muestra cada línea antes del `GROUP BY`; la suma de `ganancia_linea` por `au_id` debe coincidir con la columna `Ganancia` de la consulta principal.

---

## 9. Conclusión

- Los importes son **correctos** frente al dump de `tienda`.
- La consulta cumple: **3 tablas**, **SUM**, **sin subconsultas/vistas/procedimientos**.
- Python **reproduce** SQL (diferencia ≤ 0.01 por redondeo en un caso).
- La venta **PS7777** y los autores sin ventas en `sales` explican los registros que no aparecen en el resultado.
