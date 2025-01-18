#!/usr/bin/env php
<?php

$arrContextOptions = array(
      "ssl" => array(
        "verify_peer" => false,
        "verify_peer_name" => false,
      )
);  
  
$context = stream_context_create($arrContextOptions);
$contents = file_get_contents("https://static.blockshift.co/ve_rates.json",false, $context);
$dolar = json_decode($contents,true)['prom_epv'];
echo "$dolar";
?>
