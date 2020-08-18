#!/usr/bin/env php
<?php
// @DicomAlert
// /usr/local/bin/php /home/xavier/public_html/DicomAlert.php
include "connect.php";

$data = file_get_contents("http://www.bcv.org.ve");
preg_match_all('/USD/', $data, $matches, PREG_OFFSET_CAPTURE);
$text = substr($data, $matches[0][0][1]+85, 10);
$text = (string)$text;
$token = '716396100:AAE1MzNEEHrTixztiwFJZEhjt0loVK6eJFE';
$chat_id = '@dicomalert';
// $chat_id = 149273661;

$sql = "SELECT tasa FROM DICOM WHERE id = 1";
$result = $link->query($sql);


// echo strlen($text); 

if ($result->num_rows > 0) {
    $OldText = mysqli_fetch_assoc($result)['tasa'];
	if ($text != $OldText && strlen($text) > 7) {
		if (!is_numeric($text)) {
			$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 1";
			if ($link->query($sql) === TRUE) {
				file_get_contents("https://api.telegram.org/bot$token/sendMessage?chat_id=$chat_id&text=$text");
				// file_get_contents("https://api.telegram.org/bot$token/sendMessage?chat_id=$chat_id&text=old: $OldText");
			} else {
				file_get_contents("https://api.telegram.org/bot$token/sendMessage?chat_id=149273661&text=error".$conn->error); 
			}
		} else {
			file_get_contents("https://api.telegram.org/bot$token/sendMessage?chat_id=149273661&text=$text"); 
		}
		

	}
} else {
    file_get_contents("https://api.telegram.org/bot$token/sendMessage?chat_id=$chat_id&text=0 Results");
}
?>