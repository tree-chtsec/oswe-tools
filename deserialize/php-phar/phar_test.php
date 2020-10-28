<?php

    class TestObject {
        public function __destruct() {
            echo "Destruct called\n";
        }
    }

    $filename = 'phar://phar.phar/test.txt';
    file_exists($filename);  // file_exists, file_get_contents
?>
