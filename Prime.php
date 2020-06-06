#!/usr/bin/env php
<?php

$x = 3;
$y = 199;

for ($i=0; $i < 40; $i++) { 
	echo $i.": ".pow($x,$i)%$y,"\n";
}


?>