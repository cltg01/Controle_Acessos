<!DOCTYPE html>
<html>
<?php include 'html/head.php'; ?>
<body>
    <div class="container-fluid">
        <?php 
            $titulo = 'Registro de Saída';
            $exibirTopo = false;
            require_once 'html/movimentacao/topo.php';
        ?>

        <?php include_once 'html/mensagem.php'; ?>
        <?php 
            require('formulariosaida.php'); 
        ?>
    </div>

    <script src="html/script.js"></script>
    <?php include 'html/scriptsjs.php'; ?>
</body>
</html>