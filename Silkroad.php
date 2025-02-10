<?php
file_put_contents('test.json', file_get_contents(json_decode('php://input')));
?>
