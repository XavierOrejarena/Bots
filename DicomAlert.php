#!/usr/bin/env php
<?php

$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
);  

$data = file_get_contents("https://static.blockshift.co/ve_rates.json", true, stream_context_create($arrContextOptions));


echo "$data";

?>
