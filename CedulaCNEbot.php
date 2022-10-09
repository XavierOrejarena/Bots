#!/usr/bin/env php
<?php
// @CedulaCNEbot
define('BOT_TOKEN', '5215385282:');
define('TOKEN_BOT', 'AAH7wHVbdT8qxqwKNG-rTafjoAEJCqLkEGU');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.TOKEN_BOT.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/CedulaCNEbot.php');

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
      apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => 'Hello'));
    } else if ($text === "Hello" || $text === "Hi") {
      apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => 'Nice to meet you'));
    } else if (strpos($text, "/stop") === 0) {
      // stop now
    } else {
      $cedula = $text;
      $result = file_get_contents("http://www.cne.gob.ve/web/registro_electoral/ce.php/web/registro_electoral/imprimir_datos_elector.php?nacionalidad=V&cedula=$cedula", false);

      $persona = array();

      preg_match_all('/<td align="left"><b>/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][2][1], 100);
      $persona['Nombre'] = substr($text, strpos($text,"<b>")+3,strpos($text,"</b>")-strlen($text));

      preg_match_all('/<td align="left">/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][5][1], 100);
      $persona['Estado'] = substr($text, strpos($text,'">')+2,strpos($text,"</td>")-strlen($text));

      preg_match_all('/<td align="left">/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][7][1], 100);
      $persona['Municipio'] = substr($text, strpos($text,'">')+2,strpos($text,"</td>")-strlen($text));


      preg_match_all('/<td align="left">/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][9][1], 100);
      $persona['Parroquia'] = substr($text, strpos($text,'">')+2,strpos($text,"</td>")-strlen($text));

      preg_match_all('/<td align="left">/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][11][1], 100);
      $persona['Centro'] = substr($text, strpos($text,'F">')+3,strpos($text,"</font>")-strlen($text));

      preg_match_all('/<td align="left">/', $result, $matches, PREG_OFFSET_CAPTURE);
      $text = substr($result, $matches[0][13][1], 300);
      $persona['Direccion'] = substr($text, strpos($text,'F">')+3,strpos($text,"</font>")-strlen($text));
      apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => serialize($persona)));
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