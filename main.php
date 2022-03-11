<?php
    if($_POST) {
        $parm['pvstrxmlParametros']="<Consulta>
                                        <NombreConexion>".$_POST['conexion']."</NombreConexion>
                                        <IdCia>".$_POST['IdCia']."</IdCia>
                                        <IdProveedor>".$_POST['proveedor']."</IdProveedor>
                                        <IdConsulta>SIESA</IdConsulta>
                                        <Usuario>".$_POST['user']."</Usuario>
                                        <Clave>".$_POST['password']."</Clave>
                                        <Parametros>
                                            <Sql>".$_POST['sql']."</Sql>
                                        </Parametros>
                                    </Consulta>";
        $parm['printTipoError'] = '1';
        $parm['cache_wsdl'] = WSDL_CACHE_NONE;

        // Proxy url.
        if($_POST['proxy_host'] != '')
            $parm['proxy_host'] = $_POST['proxy_host']; //'191.102.113.190';
        if($_POST['proxy_port'] != '')
            $parm['proxy_port'] = $_POST['proxy_port']; //5721;

        echo '<textarea id="debug" style="width:100%;height:300px;display:none;">';
        print_r($parm);
        echo "</textarea>";
        echo '<a id="debug_a1" href="#" onclick="document.getElementById(\'debug\').style.display=\'block\';document.getElementById(\'debug_a1\').style.display=\'none\';document.getElementById(\'debug_a2\').style.display=\'block\';">Debug</a>';
        echo '<a id="debug_a2" style="display:none;" id="a1" href="#" onclick="document.getElementById(\'debug\').style.display=\'none\';document.getElementById(\'debug_a1\').style.display=\'block\';document.getElementById(\'debug_a2\').style.display=\'none\';">Cerrar</a>';
        try {
            $client = new SoapClient($_POST['url'], $parm);
            $result = $client->EjecutarConsultaXML($parm);//llamamos al métdo que nos interesa con los parámetros
            $schema = @simplexml_load_string($result->EjecutarConsultaXMLResult->schema);
            $any = @simplexml_load_string($result->EjecutarConsultaXMLResult->any);

            if(@is_object($any->NewDataSet->Resultado )) {
                foreach ($any->NewDataSet->Resultado as $key => $value) {
                    foreach ($value as $campo => $valor) {
                        $resultado[(String)$campo] = (String)$valor;
                    }
                    unset($resultado['ws_id']);
                    $data[] = $resultado;
                    $resultado = array();
                }
            }

            if(@$any->NewDataSet->Table) {
                foreach ($any->NewDataSet->Table as $key => $value) {
                    echo "\n";
                    echo "\nError Linea:\t ".$value->F_NRO_LINEA;
                    echo "\nError Value:\t ".$value->F_VALOR;
                    echo "\nError Desc:\t ".$value->F_DETALLE;
                }
            }
        }

        catch (Exception $e) {
        $error = $e->getMessage();
        }
    }

    if(!$_POST['conexion'])
        $_POST['conexion'] = 'unoee_siesa';
?>

