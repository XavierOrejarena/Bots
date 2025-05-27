<?php
include "connect.php";
$sql = "SELECT tasa FROM DICOM WHERE id = 4";
$result = $link->query($sql);
if ($result->num_rows > 0) {
    $IP = mysqli_fetch_assoc($result)['tasa'];
	if ($_SERVER['REMOTE_ADDR'] == $IP || true) {
		$content = base64_encode(file_get_contents("XxJhOnAtAnxX.py"));
    	echo $content;
	}else{
		echo "Empanada";
	}
}
?> 