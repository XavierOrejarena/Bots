<?php
file_put_contents('sro.json', json_decode(file_get_contents('php://input')));
?>
