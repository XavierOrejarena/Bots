#!/usr/bin/env php
<?php
function getBTCValue() {
	$BINANCE_BTCUSDT = file_get_contents("https://www.bitmex.com/api/v1/instrument?symbol=XBT");
	$BINANCE_BTCUSDT = json_decode($BINANCE_BTCUSDT, true);

  
  return $BINANCE_BTCUSDT[0]['lastPrice'];
}

function getS() {
  include "connect.php";
  $priceBTC = getBTCValue();
  $URL = file_get_contents("https://localbitcoins.com/buy-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  $i = 0;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES' && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $COMPRA = number_format(round($oferta['data']['temp_price']/$priceBTC));
      $sql = "UPDATE LocalBitcoins SET COMPRA='$COMPRA' WHERE id='$i'";
      if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
      } else {
        echo "Error updating record: " . $link->error;
      }
      $i++;
      if ($i > 9){
        $sql = "UPDATE LocalBitcoins SET COMPRA='$priceBTC' WHERE id='$i'";
        $link->query($sql);
        break; 
      }
    }
  }
  
  $URL = file_get_contents("https://localbitcoins.com/sell-bitcoins-online/ve/venezuela/.json");
  $DATA = json_decode($URL, true);
  
  $i = 0;
  foreach ($DATA['data']['ad_list'] as $oferta) {
    if ($oferta['data']['currency'] == 'VES'  && !stripos($oferta['data']['msg'], 'bitmain') && !stripos($oferta['data']['bank_name'], 'bitmain')) {
      $VENTA = number_format(round($oferta['data']['temp_price']/$priceBTC));
      $sql = "UPDATE LocalBitcoins SET VENTA='$VENTA' WHERE id='$i'";
      if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
      } else {
        echo "Error updating record: " . $link->error;
      }
      $i++;
      if ($i > 9) break;
    }
  }
}
getS();
?>