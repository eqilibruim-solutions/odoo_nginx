import json
import psycopg2

conn = psycopg2.connect("host=localhost dbname=integracion_mscwms user=simon_trillos password=0XGIXjsZUC")
cur = conn.cursor()

def prueba():
    sql = "SELECT compania, num_ped, nit_cliente, cod_vendedor, cond_pago, observacion, fecha_pedido FROM pedidos_wms WHERE observacion='' group by 1,2,3,4,5,6,7 ORDER BY num_ped ASC"
    cur.execute(sql)
    encab = cur.fetchall()
    data = {}
    for dat in encab:
        num_ped = dat[1]
        data = {"compania": dat[0], "num_ped": dat[1], "nit_cliente": dat[2], "cod_vendedor": dat[3], "cond_pago": dat[4], "observacion": dat[5], "fecha_pedido": dat[6]}

        sqldetalle = f"SELECT num_ped, cod_producto, cant_pedida, precio_unitario, descuento FROM pedidos_wms WHERE num_ped='{num_ped}'"
        cur.execute(sqldetalle)
        detalle = cur.fetchall()
        data['item'] = []
        for detll in detalle:
            data['item'].append({"cod_producto": detll[1], "cant_pedida": int(detll[2]), "precio_unitario": float(detll[3]), "descuento": float(detll[4])})
            update_sql_pe = "UPDATE pedidos_wms s SET observacion=o.ref FROM (VALUES (%s)) as o(ref) WHERE num_ped=%s"
            cur.execute(update_sql_pe, (dat[1], dat[1]))
            conn.commit()

        with open('/home/simon_trillos/maestro_integrador/pedidos_connection/datosjson/'+ str(num_ped) +'.json', 'w') as file:
            json.dump(data, file, indent=4)

prueba()