<!DOCTYPE html>
<html>
<html lang="en">
    <head>
        <title>Test Soap</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="x-ua-compatible" content="ie=edge">

        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/css/bootstrap.min.css" integrity="2hfp1SzUoho7/TsGGGDaFdsuuDL0LX2hnUp6VkX3CUQ2K4K+xjboZdsXyp4oUHZj" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdn.datatables.net/1.10.12/css/jquery.dataTables.min.css" >
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.0.0/jquery.min.js" integrity="sha384-THPy051/pYDQGanwU6poAc/hOdQxjnOEXzbT+OuUAFqNqFjL+4IGLBgCJC3ZOShY" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.2.0/js/tether.min.js" integrity="sha384-Plbmg8JY28KFelvJVai01l8WyZzrYWG825m+cZ0eDDS1f7d/js6ikvy1+X+guPIB" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.4/js/bootstrap.min.js" integrity="VjEeINv9OSwtWFLAtmc4JCtEJXXBub00gtSnszmspDLCtC0I4z4nqz7rEFbIZLLU" crossorigin="anonymous"></script>
        <script src="https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min.js" ></script>
    </head>
    <body>
        <nav class="navbar navbar-dark bg-inverse">
            <a class="navbar-brand" href="#">Test BEXconnect</a>
        </nav>

        <div class="container">
            <br>
            <br>
            <form method="POST">
                <?php 
                    if($error ) {
                ?>
                <div class="alert alert-danger">
                    <?php echo utf8_decode($error); ?>
                </div>

                    <?php
                    }
                    ?>

                <div class="form-group">
                    <label for="url">URL Server:</label>
                    <input type="url" required class="form-control" name="url" value="<?php echo $_POST["url"]; ?>" id="url">
                </div>
                <div class="form-group">
                    <label for="proxy_host">Proxy Host:</label>
                    <input type="text" class="form-control" name="proxy_host" value="<?php echo $_POST["proxy_host"]; ?>" id="proxy_host">
                </div>
                <div class="form-group">
                    <label for="proxy_port">Proxy Port:</label>
                    <input type="text" class="form-control" name="proxy_port" value="<?php echo $_POST["proxy_port"]; ?>" id="proxy_port">
                </div>
                <div class="form-group">
                    <label for="conexion">Conexion:</label>
                    <input type="text" required class="form-control" value="<?php echo $_POST["conexion"]; ?>" name="conexion" id="conexion">
                </div>
                <div class="form-group">
                    <label for="IdCia">IdCia:</label>
                    <input type="number"  min=1 max=999 step=1required class="form-control" value="<?php  if($_POST["IdCia"]){ echo $_POST["IdCia"];}else{ echo '1'; }; ?>" name="IdCia" id="IdCia">
                </div>
                <div class="form-group">
                    <label for="user">Usuario:</label>
                    <input type="text" required class="form-control" name="user" value="<?php echo $_POST["user"]; ?>" id="user">
                </div>
                <div class="form-group">
                    <label for="pwd">Contrase&ntilde;a:</label>
                    <input type="text" required class="form-control" value="<?php echo $_POST["password"]; ?>" name="password" id="password">
                </div>
                <div class="form-group">
                    <label for="pwd">Proveedor:</label>
                    <select name="proveedor">
                        <option <?php if($_POST['proveedor']=='PICONNECT'){ echo 'selected'; } ?> value="PICONNECT">PICONNECT</option>
                        <option <?php if($_POST['proveedor']=='BEXCONNECT'){ echo 'selected'; } ?> value="BEXCONNECT">BEXCONNECT</option>
                        <option <?php if($_POST['proveedor']=='BEXMOVIL'){ echo 'selected'; } ?> value="BEXMOVIL">BEXMOVIL</option>
                        <option <?php if($_POST['proveedor']=='PIMOVIL'){ echo 'selected'; } ?> value="PIMOVIL">PIMOVIL</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="pwd">Formato:</label>
                    <select name="formato">
                        <option <?php if($_POST['formato']=='datatable'){ echo 'selected'; } ?> value="datatable">DataTable</option>
                        <option <?php if($_POST['formato']=='json'){ echo 'selected'; } ?> value="json">JSON</option>
                        option
                    </select>
                </div>
                <div class="form-group">
                    <label for="sql">SQL:</label>
                    <textarea required class="form-control" rows="10" name="sql" id="sql"><?php echo htmlentities($_POST["sql"], ENT_QUOTES, "UTF-8"); ?></textarea>
                </div>

                <button type="submit" class="btn btn-default">Run</button>
            </form>
                <hr>
                <?php
                    if($data && $_POST['formato'] =='datatable') {
                ?>
                    <table class="table">
                        <thead class="thead-inverse">
                            <tr>
                                <th>#</th>
                                    <?php 
                                        foreach ($data[0] as $key => $value) {
                                    ?>
                                    <th>
                                    <?php 
                                            echo $key; 
                                    ?>
                                </th>
                                    <?php
                                        }
                                    ?>
                            </tr>
                        </thead>
                        <tbody>
                            <?php 
                                foreach ($data as $key => $value) {
                            ?>
                            <tr>
                                <th scope="row"><?php echo intval($key)+1; ?></th>
                                <?php 
                                    foreach ($value as $key2 => $value2) {
                                ?>
                                    <td>
                                    <?php 
                                        echo $value2; 
                                    ?>
                                    </td>
                                <?php
                                    }
                                ?>
                            </tr>
                            <?php
                                }
                            ?>
                        </tbody>
                        <?php 
                            foreach ($data as $key => $value) {
                        ?>
                            <tr>
                            <th scope="row">
                            <?php 
                                echo intval($key)+1; 
                            ?>
                            </th>
                            <?php 
                                foreach ($value as $key2 => $value2) {
                            ?>
                                <td>
                                <?php 
                                    echo $value2; 
                                ?>
                                </td>
                            <?php
                                }
                            ?>
                            </tr>
                        <?php
                            }
                        ?>
                    </tbody>
                </table>
            <?php
                }
            ?>

            <?php
                if($data && $_POST['formato'] =='json') {
                    echo "<pre>";
                    print_r($data);
                    echo "</pre>";
                }
            ?>
        </div>

        <script>
            $(function () {
                $("table").DataTable();
            });
        </script>
    </body>
</html>