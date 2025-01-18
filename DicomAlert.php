#!/usr/bin/env php
<?php

$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
);  

$data = file_get_contents("http://bcv.org.ve", false, stream_context_create($arrContextOptions));
preg_match_all('/> USD</', $data, $matches, PREG_OFFSET_CAPTURE);
$text = substr($data, $matches[0][0][1]+122, 11);
echo "$text";

?>
