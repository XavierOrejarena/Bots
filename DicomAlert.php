#!/usr/bin/env php
<?php
// @DicomAlert
// /usr/local/bin/php /home/xavier/public_html/DicomAlert.php
include "connect.php";
// $data = file_get_contents("http://www.bcv.org.ve");
$data = file_get_contents("http://bcv.org.ve", true);
// preg_match_all('/<strong>/', $data, $matches, PREG_OFFSET_CAPTURE);
// $text = substr($data, $matches[0][6][1]+9, 10);
// $text = (string)$text;
// $token = '16396100:AAG_6y_pnkgYCKNRMyFVHow2eefR719DfCk';
// $chat_id = '@AlertaBCV';
// $chat_id = 149273661;

// $sql = "SELECT tasa FROM DICOM WHERE id = 1";
// $result = $link->query($sql);


// echo strlen($text); 

// if ($result->num_rows > 0 && $text != "") {
//     $OldText = mysqli_fetch_assoc($result)['tasa'];
// 	if ($text !== $OldText) {
// 		if (!preg_match('/[a-zA-Z]/', $text)) {
// 			$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 1";
// 			if ($link->query($sql) === TRUE) {
// 				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=$text");
// 				// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=old: $OldText");
// 				// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=OLD:$OldText NEW:$text"); 
// 			} else {
// 				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=error".$conn->error); 
// 			}
// 		} else {
// 			file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
// 		}
		

// 	}
// } else {
// 	file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
//     file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=0 Results");
// }
?>