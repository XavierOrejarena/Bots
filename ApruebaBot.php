#!/usr/bin/env php
<?php
//@apruebabot
define('BOT_TOKEN', '695950939:');
define('TOKEN_BOT', 'AAHfKc9Lv1yceBT9yPkpcxNlAeRsLPuFGHw');
define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.TOKEN_BOT.'/');
define('WEBHOOK_URL', 'https://vps239318.vps.ovh.ca/xavier/ApruebaBot.php');


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

class Field_calculate {
    const PATTERN = '/(?:\-?\d+(?:\.?\d+)?[\+\-\*\/])+\-?\d+(?:\.?\d+)?/';

    const PARENTHESIS_DEPTH = 10;

    public function calculate($input){
        if(strpos($input, '+') != null || strpos($input, '-') != null || strpos($input, '/') != null || strpos($input, '*') != null){
            //  Remove white spaces and invalid math chars
            $input = str_replace(',', '.', $input);
            $input = preg_replace('[^0-9\.\+\-\*\/\(\)]', '', $input);

            //  Calculate each of the parenthesis from the top
            $i = 0;
            while(strpos($input, '(') || strpos($input, ')')){
                $input = preg_replace_callback('/\(([^\(\)]+)\)/', 'self::callback', $input);

                $i++;
                if($i > self::PARENTHESIS_DEPTH){
                    break;
                }
            }

            //  Calculate the result
            if(preg_match(self::PATTERN, $input, $match)){
                return $this->compute($match[0]);
            }
            // To handle the special case of expressions surrounded by global parenthesis like "(1+1)"
            if(is_numeric($input)){
                return $input;
            }

            return 0;
        }

        return $input;
    }

    private function compute($input){
        $compute = create_function('', 'return '.$input.';');

        return 0 + $compute();
    }

    private function callback($input){
        if(is_numeric($input[1])){
            return $input[1];
        }
        elseif(preg_match(self::PATTERN, $input[1], $match)){
            return $this->compute($match[0]);
        }

        return 0;
    }
}

function processQuery($inline_query)
{
    $results = [];

    if (empty($inline_query['query'])) {
        $results[] = [
            'type'         => 'article',
            'id'           => '0',
            'title'        => 'Esperando una consulta...',
            'message_text' => '5/7+50-4 = `81`',
            'description'  => 'Ejemplo: 5/7+50-4',
            'parse_mode'   => 'markdown',
        ];
    } else {
        $text = $inline_query['query'];
        
        $Cal = new Field_calculate();
        
        $result = $Cal->calculate($text);
        $ESresult = str_replace('.', ',', $result);
        $results[] = [
            'type'         => 'article',
            'id'           => gen_uuid(),
            'title'        => $ESresult,
            'message_text' => "`$ESresult`",
            'parse_mode'   => 'markdown',
        ];
        $RES = str_replace("*","\*", $text);
        $results[] = [
            'type'         => 'article',
            'id'           => gen_uuid(),
            'title'        => "$text = $ESresult",
            'message_text' => "$RES *bold text*",
            'parse_mode'   => 'MarkdownV2',
        ];
    }

    apiRequest('answerInlineQuery', array('inline_query_id' => $inline_query['id'], 'results' => $results, 'cache_time' => 0));
}

if (php_sapi_name() == 'cli') {
    // if run from console, set or delete webhook
  apiRequest('setWebhook', ['url' => isset($argv[1]) && $argv[1] == 'delete' ? '' : WEBHOOK_URL]);
    exit;
}

function processMessage($message) {
    $message_id = $message['message_id'];
    $chat_id = $message['chat']['id'];
    $text = $message['text'];    
    $Cal = new Field_calculate();
    $result = $Cal->calculate($text);
    $ESresult = "`".str_replace('.', ',', $result)."`";
    apiRequest("sendMessage", array('chat_id' => $chat_id, "text" => $ESresult, "parse_mode" => "markdown"));
}

$content = file_get_contents('php://input');
$update = json_decode($content, true);

if (isset($update['message'])) {
    processMessage($update['message']);
    // saveUser($update['message']['from']);
}

if (isset($update['inline_query'])) {
    processQuery($update['inline_query']);
    // if (!in_array($update['inline_query']['from']['id'], array(350624626, 270551497, 3247447, 390988751, 8260118, 134852004, 1231821, 214608241, 340381568, 522739070, 196129611, 4769326, 514121441))) {
    // }else {
        // sendMessage($update['inline_query']['from']['id'], "Este bot es privado, para usarlo escribir a @XavierOrejarena");
    // }
    // saveUser($update['inline_query']['from']);
}

?>