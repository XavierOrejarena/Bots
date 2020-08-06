#!/usr/bin/env php
<?php

    ini_set('default_socket_timeout', 900);
    $URL = file_get_contents("https://berserkerchk.000webhostapp.com/apifullbot.php?probar=cc&ccs=4165752111217120%7C04%7C21%7C731&separador=%7C", 0, $ctx);
    $DATA = json_decode($URL, true);
    
    echo "\n";
    print_r($URL);
    print_r($DATA);
    echo "\n";
    
    
    ?>