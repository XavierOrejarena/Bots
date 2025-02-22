#!/usr/bin/env php
<?php

define('PT1', '7330372927:');
define('PT2', 'AAEex8gfTnGTnCUvS2F2UvIzXCFdSgsBX70');
define('API_URL', 'https://api.telegram.org/bot'.PT1.PT2.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/donpremiumbot.php');

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

  $payload = json_encode($parameters);
  header('Content-Type: application/json');
  header('Content-Length: '.strlen($payload));
  echo $payload;

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
  if (isset($message['text'])) {
    // incoming text message
    $text = $message['text'];
    if ($text == '/start'){
      $data = file_get_contents("https://criptodolar.net/cotizacion/dolar-monitor");
      preg_match_all('/5d5dfaa6639f395c7fd11d13/', $data, $matches, PREG_OFFSET_CAPTURE);
      $dolar = substr($data, $matches[0][0][1]+31,5);
      $NetflixBs = 3*$dolar;
      $DisneyBs = 3*$dolar;
      $HBOMaxBs = 2*$dolar;
      $AmazonPrimeBs = 2*$dolar;
      $ParamountBs = 2*$dolar;
      $CrunchyrollBs = 3*$dolar;
      $YouTube1Bs = 4*$dolar;
      $YouTube12Bs = 20*$dolar;
      $Spotify1Bs = 5*$dolar;
      $Spotify3Bs = 12*$dolar;

      $text = "1 PERFIL x 1 MES: 
🔴 Netflix: $NetflixBs Bs
🔵 Disney+: $DisneyBs Bs
🟣 HBO Max: $HBOMaxBs Bs
🟢 Amazon Prime: $AmazonPrimeBs Bs
🔵 Paramount: $ParamountBs Bs
🟠 Crunchyroll: $CrunchyrollBs Bs
 
CUENTA COMPLETA: 
🔴 YouTube 1 mes: $YouTube1Bs Bs
🔴 YouTube 12 meses: $YouTube12Bs Bs
🟢 Spotify 1 mes: $Spotify1Bs Bs
🟢 Spotify 3 meses: $Spotify3Bs Bs";



      apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => "`".$text."`", 'parse_mode' => 'MarkDown'));
    }
  } else {
    apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => 'I understand only text messages'));
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
