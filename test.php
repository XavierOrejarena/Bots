#!/usr/bin/env php
<?php
define('BOT_TOKEN', '1228539660:AAENYRaMlIR84VtmTSO5MHg13saDL3epHkk');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');

function apiRequestJson($method, $parameters) {
  if (!is_string($method)) {
    error_log("Method name must be a string\n");
    return false;
  }

  if (!$parameters) {
    $parameters = array();
  } else if (!is_array($parameters)) {
    error_log("Parameters must be an array\n");
    return false;
  }

  $parameters["method"] = $method;

  $handle = curl_init(API_URL);
  curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 5);
  curl_setopt($handle, CURLOPT_TIMEOUT, 60);
  curl_setopt($handle, CURLOPT_POST, true);
  curl_setopt($handle, CURLOPT_POSTFIELDS, json_encode($parameters));
  curl_setopt($handle, CURLOPT_HTTPHEADER, array("Content-Type: application/json"));

  return exec_curl_request($handle);
}

function exec_curl_request($handle) {
  $response = curl_exec($handle);

  if ($response === false) {
    $errno = curl_errno($handle);
    $error = curl_error($handle);
    error_log("Curl returned error $errno: $error\n");
    curl_close($handle);
    return false;
  }

  $http_code = intval(curl_getinfo($handle, CURLINFO_HTTP_CODE));
  curl_close($handle);

  if ($http_code >= 500) {
    // do not wat to DDOS server if something goes wrong
    sleep(10);
    return false;
  } else if ($http_code != 200) {
    $response = json_decode($response, true);
    error_log("Request has failed with error {$response['error_code']}: {$response['description']}\n");
    if ($http_code == 401) {
      throw new Exception('Invalid access token provided');
    }
    return false;
  } else {
    $response = json_decode($response, true);
    if (isset($response['description'])) {
      error_log("Request was successful: {$response['description']}\n");
    }
    $response = $response['result'];
  }

  return $response;
}

include "connect.php";
$chat_id = 149273661;
$text = "COMPRA\t\tVENTA\n";
$sql = "SELECT COMPRA,VENTA FROM LocalBitcoins";
$result = $link->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    $text = $text. $row["COMPRA"]. "\t\t" . $row["VENTA"]."\n";
  }
} else {
  $text = "0 results";
}

apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "<pre>".$text."</pre>", 'parse_mode' => 'HTML'));

function getBTCValue() {
  $BINANCE_BTCUSDT = file_get_contents("https://www.bitmex.com/api/v1/trade/bucketed?binSize=1m&partial=true&count=100&reverse=true");
  $BINANCE_BTCUSDT = json_decode($BINANCE_BTCUSDT, true);

  foreach ($BINANCE_BTCUSDT as $coin) {
      if ($coin['symbol'] == 'XBTUSD') {
          return round($coin['open'],2);
          break;
      }
  }
  
  return 0;
}

function getS() {
  include "connect.php";
  $priceBTC = getBTCValue();
  $URL = file_get_contents("https://localbitcoins.com/buy-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  $i = 0;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES' && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $COMPRA = number_format(round($oferta['data']['temp_price']/$priceBTC));
      $sql = "UPDATE LocalBitcoins SET COMPRA='$COMPRA' WHERE id='$i'";
      if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
      } else {
        echo "Error updating record: " . $link->error;
      }
      $i++;
      if ($i > 9) break;
    }
  }
  
  $URL = file_get_contents("https://localbitcoins.com/sell-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  
  $i = 0;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES'  && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $VENTA = number_format(round($oferta['data']['temp_price']/$priceBTC));
      $sql = "UPDATE LocalBitcoins SET VENTA='$VENTA' WHERE id='$i'";
      if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
      } else {
        echo "Error updating record: " . $link->error;
      }
      $i++;
      if ($i > 9) break;
    }
  }
}

getS();
?>