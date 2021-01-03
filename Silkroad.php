<table>
<?php 
echo "PHP!<br>";
if (!empty($_POST)) {
    echo "<h2>PHP is Fun!</h2>";
    echo "Hello world!<br>";
    foreach ($_POST as $key => $value) {
        echo "<tr>";
        echo "<td>";
        echo $key;
        echo "</td>";
        echo "<td>";
        echo $value;
        echo "</td>";
        echo "</tr>";
    }
}else {
    var_dump($_POST);
}

?>
</table>