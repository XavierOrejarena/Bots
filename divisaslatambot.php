#!/usr/bin/env php
<?php

define('BOT_TOKEN', '1224010504:AAE42bCZS8A6rhmTHq15EnFkogVARy9utnU');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');
define('WEBHOOK_URL', 'https://xavier.mer.web.ve/divisaslatambot.php');
define('appID', '36cab38e64694c14bc52931f371b4fbc');
define('API_URL_RATES', 'https://openexchangerates.org/api/latest.json?app_id='.appID);

function gen_uuid() {
  return sprintf( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
      mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ),
      mt_rand( 0, 0xffff ),
      mt_rand( 0, 0x0fff ) | 0x4000,
      mt_rand( 0, 0x3fff ) | 0x8000,
      mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff )
  );
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


  if ($text == "/start") {
    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => 'La función de este bot es unicamente hacer cambio entre divisas, ejemplo para convertir 100 EUR a USD solo hace falta escribir:

"100 EUR"

Ahora si quieres convertir 50 CLP a VES solo debes escribir:

"50 CLP VES"

Obviamente sin las comillas, no seas tont@

Los datos son obtenidos de openexchangerates.org
No se hace distinción entre mayúsculas.'));
  }else{
    $size = sizeof(str_word_count($text, 1, "0123456789."));
    $first = strtoupper(str_word_count($text, 1, "0123456789.")[1]);
    $second = strtoupper(str_word_count($text, 1, "0123456789.")[2]);

    if (($size == 2 && $first != 'USD') || ($size == 3 && $second == 'USD')) {
      $data = file_get_contents(API_URL_RATES);
      $data = json_decode(utf8_encode($data), true);
      $amount = str_word_count($text, 1, "0123456789.")[0];
      $result = $amount/$data['rates'][$first];
    } elseif ($size == 3) {
      $data = file_get_contents(API_URL_RATES);
      $data = json_decode(utf8_encode($data), true);
      $amount = str_word_count($text, 1, "0123456789.")[0];
      $result_1 = $data['rates'][$first];
      $result_2 = $data['rates'][$second];
      $result = $amount*$result_2/$result_1;
    }
    $result = number_format(round($result,2), 2, '.', ',');
    apiRequestJson("sendMessage", array('chat_id' => $chat_id, "text" => $result));

	}
}

if (php_sapi_name() == 'cli') {
  // if run from console, set or delete webhook
  apiRequest('setWebhook', array('url' => isset($argv[1]) && $argv[1] == 'delete' ? '' : WEBHOOK_URL));
  exit;
}

function processQuery($inline_query)
{
    $text = strtoupper($inline_query['query']);
    $query_id = $inline_query['id'];
    $results = [];
    if (!empty($inline_query['query'])) {
        
    }

    if (empty($inline_query['query'])) {
        $results[] = [
            'type'         => 'article',
            'id'           => '0',
            'title'        => 'Esperando una consulta...',
            'message_text' => 'Tienes que escribir monto DIVISA1 DIVISA2',
            'description'  => 'Ejemplo: 100 USD EUR',
        ];
    }else {
      $size = sizeof(str_word_count($text, 1, "0123456789."));
      $first = str_word_count($text, 1, "0123456789.")[1];
      $second = str_word_count($text, 1, "0123456789.")[2];

      if (($size == 2 && $first != 'USD') || ($size == 3 && $second == 'USD')) {
        $data = file_get_contents(API_URL_RATES);
        $data = json_decode(utf8_encode($data), true);
        $amount = str_word_count($text, 1, "0123456789.")[0];
        $result = $amount/$data['rates'][$first];
      } elseif ($size == 3) {
        $data = file_get_contents(API_URL_RATES);
        $data = json_decode(utf8_encode($data), true);
        $amount = str_word_count($text, 1, "0123456789.")[0];
        $result_1 = $data['rates'][$first];
        $result_2 = $data['rates'][$second];
        $result = $amount*$result_2/$result_1;
      }
      $result = number_format(round($result,2), 2, '.', ',');

        $results[] = [
        'type'         => 'article',
        'id'           => gen_uuid(),
        'title'        => $amount." ".$first." Equivale a:",
        'description'  => $result." ".$second,
        'message_text' => $amount." ".$first." = ".$result." ".$second,
        ];
    }
    
    apiRequest('answerInlineQuery', array('inline_query_id' => $inline_query['id'], 'results' => $results, 'cache_time' => 0));
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

if (isset($update['inline_query'])) {
  processQuery($update['inline_query']);
}