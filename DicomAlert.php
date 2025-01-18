#!/usr/bin/env php
<?php

print_r(json_decode(file_get_contents("https://exchange.vcoud.com/coins/latest?type=bolivar&base=usd"), true)[0]['price']);

?>
