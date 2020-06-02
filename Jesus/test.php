#!/usr/bin/php
<?php
include "connect.php";

$text = "/tasa 3.33";
if (strpos($text,"/tasa") !== false) {
  $tasa = str_word_count($text, 1, "0123456789.")[1];
  $sql = "UPDATE DICOM SET tasa = '$tasa' WHERE id = 2";
  $result = $link->query($sql);
  echo $result;
}else {
  echo "Not Ok\n";
}


?>