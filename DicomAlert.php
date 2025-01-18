#!/usr/bin/env php
<?php
// @DicomAlert
// /usr/local/bin/php /home/xavier/public_html/DicomAlert.php
include "connect.php";
// $data = file_get_contents("http://www.bcv.org.ve");
// $data = file_get_contents("http://bcv.org.ve", true);
$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
);  

$data = file_get_contents("http://bcv.org.ve", false, stream_context_create($arrContextOptions));

// preg_match_all('/<strong>/', $data, $matches, PREG_OFFSET_CAPTURE);
// $text = substr($data, $matches[0][6][1]+9, 10);
preg_match_all('/> USD</', $data, $matches, PREG_OFFSET_CAPTURE);
$text = substr($data, $matches[0][0][1]+122, 11);
$text = (string)$text;
$token = '16396100:AAG_6y_pnkgYCKNRMyFVHow2eefR719DfCk';
// $token = '716396100:AAG_6y_pnkgYCKNRMyFVHow2eefR719DfCk';
$chat_id = '@AlertaBCV';
// $chat_id = 149273661;


$sql = "SELECT tasa FROM DICOM WHERE id = 1";
$result = $link->query($sql);

// echo $text;
// echo strlen($text); 

if ($result->num_rows > 0 && $text != "") {
    $OldText = mysqli_fetch_assoc($result)['tasa'];
	if ($text !== $OldText) {
		if (!preg_match('/[a-zA-Z]/', $text)) {
			$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 1";
			if ($link->query($sql) === TRUE) {
				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=`$text`&parse_mode=markdown");
				// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=old: $OldText");
				// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=OLD:$OldText NEW:$text"); 
			} else {
				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=error".$conn->error); 
			}
		} else {
			file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
		}
		

	}
} else {
	file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
    file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=0 Results");
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$arrContextOptions = array("ssl" => array("verify_peer" => false,"verify_peer_name" => false,));  
$text = json_decode(file_get_contents("https://static.blockshift.co/ve_rates.json",false,stream_context_create($arrContextOptions)),true)['prom_epv'];
$chat_id = "@DolarParallel";
$sql = "SELECT tasa FROM DICOM WHERE id = 5";
$result = $link->query($sql);

if ($result->num_rows > 0 && $text != "") {
    $OldText = mysqli_fetch_assoc($result)['tasa'];
	if ($text !== $OldText) {
		if (!preg_match('/[a-zA-Z]/', $text)) {
			$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 5";
			if ($link->query($sql) === TRUE) {
				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=`$text`&parse_mode=markdown");
			} else {
				file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=error".$conn->error); 
			}
		} else {
			file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
		}
		

	}
} else {
	file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
    file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=0 Results");
}


?>
