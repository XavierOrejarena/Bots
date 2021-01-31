#!/usr/bin/env php
<?php

define('BOT_TOKEN', '1611564155:AAFef7H1bWwk3ibj5M-vO5xGb44sbFiowlk');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/monterobarbot.php');

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

    if (strpos($text, "/start") === 0) {
      apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => 'Hola, ¿qué desea?', 'reply_markup' => array(
        'keyboard' => array(array('Menu', 'Precios'), array('Ubicación', 'Ordenar'), array('Promociones'),array('Redes Sociales')),
        'one_time_keyboard' => true,
        'resize_keyboard' => true)));
    } else if ($text === "Hello" || $text === "Ordenar") {
      apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => 'Hola, ¿qué desea?', 'reply_markup' => array(
        'keyboard' => array(array('Hamburguesas', 'Pizzas'),array('Bebidas', 'Pepitos')),
        'one_time_keyboard' => true,
        'resize_keyboard' => true)));
    } else if ($text === "Hello" || $text === "Promociones") {
      apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => 'Hola, ¿qué desea?', 'reply_markup' => array(
        'keyboard' => array(array('Montero', 'Terios'),array('Pepitos', '4x4'), array('Super Duty', 'En nuestro local'),),
        'one_time_keyboard' => true,
        'resize_keyboard' => true)));  
    } else if (strpos($text, "Hamburguesas") === 0) {
        apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => '¿Cantidad?', 'reply_markup' => array(
        'keyboard' => array(array('1', '2', '3'),array('4', '5', '6'),array('7', '8', '9')),
        'one_time_keyboard' => true,
        'resize_keyboard' => true)));
    } else if ($text === "Hello" || $text === "Ubicación") {
        $token = BOT_TOKEN;
        file_get_contents("https://api.telegram.org/bot$token/sendlocation?chat_id=$chat_id&&latitude=10.457583618462683&longitude=-66.82886919591881"); 
    } else if ($text === "Hello" || $text === "Redes Sociales") {
        apiRequestWebhook("sendMessage", array('chat_id' => $chat_id, "reply_to_message_id" => $message_id, "text" => 'https://www.instagram.com/monterobar97'));
    } else {
      apiRequestWebhook("sendMessage", array('chat_id' => $chat_id, "reply_to_message_id" => $message_id, "text" => 'Cool'));
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