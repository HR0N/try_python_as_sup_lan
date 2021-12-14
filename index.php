<?php
    $command = escapeshellarg('python index2.py');
    $output = shell_exec($command);
    echo $output;
?>