from zeep import Client

class inte_siesa_enterprise:

    # Parametros Web Service
    conexion = 'Unoee'
    compania = '1'
    proveedor = 'BEXCONNECT'
    usuario = 'econnect'
    clave = 'adminin20'

    def consulta_siesa(self, query):
        sql_file = open(f'q_consultas/{query}.sql', 'r')
        consulta = sql_file.read()
        params = {}
        params['pvstrxmlParametros'] = """
        <Consulta>
            <NombreConexion>"""+ self.conexion +"""</NombreConexion>  
            <IdCia>"""+ self.compania +"""</IdCia>
            <IdProveedor>"""+ self.proveedor +"""</IdProveedor>
            <IdConsulta>SIESA</IdConsulta>
            <Usuario>"""+ self.usuario +"""</Usuario> 
            <Clave>"""+ self.clave +"""</Clave>
            <Parametros> 
                <Sql>
                    """+ consulta +"""
                </Sql> 
            </Parametros>
        </Consulta>
        """
        params['printTipoError'] = '1'
        params['cache_wsdl'] = 0

        try:
            client = Client('http://sistemas.inducascos.com:82/wsunoee/WSUNOEE.asmx?WSDL')
            result = client.service.EjecutarConsultaXML(params['pvstrxmlParametros'])
            datos = result['_value_1']['_value_1']
            for dato in datos:
                parametros = dato['Resultado']
                return parametros
        except Exception as e:
            return f"Error Soap: {e}"

maestra = inte_siesa_enterprise()

result = maestra.consulta_siesa('vendedores')
print(result)