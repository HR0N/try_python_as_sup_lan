<?php
header('Content-type: text/html; charset=utf-8');
$mysqli = new mysqli("pr435071.mysql.tools", "pr435071_api", "s5+5+sYaF6", "pr435071_api");
/* change character set to utf8mb4 */
$mysqli->set_charset("utf8mb4");
$result = $mysqli->query("SELECT json
                         FROM weather2 ORDER BY id DESC LIMIT 1") or die('Invalid query');
while($row = $result->fetch_row()) {
    $rows[]=$row;
}
$result->close();
$mysqli->close();
//echo "<pre>";
//var_dump($rows[0][0]);
//echo "</pre>";
//$str = json_encode(mb_convert_encoding($rows[0][0], "UTF-8", "Windows-1252"));  <====== Тварь! (cp-1252)
$str = json_encode(mb_convert_encoding($rows[0][0], "UTF-8"));
echo $str;