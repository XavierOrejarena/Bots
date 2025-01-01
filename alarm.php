#!/usr/bin/env php
<?php
	$tkn = "411509742:";
	$token = 'AAFKzBXmOO0fx8e3bXDHBo4tj-QMazfre2E';
	$api = $tkn.$token;
	function sendMessage($chat_id, $text)
	{
	    global $api;
	    $get = file_get_contents("https://api.telegram.org/bot$api/sendMessage?chat_id=$chat_id&text=".urlencode($text));
	}

	include "connect.php";
	
	$result = mysqli_query($link, "SELECT * FROM alarms_binance");
	while($row = mysqli_fetch_array($result)){
		$chat_id = $row['chat_id'];
		$coin = $row['coin'];
		$seted_price = $row['seted_price'];
		$type = $row['type'];
		$row_num = $row['row_num'];
		$arrContextOptions=array(
		    "ssl"=>array(
		    "verify_peer"=>false,
		    "verify_peer_name"=>false,
		    ),
		);
		$data = json_decode(file_get_contents("https://api.binance.com/api/v1/ticker/price?symbol=$coin", false, stream_context_create($arrContextOptions))['price'];
		// $price = json_decode(file_get_contents("https://api.binance.com/api/v1/ticker/price?symbol=$coin"), true)['price'];
		if (is_numeric($price)) {
			$seted_price = floatval($seted_price);
			$price = floatval($price);
			if ($price >= $seted_price and $type == "high") {
				sendMessage($chat_id, "/".$coin." just reached the price of ".$seted_price);
				mysqli_query($link, "DELETE FROM alarms_binance WHERE row_num ='$row_num'");
			}
			elseif ($price <= $seted_price and $type == "low") {
				sendMessage($chat_id, "/".$coin." just reached the price of ".$seted_price);
				mysqli_query($link, "DELETE FROM alarms_binance WHERE row_num ='$row_num'");
			}
		}

 	}
?>
