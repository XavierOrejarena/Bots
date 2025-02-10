<?php
file_put_contents('test.json', json_decode(file_get_contents('php://input')));
?>
