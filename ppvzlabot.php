#!/usr/bin/env php
<?php
//@ppvzlabot
define('PT1', '533073153:');
define('PT2', 'AAEZ5fAbuewT3eFryw5l3wGLHgk4zXbAmzs');
define('API_URL', 'https://api.telegram.org/bot'.PT1.PT2.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/ppvzlabot.php');

function gen_uuid() {
    return sprintf( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
        mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ),
        mt_rand( 0, 0xffff ),
        mt_rand( 0, 0x0fff ) | 0x4000,
        mt_rand( 0, 0x3fff ) | 0x8000,
        mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff ), mt_rand( 0, 0xffff )
    );
}

function sendMessage($chat_id, $text) {
    apiRequest('sendMessage', ['chat_id' => $chat_id, 'text' => $text, 'parse_mode' => 'MarkDown']);
}

function saveUser($user) {
    include "connect.php";
    $chat_id = $user['id'];
    $first_name = $user['first_name'];
    $last_name = $user['last_name'];
    $username = $user['username'];
    $result = mysqli_query($link, "SELECT chat_id FROM users WHERE chat_id = '$chat_id'");
    if (mysqli_num_rows($result) == 0){
        mysqli_query($link, "INSERT INTO users (chat_id, first_name, last_name, username, ppvzlabot) VALUES ('$chat_id', '$first_name', '$last_name', '$username', 1)");
    }else {
        mysqli_query($link, "UPDATE users SET ppvzlabot = ppvzlabot+1, first_name = '$first_name', last_name = '$last_name', username = '$username' WHERE chat_id = '$chat_id';");
    }
    mysqli_close($link);
}

function apiRequestWebhook($method, $parameters)
{
    if (!is_string($method)) {
        error_log("El nombre del método debe ser una cadena de texto\n");
        return false;
    }
    if (!$parameters) {
        $parameters = [];
    } elseif (!is_array($parameters)) {
        error_log("Los parámetros deben ser un arreglo/matriz\n");
        return false;
    }
    $parameters['method'] = $method;
    header('Content-Type: application/json');
    echo json_encode($parameters);
    return true;
}

function exec_curl_request($handle)
{
    $response = curl_exec($handle);
    if ($response === false) {
        $errno = curl_errno($handle);
        $error = curl_error($handle);
        error_log("Curl retornó un error $errno: $error\n");
        curl_close($handle);
        return false;
    }
    $http_code = intval(curl_getinfo($handle, CURLINFO_HTTP_CODE));
    curl_close($handle);
    if ($http_code >= 500) {
        // do not wat to DDOS server if something goes wrong
    sleep(10);
        return false;
    } elseif ($http_code != 200) {
        $response = json_decode($response, true);
        error_log("La solicitud fallo con el error {$response['error_code']}: {$response['description']}\n");
        if ($http_code == 401) {
            throw new Exception('El token provisto es inválido');
        }
        return false;
    } else {
        $response = json_decode($response, true);
        if (isset($response['description'])) {
            error_log("La solicitud fue exitosa: {$response['description']}\n");
            echo "<h3>seted Webhook</h1>";
        }
        $response = $response['result'];
    }
    return $response;
}

function apiRequest($method, $parameters)
{
    if (!is_string($method)) {
        error_log("El nombre del método debe ser una cadena de texto\n");
        return false;
    }
    if (!$parameters) {
        $parameters = [];
    } elseif (!is_array($parameters)) {
        error_log("Los parámetros deben ser un arreglo/matriz\n");
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
    curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 0);
    curl_setopt($handle, CURLOPT_TIMEOUT, 0);
    return exec_curl_request($handle);
}

