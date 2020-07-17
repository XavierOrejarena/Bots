#!/usr/bin/env php
<?php

$text = "20*500k";
$BS = str_word_count($text, 1, '0123456789.')[1];
$signal = str_word_count($text, 1, '*xX/\def')[0];
$BS = pow(1000,strlen(stristr($BS, 'k')))*(real)$BS;

echo $BS, "\n";
?>