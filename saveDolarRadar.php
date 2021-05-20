#!/usr/bin/env php
<?php
    include "connect.php";
    $i = 0;

    $dolartoday = json_decode(utf8_encode(file_get_contents("https://s3.amazonaws.com/dolartoday/data.json")))->USD->dolartoday;
    $dolartoday = number_format($dolartoday, 2, ',', '.');

    $sql = "UPDATE Dolar SET TASA='$dolartoday' WHERE id='$i'";
    if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
    } else {
        echo "Error updating record: " . $link->error;
    }

    // $i++;

    // $bolivarcucuta = json_decode(utf8_encode(file_get_contents("https://s3.amazonaws.com/frontcloud/data.json")))->USDVEF->dolarcucuta_efe;
    // $bolivarcucuta = number_format($bolivarcucuta, 2, ',', '.');

    // $sql = "UPDATE Dolar SET TASA='$bolivarcucuta' WHERE id='$i'";
    // if ($link->query($sql) === TRUE) {
    //     echo "Record updated successfully\n";
    // } else {
    //     echo "Error updating record: " . $link->error;
    // }

    $i++;

    $airtm = file_get_contents("https://rates.airtm.com/");
    preg_match_all('/class="rate--general"/', $airtm, $matches, PREG_OFFSET_CAPTURE);
    $airtm = substr($airtm, $matches[0][0][1]+22, 7);
    $airtm = number_format($airtm, 2, ',', '.');

    $sql = "UPDATE Dolar SET TASA='$airtm' WHERE id='$i'";
    if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
    } else {
        echo "Error updating record: " . $link->error;
    }

    $i++;

    $dicom = file_get_contents("http://www.bcv.org.ve");
    preg_match_all('/USD/', $dicom, $matches, PREG_OFFSET_CAPTURE);
    $dicom = substr($dicom, $matches[0][0][1]+85, 12);
    // $dicom = number_format($dicom, 2, ',', '.');

    $sql = "UPDATE Dolar SET TASA='$dicom' WHERE id='$i'";
    if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
    } else {
        echo "Error updating record: " . $link->error;
    }

    $i++;

    $yadio = json_decode(utf8_encode(file_get_contents("https://api.yadio.io/rate/VES")))->usd;
    $yadio = number_format($yadio, 2, ',', '.');

    $sql = "UPDATE Dolar SET TASA='$yadio' WHERE id='$i'";
    if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
    } else {
        echo "Error updating record: " . $link->error;
    }

    $i++;

    $localbitcoins = json_decode(utf8_encode(file_get_contents("https://localbitcoins.com/bitcoincharts/VES/trades.json")))[0]->price;
    $btc = json_decode(utf8_encode(file_get_contents("https://localbitcoins.com/api/equation/btc_in_usd")))->data;
    $localbitcoins = round($localbitcoins/$btc,2);
    $localbitcoins = number_format($localbitcoins, 2, ',', '.');
    
    $sql = "UPDATE Dolar SET TASA='$localbitcoins' WHERE id='$i'";
    if ($link->query($sql) === TRUE) {
        echo "Record updated successfully\n";
    } else {
        echo "Error updating record: " . $link->error;
    }
?>