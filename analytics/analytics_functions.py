from etl.db_operations import select_data

def get_regions(conn):
    """
        Function connects to SQLite DB and returns regions iterator.
        Input Parameters:
            conn - connection to SQLite DB
        Output: returns regions iterator
    """
    query = """
        SELECT DISTINCT region FROM hourly_prices ORDER BY region
    """
    regions_iterator = select_data(conn, query)
    return regions_iterator

def get_chart_data(conn, start_date, end_date):
    """
        Function connects to SQLite DB and returns data iterator
        Input:
            conn - connection to SQLite DB
            start_date - start date 
            end_date - end date
        Output: returns data iterator
    """
    query = """
        SELECT price_time, region, price 
        FROM hourly_prices
        WHERE price_time >= ? AND price_time <= ?
            AND region IN ('AT', 'BE', 'DK1', 'EE', 'FI', 'FR', 'LT', 'LV', 'NL', 'SE1')
        ORDER BY region, price_time
    """
    sdate = start_date.strftime('%Y-%m-%d') + " 00:00"
    edate = end_date.strftime('%Y-%m-%d') + " 23:00"
    chart_data_iterator = select_data(conn, query, (sdate, edate))
    return chart_data_iterator

        
    