function apiRequestJson($method, $parameters)
{
    if (!is_string($method)) {
        error_log("El nombre del método debe ser una cadena de texto\n");
        return false;
    }
    if (!$parameters) {
        $parameters = [];
    } elseif (!is_array($parameters)) {
        error_log("Los parámetros deben ser un arreglo/matriz\n");
        return false;
    }
    $parameters['method'] = $method;
    $handle = curl_init(API_URL);
    curl_setopt($handle, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($handle, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($handle, CURLOPT_TIMEOUT, 60);
    curl_setopt($handle, CURLOPT_POSTFIELDS, json_encode($parameters));
    curl_setopt($handle, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    return exec_curl_request($handle);
}

function processQuery($inline_query)
{
    $query_id = $inline_query['id'];
    $results = [];
    if (!empty($inline_query['query'])) {
        $text = $inline_query['query'];
        $text = str_replace(',', '.', $text);
        $text   = str_replace('x','*',$text);
        $text   = str_replace('X','*',$text);
        $USD = str_word_count($text, 1, '0123456789.')[0];
        $BS = str_word_count($text, 1, '0123456789.')[1];
        $signal = str_word_count($text, 1, '*xX/\def')[0];
        $BS = pow(1000,strlen(stristr($BS, 'k')))*(real)$BS;
        $emoji = "\xE2\x98\x95: Bs ".number_format($BS, 2, ',', '');
    }

    if (empty($inline_query['query'])) {
        $results[] = [
            'type'         => 'article',
            'id'           => '0',
            'title'        => 'Esperando una consulta...',
            'message_text' => 'Tienes que escribir el monto*tasa.
            Ejemplo: 50*7500',
            'description'  => 'Ejemplo: 50*7500',
        ];
    }
    else if ($signal == 'x' || $signal == '*' || is_null($signal) || $signal == 'X') {
        $receive = round(($USD-$USD*(0.054)-0.3), 2);
        $sent = round((100*($USD+0.3)/94.6),2);
        if ($BS < 2 ) {
            $Total = "`".number_format($receive*$BS, 2, '.', '')."` $";
            $emoji = "％: ".number_format($BS, 2, '.', '');
        }else {
            $Total = "Bs `".number_format($receive*$BS, 2, ',', '')."`";
        }
        if ($BS) {
            $message_text1 = "Envían: `$USD` $
Llegarán: `$receive` $
$emoji
Total: $Total";
            if ($BS < 2 ) {
                $Total = "`".number_format($USD*$BS, 2, '.', '')."` $";
                $emoji = "％: ".number_format($BS, 2, '.', '');
            }else {
                $Total = "Bs `".number_format($USD*$BS, 2, ',', '')."`";
            }
            $message_text2 = "Envían: `$sent` $
Llegarán: `$USD` $
$emoji
Total: $Total";
        } else {
            $message_text1 = "Envían: `$USD` $
Llegarán: `$receive` $";
            $message_text2 = "Envían: `$sent` $
Llegarán: `$USD` $";
        }
        $results[] = [
        'type'         => 'article',
        'id'           => gen_uuid(),
        'title'        => "Si envían: $$USD",
        'message_text' => $message_text1,
        'description'  => "Llegarán: $$receive",
        'parse_mode' => 'MarkDown',
        ];
        $results[] = [
        'type'         => 'article',
        'id'           => gen_uuid(),
        'title'        => "Para que lleguen: $$USD",
        'message_text' => $message_text2,
        'description'  => "Deben enviar: $sent",
        'parse_mode' => 'MarkDown',
        ];
    }
    else if ($signal == "/" || $signal == '\\') {
        $sent = round((100*(($USD/$BS)+0.3)/94.6),2);
        $receive = round($USD/$BS,2);
        if ((fmod($USD,    1) !== 0.00) ) {
            $Total = number_format($USD, 2, ',', '');
        }else {
            $Total = number_format($USD, 2, ',', '');
        }
        $results[] = [
    'type'         => 'article',
    'id'           => gen_uuid(),
    'title'        => "Para pagar $USD Bs.",
    'message_text' => "Envían: `$sent` $
Llegarán: `$receive` $
$emoji
Total: Bs `$Total`",
    'description'  => "Deben enviar $sent",
    'parse_mode' => 'MarkDown',
    ];
    }
    apiRequest('answerInlineQuery', array('inline_query_id' => $inline_query['id'], 'results' => $results, 'cache_time' => 0));
}

if (php_sapi_name() == 'cli') {
    // if run from console, set or delete webhook
  apiRequest('setWebhook', ['url' => isset($argv[1]) && $argv[1] == 'delete' ? '' : WEBHOOK_URL]);
    exit;
}

$malaPaga = array('Xavier','440413394');

function processMessage($message) {
    $message_id = $message['message_id'];
    $chat_id = $message['chat']['id'];
    $text = $message['text'];
    $text = str_replace(',', '.', $text);
    $id = strval($message['from']['id']);

    // sendMessage($chat_id, $message['from']['id']);
    // $URL = API_URL."sendMessage?chat_id=".$chat_id."&text=`".$text."`&parse_mode=MarkDown";
    // file_get_contents($URL);

    if (in_array($message['from']['first_name'], $malaPaga)) {
        sendMessage($chat_id, "Hola ".$message['from']['first_name'].", comunícate con @OrejarenaXavier para activar el bot.");
    }else {
        if(strtolower($text) == "/start") {
        sendMessage($chat_id, "Hola ".$message['from']['first_name'].", solo escribe Monto*Tasa y espera el resultado.");
    
        } else {
                $text   = str_replace('x','*',$text);
                $text   = str_replace('X','*',$text);
                $USD = str_word_count($text, 1, '0123456789.')[0];
                $BS = str_word_count($text, 1, '0123456789.')[1];
                $signal = str_word_count($text, 1, '*xX/\def')[0];
                $BS = pow(1000,strlen(stristr($BS, 'k')))*(real)$BS;
                $emoji = "\xE2\x98\x95: Bs ".number_format($BS, 2, ',', '');
    
                if ($signal == 'x' || $signal == '*' || is_null($signal) || $signal == 'X') {
                    $receive = round(($USD-$USD*(0.054)-0.3), 2);
                    $Total = "Bs `".number_format($receive*$BS, 2, ',', '')."`";
                    if ($BS < 2 ) {
                        $Total = "`".number_format($receive*$BS, 2, '.', '')."` $";
                        $emoji = "％: ".number_format($BS, 2, '.', '');
                    }
                    $sent = round((100*($USD+0.3)/94.6),2);
                    if ($BS) {
                        $msg1 = "Envían: `$USD` $
Llegarán: `$receive` $
$emoji
Total: $Total";
                        $Total = "Bs `".number_format($USD*$BS, 2, ',', '')."`";
                        if ($BS < 2) {
                            $Total = "`".number_format($USD*$BS, 2, '.', '')."` $";
                            $emoji = "％: ".number_format($BS, 2, '.', '');
                        }
                        $msg2 = "Envían: `$sent` $
Llegarán: `$USD` $
$emoji
Total: $Total";
                    } else {
                        $msg1 = "Envían: `$USD` $
Llegarán: `$receive` $";
                        $msg2 = "Envían: `$sent` $
Llegarán: `$USD` $";
                    }
                }
                else if ($signal == "/" || $signal == '\\') {
                    $sent = round((100*(($USD/$BS)+0.3)/94.6),2);
                    $receive = round($USD/$BS,2);
                    $Total = number_format($receive*$BS, 2, ',', '');
                    if ($BS < 2 ) {
                        $Total = number_format($USD, 2, '.', '');
                        $emoji = "％: ".number_format($BS, 2, '.', '');
                    }
                    $msg1 = "Envían: `$sent` $
Llegarán: `$receive` $
$emoji
Total: Bs `$Total`";
                }
    
                sendMessage($chat_id, $msg1);
                if ($msg2 !== NULL) {
                    sendMessage($chat_id, $msg2);
                }
                
            }

    }

}

$content = file_get_contents('php://input');
$update = json_decode($content, true);

if (isset($update['message'])) {
    processMessage($update['message']);
    saveUser($update['message']['from']);
}

if (isset($update['inline_query'])) {
    processQuery($update['inline_query']);
    // if (!in_array($update['inline_query']['from']['id'], array(350624626, 270551497, 3247447, 390988751, 8260118, 134852004, 1231821, 214608241, 340381568, 522739070, 196129611, 4769326, 514121441))) {
    // }else {
        // sendMessage($update['inline_query']['from']['id'], "Este bot es privado, para usarlo escribir a @XavierOrejarena");
    // }
    saveUser($update['inline_query']['from']);
}

?>
