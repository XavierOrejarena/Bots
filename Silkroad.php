<?php
file_put_contents('sro.json', json_encode(file_get_contents('php://input')));
?>
