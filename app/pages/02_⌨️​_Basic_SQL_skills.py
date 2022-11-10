import streamlit as st

st.set_page_config(layout='wide')

sql = st.container()

with sql:
    st.subheader('1. For each month from Jan 2019 through Sep 2019, how many loans were given, to how many clients, and what is the total principal amount.')

    st.code(
        '''
        SELECT
	origination_date,
	COUNT(loan_id),
	COUNT(client_id),
	SUM(principal_amount) -- columns of date, number of loans and clients, and total amount
FROM
	LOANS
WHERE
	origination_date > '2018-12-31'
	AND origination_date < '2019-10-01' -- filter to get dates between January and September 2019
GROUP BY
	MONTH(origination_date); -- results are grouped by month
        ''', language='sql'
    )

    st.subheader('2. At present how many clients have been given 3 or more loans?')
    
    st.code(
        '''
        SELECT
	client_id,
	COUNT(client_id) as counts -- selection of client id and the number of times the client appears
FROM
	LOANS
WHERE
	counts >= 3 -- filter to obtain those who obtained 3 or more loans
GROUP BY
	client_id
ORDER BY
	counts DESC;
        ''',language='sql'
    )

    st.subheader('3. For clients located in Bogota (city_id = 7) and for whom the sum of principal amount on all his/her loans is higher than $10.000.000, what is the average payment amount via ELECTRONIC channel?')

    st.code(
        '''
        SELECT
	l.client_id,
    SUM(l.principal_amount) as total_amount,
	AVG(p.amount) as avg_payment -- selection of client id, total loan amount and average payment
FROM
	PAYMENTS p
	JOIN LOANS l ON p.loan_id = l.loan_id
	JOIN CLIENTS c ON l.client_id = c.client_id
WHERE
	c.city_id = 7
	AND total_amount > 10000000
	AND p.channel = 'ELECTRONIC' -- filters by city, total amount and payment channel
GROUP BY
	l.client_id
ORDER BY
	avg_payments DESC;
        ''', language='sql'
    )