-- 1
SELECT
	origination_date,
	COUNT(loan_id),
	COUNT(client_id),
	SUM(principal_amount) -- columnas de fecha, cantidad de prestamos y clientes, y monto total
FROM
	LOANS
WHERE
	origination_date > '2018-12-31'
	AND origination_date < '2019-10-01' -- filtros para fechas entre enero y septiembre 2019
GROUP BY
	MONTH(origination_date); -- se agrupan los resultados por mes

-- 2
SELECT
	client_id,
	COUNT(client_id) as counts -- seleccion de id cliente y la cantidad de veces que aparece el cliente
FROM
	LOANS
WHERE
	counts >= 3 -- filtro para obtener los que obtuvieron 3 o más préstamos
GROUP BY
	client_id
ORDER BY
	counts DESC;


-- 3
SELECT
	l.client_id,
    SUM(l.principal_amount) as total_amount,
	AVG(p.amount) as avg_payment -- seleccion de id cliente, monto total de prestamo y pago promedio
FROM
	PAYMENTS p
	JOIN LOANS l ON p.loan_id = l.loan_id
	JOIN CLIENTS c ON l.client_id = c.client_id
WHERE
	c.city_id = 7
	AND total_amount > 10000000
	AND p.channel = 'ELECTRONIC' -- filtros por ciudad, monto total y canal de pago
GROUP BY
	l.client_id
ORDER BY
	avg_payments DESC;