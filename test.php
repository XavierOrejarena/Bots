#!/usr/bin/env php
<?php
    include "connect.php";
    define('BOT_TOKEN', '695950939:AAHfKc9Lv1yceBT9yPkpcxNlAeRsLPuFGHw');
    define('API_URL', 'https://api.telegram.org/bot'.BOT_TOKEN.'/');
    $chat_id = 149273661;
    $text = "INDICADOR\t\t\t\t\t\t\t\tTASA\n";
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
    ?>