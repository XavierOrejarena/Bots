<?php
$data = json_encode(file_get_contents("php://input"));
file_put_contents("test.json", json_decode($data))
?>
