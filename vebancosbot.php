#!/usr/bin/env php
<?php
//@Venezuela2Codebot
define('BOT_TOKEN', '2130044368:');
define('TOKEN_BOT', 'AAF35Fhz_PTfVqUxK_XECjr2oMvzvJ7IQP4');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.TOKEN_BOT.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/vebancosbot.php');

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

$bancos = array(
'0102' => 'Banco de Venezuela, S.A.C.A.',
'0104' => 'Venezolano de Crédito',
'0105' => 'Mercantil',
'0108' => 'Provincial',
'0114' => 'Bancaribe',
'0115' => 'Exterior',
'0116' => 'Occidental de Descuento',
'0128' => 'Banco Caroní',
'0134' => 'Banesco',
'0138' => 'Banco Plaza',
'0151' => 'BFC Banco Fondo Común',
'0156' => '100% Banco',
'0157' => 'Del Sur',
'0163' => 'Banco del Tesoro',
'0166' => 'Banco Agrícola de Venezuela',
'0168' => 'Bancrecer',
'0169' => 'Mi Banco',
'0171' => 'Banco Activo',
'0172' => 'Bancamiga',
'0174' => 'Banplus',
'0175' => 'Bicentenario del Pueblo',
'0177' => 'Banfanb',
'0191' => 'BNC Nacional de Crédito',);

// $text = 'Feliciano tapia
// 23.768.489\
// 0134-0404-62-4041043346/
// Cta corriente
// 0414-189 25 15';

// $text = ucwords($text);
// $text = str_replace("-", "", $text);
// $text = str_replace(".", "", $text);
// $text = str_replace("/", "", $text);
// $text = str_replace("\\", "", $text);
// $text = str_replace("Corriente", "", $text);
// $text = str_replace("Ahorro", "", $text);
// $text = str_replace("Cuenta", "", $text);
// $text = str_replace("Cta", "", $text);
// $text = str_replace("Ci", "", $text);
// // print_r($text);
// // preg_match_all('/[a-zA-Z]/', $text, $matches);
// $nombre = preg_replace("/[^a-zA-Z ]+/", "", $text);
// $nombre = str_replace("\n", "", $matches);

// $text = str_replace(" ", "", $text);
// preg_match_all('!\d+!', $text, $matches);

// // // echo $bancos['0134']. "\n";
// foreach ($matches[0] as $code){
//     // print_r($code);
//     $Banco = strpos($code, '01');
//     if($Banco !== false){
//         $Banco = substr($code, $Banco, 20);
//         if (!is_numeric($Banco)){
//             $Banco = '';
//         }
//     }
//     if(strpos($code, '0414') !== false){
//         $PagoMovil = substr($code, strpos($code, '0414'), 10);
//         if (!is_numeric($PagoMovil)){
//             $PagoMovil = '';
//         }
//     }else if(strpos($code, '0424') !== false){
//         $PagoMovil = substr($code, strpos($code, '0424'), 10);
//         if (!is_numeric($PagoMovil)){
//             $PagoMovil = '';
//         }
//     }else if(strpos($code, '0416') !== false){
//         $PagoMovil = substr($code, strpos($code, '0416'), 10);
//         if (!is_numeric($PagoMovil)){
//             $PagoMovil = '';
//         }
//     }else if(strpos($code, '0426') !== false){
//         $PagoMovil = substr($code, strpos($code, '0426'), 10);
//         if (!is_numeric($PagoMovil)){
//             $PagoMovil = '';
//         }
//     }else if(strpos($code, '0412') !== false){
//         $PagoMovil = substr($code, strpos($code, '0412'), 10);
//         if (!is_numeric($PagoMovil)){
//             $PagoMovil = '';
//         }
//     }
// }

function processMessage($message) {
  // process incoming message
  $message_id = $message['message_id'];
  $chat_id = $message['chat']['id'];
  if ($chat_id == 149273661) {
    // incoming text message
    $text = $message['text'];

    if (strpos($text, "/start") === 0) {
      apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => 'Go!'));
    } else {
        $text = ucwords($text);
        $text = str_replace("-", "", $text);
        $text = str_replace(".", "", $text);
        $text = str_replace("/", "", $text);
        $text = str_replace("\\", "", $text);
        $text = str_replace("Corriente", "", $text);
        $text = str_replace("Ahorro", "", $text);
        $text = str_replace("Cuenta", "", $text);
        $text = str_replace("Cta", "", $text);
        $text = str_replace("Ci", "", $text);
        $nombre = preg_replace("/[^a-zA-Z ]+/", "", $text);
        // $nombre = str_replace("\n", "", $matches);
        
        // $text = str_replace(" ", "", $text);
        preg_match_all('!\d+!', $text, $matches);
        foreach ($matches[0] as $code){
            if (strlen($code) == 7 or strlen($code) == 8){
                $cedula = $code;
            }
            $cuenta = strpos($code, '01');
            if($cuenta !== false){
                $cuenta = substr($code, $cuenta, 20);
                if (!is_numeric($cuenta)){
                    $cuenta = '';
                }
            }
            if(strpos($code, '0414') !== false){
                $PagoMovil = substr($code, strpos($code, '0414'), 10);
                if (!is_numeric($PagoMovil)){
                    $PagoMovil = '';
                }
            }else if(strpos($code, '0424') !== false){
                $PagoMovil = substr($code, strpos($code, '0424'), 10);
                if (!is_numeric($PagoMovil)){
                    $PagoMovil = '';
                }
            }else if(strpos($code, '0416') !== false){
                $PagoMovil = substr($code, strpos($code, '0416'), 10);
                if (!is_numeric($PagoMovil)){
                    $PagoMovil = '';
                }
            }else if(strpos($code, '0426') !== false){
                $PagoMovil = substr($code, strpos($code, '0426'), 10);
                if (!is_numeric($PagoMovil)){
                    $PagoMovil = '';
                }
            }else if(strpos($code, '0412') !== false){
                $PagoMovil = substr($code, strpos($code, '0412'), 10);
                if (!is_numeric($PagoMovil)){
                    $PagoMovil = '';
                }
            }
        }
        apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => $nombre));
        apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => $cuenta));
        apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => $cedula));
        apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => $PagoMovil));
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
  exit;
}

if (isset($update["message"])) {
  processMessage($update["message"]);
}