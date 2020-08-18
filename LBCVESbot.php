#!/usr/bin/env php
<?php

define('BOT_TOKEN', '1228539660:AAENYRaMlIR84VtmTSO5MHg13saDL3epHkk');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/LBCVESbot.php');

function saveUser($user) {
  include "connect.php";
  $chat_id = $user['id'];
  $first_name = $user['first_name'];
  $last_name = $user['last_name'];
  $username = $user['username'];
  $result = mysqli_query($link, "SELECT chat_id FROM users WHERE chat_id = '$chat_id'");
  if (mysqli_num_rows($result) == 0){
      mysqli_query($link, "INSERT INTO users (chat_id, first_name, last_name, username, LBCVESbot) VALUES ('$chat_id', '$first_name', '$last_name', '$username', 1)");
  }else {
      mysqli_query($link, "UPDATE users SET LBCVESbot = LBCVESbot+1, first_name = '$first_name', last_name = '$last_name', username = '$username' WHERE chat_id = '$chat_id';");
  }
  mysqli_close($link);
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

  if ($text == '/s' || $text == '/s@LBCVESbot') {
    include "connect.php";
    $text = "COMPRA\t\tVENTA\n";
    $sql = "SELECT COMPRA,VENTA FROM LocalBitcoins";
    $result = $link->query($sql);
    $i = 0;

    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        $i++;
        if ($i > 10) {
          $text = $text. "\n\nUSD/BTC = ";
        }
        $text = $text. $row["COMPRA"]. "\t\t" . $row["VENTA"]."\n";
      }
    } else {
      $text = "0 results";
    }

    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "<pre>".$text."</pre>", 'parse_mode' => 'HTML'));
  } else if ($text == '/start'){
    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "Comando: /s

Muestra la tasa del dólar en VES dividiendo las 10 primeras ofertas en localbitcoins.com entre la tasa del BTC según Bitmex.com

Comando: /r

Muestra la tasa del dolar en VES segun varios indicadores."));
  } else if ($text == '/r' || $text == '/r@LBCVESbot') {
    include "connect.php";
    $text = '';
    $sql = "SELECT INDICADOR,TASA FROM Dolar";
    $result = $link->query($sql);
    $i = 0;

    if ($result->num_rows > 0) {
      while($row = $result->fetch_assoc()) {
        $i++;
        $str =  $row["INDICADOR"]."                                                                ";
        $str = substr_replace($str,$row["TASA"],15);
        $text = $text."\n".$str;
      }
    } else {
      $text = "0 results";
    }

    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => "<pre>".$text."</pre>", 'parse_mode' => 'HTML'));
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
  saveUser($update['message']['from']);
}