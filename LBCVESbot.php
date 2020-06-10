#!/usr/bin/env php
<?php

define('BOT_TOKEN', '1228539660:AAENYRaMlIR84VtmTSO5MHg13saDL3epHkk');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');
define('WEBHOOK_URL', 'https://xavier.mer.web.ve/LBCVESbot.php');

function getS() {
  $rdata = array("COMPRA\t\tVENTA");
  $priceBTC = getBTCValue();
  $URL = file_get_contents("https://localbitcoins.com/buy-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  $text = '';
  $i = 0;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES' && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $rdata[] = number_format(round($oferta['data']['temp_price']/$priceBTC));
      $i++;
      if ($i > 9) break;
    }
  }
  
  $URL = file_get_contents("https://localbitcoins.com/sell-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  
  $i = 1;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES'  && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $rdata[$i] = $rdata[$i]."\t\t\t".number_format(round($oferta['data']['temp_price']/$priceBTC));
      $i++;
      if ($i > 10) break;
    }
  }

  foreach ($rdata as $key) {
    $text = $text.$key."\n";
  }
  return $text."\n\n$priceBTC";

}

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

function apiRequestWebhook($method, $parameters) {
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

  header("Content-Type: application/json");
  echo json_encode($parameters);
  return true;
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

function apiRequest($method, $parameters) {
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

  foreach ($parameters as $key => &$val) {
    // encoding to JSON array parameters, for example reply_markup
    if (!is_numeric($val) && !is_string($val)) {
      $val = json_encode($val);
    }
  }
  $url = API_URL.$method.'?'.http_build_query($parameters);

  $handle = curl_init($url);
  curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 5);
  curl_setopt($handle, CURLOPT_TIMEOUT, 60);

  return exec_curl_request($handle);
}

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

function processMessage($message) {
  // process incoming message
  $message_id = $message['message_id'];
  $chat_id = $message['chat']['id'];
  $text = $message['text'];

  if ($text == '/s') {
    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "<pre>".getS()."</pre>", 'parse_mode' => 'HTML'));
  } else if ($text == '/start'){
    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "El único comando /s te muestra la tasa del dolar en VES dividiendo las 10 primeras ofertas en localbitcoins.com entre la tasa del BTC segun Bitmex.com"));
  }
  
}

if (php_sapi_name() == 'cli') {
  // if run from console, set or delete webhook
  apiRequest('setWebhook', array('url' => isset($argv[1]) && $argv[1] == 'delete' ? '' : WEBHOOK_URL));
  exit;
}


$content = file_get_contents("php://input");
$update = json_decode($content, true);

if (!$update) {
  // receive wrong update, must not happen
  exit;
}

if (isset($update["message"])) {
  processMessage($update["message"]);
}