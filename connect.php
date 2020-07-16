<?php
$database = 'xavier';

// $host = '127.0.0.1';
// $usr = 'root';
// $password = 'xavier123';
// $port = 3306;
// $link = mysqli_connect($host, $usr, $password, $database,$port);
$host = 'localhost';
$usr = 'xavier';
$password = 'x4v13R';
$link = mysqli_connect($host, $usr, $password, $database);

if (!$link) {
    die("Connection failed: " . mysqli_connect_error());
  }
  echo "Connected successfully\n";
?>