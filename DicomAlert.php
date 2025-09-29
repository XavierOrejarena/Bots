#!/usr/bin/env php
<?php
include "connect.php";

$token = '16396100:AAG_6y_pnkgYCKNRMyFVHow2eefR719DfCk';
$chat_id = '@AlertaBCV';
$sql = "SELECT tasa FROM DICOM WHERE id = 1";
$result = $link->query($sql);

$text = USD();

if ($result->num_rows > 0 && $text) {
    $OldText = mysqli_fetch_assoc($result)['tasa'];
	if ($text !== $OldText) {
		if (!preg_match('/[a-zA-Z]/', $text)) {
			$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 1";
			if ($link->query($sql) === TRUE) {
				// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=`$text`&parse_mode=markdown");
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

// $text = json_decode(file_get_contents("https://exchange.vcoud.com/coins/latest?type=bolivar&base=usd"), true)[0]['price'];

file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text xD");

$chat_id = '@DolarParallel';
$sql = "SELECT tasa FROM DICOM WHERE id = 5";
$result = $link->query($sql);

$text = EUR();

if ($result->num_rows > 0 && $text) {
    $OldText = mysqli_fetch_assoc($result)['tasa'];
	if ($text != $OldText) {
		$sql = "UPDATE DICOM SET tasa = '$text' WHERE id = 5";
		if ($link->query($sql) === TRUE) {
			// file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=$chat_id&text=`$text`&parse_mode=markdown");
		} else {
			file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=error".$conn->error);
		}
	}
} else {
	file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=$text"); 
    file_get_contents("https://api.telegram.org/bot7$token/sendMessage?chat_id=149273661&text=? Results");
}

function USD(){
	$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    	),
    "http" => array(
        "method" => "GET", // HTTP request method
        "header" => "User-Agent: MyCustomAgent/1.0\r\n", // Custom HTTP headers
        "timeout" => 500, // Request timeout in seconds
        // ... other HTTP options
    ),
	);  
	$data = file_get_contents("http://bcv.org.ve", false, stream_context_create($arrContextOptions));
	preg_match_all('/> USD</', $data, $matches, PREG_OFFSET_CAPTURE);
	$text = substr($data, $matches[0][0][1]+122, 11);
	$text = (string)$text;
	print_r("USD: ".$text."\n");
	if ($text =! ""){
		return $text;
		echo "oolllooo";
	} else{
		return USD();
	}
}

function EUR(){
	$arrContextOptions=array(
    "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false,
    ),
    "http" => array(
        "method" => "GET", // HTTP request method
        "header" => "User-Agent: MyCustomAgent/1.0\r\n", // Custom HTTP headers
        "timeout" => 500, // Request timeout in seconds
        // ... other HTTP options
    ),
	);  
	$data = file_get_contents("http://bcv.org.ve", false, stream_context_create($arrContextOptions));
	preg_match_all('/EUR/', $data, $matches, PREG_OFFSET_CAPTURE);
	$text = substr($data, $matches[0][0][1]+104, 11);
	$text = (string)$text;
	print_r("EUR: ".$text."\n");
	if ($text =! ""){
		echo "loool";
		return $text;
	} else{
		return EUR();
	}
}

?>
