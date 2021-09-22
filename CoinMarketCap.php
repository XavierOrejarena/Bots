#!/usr/bin/env php
<?php
$url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest';
$parameters = [
  'symbol' => 'WANA'
];

$headers = [
  'Accepts: application/json',
  'X-CMC_PRO_API_KEY: 2d6611e3-3184-4874-9ed1-c7c67c7a9c94'
];
$qs = http_build_query($parameters); // query string encode the parameters
$request = "{$url}?{$qs}"; // create the request URL


$curl = curl_init(); // Get cURL resource
// Set cURL options
curl_setopt_array($curl, array(
  CURLOPT_URL => $request,            // set the request URL
  CURLOPT_HTTPHEADER => $headers,     // set the headers 
  CURLOPT_RETURNTRANSFER => 1         // ask for raw response instead of bool
));

$response = curl_exec($curl); // Send the request, save the response
$data = json_decode($response);
print_r(round($data->data->WANA->quote->USD->price,2)); // print json decoded response
curl_close($curl); // Close request
?>