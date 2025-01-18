#!/usr/bin/env php
<?php

$opts = array('http'=>array('header' => "User-Agent:MyAgent/1.0\r\n")); 
//Basically adding headers to the request
$context = stream_context_create($opts);
$data = file_get_contents("https://static.blockshift.co/ve_rates.json",false,$context);




echo "$data";

?>
