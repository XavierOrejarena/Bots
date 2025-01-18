#!/usr/bin/env php
<?php

$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>true,
        "verify_peer_name"=>true,
    ),
);  

$data = file_get_contents("https://static.blockshift.co/ve_rates.json", false, stream_context_create($arrContextOptions));


echo "$data";

?>
