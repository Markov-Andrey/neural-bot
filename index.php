<?php

require_once __DIR__ . '/services/Logger.php';
require_once __DIR__ . '/services/Database.php';
require_once __DIR__ . '/services/TextCleaner.php';

$logger = new Logger();

function sumWeightsByName(string $name, array $weightsDict, array $phrases, array $singleWords): float {
    $cleanedName = TextCleaner::normalize($name);
    $totalWeight = 0.0;

    foreach ($phrases as $phrase) {
        if (strpos($cleanedName, $phrase) !== false) {
            $count = substr_count($cleanedName, $phrase);
            if (isset($weightsDict[$phrase]) && is_numeric($weightsDict[$phrase])) {
                $totalWeight += floatval($weightsDict[$phrase]) * $count;
            }
        }
    }

    $words = explode(' ', $cleanedName);
    foreach ($words as $word) {
        if (in_array($word, $singleWords, true) && isset($weightsDict[$word]) && is_numeric($weightsDict[$word])) {
            $totalWeight += floatval($weightsDict[$word]);
        }
    }

    return $totalWeight;
}

function main() {
    global $logger;

    $targetWeight = 200;
    $noWeight = 204;
    $maxRows = 1000;

    $db = new Database();

    try {
        $rows = $db->artSelect($maxRows);

        if (empty($rows)) {
            echo "INFO: No data" . PHP_EOL;
            return;
        }

        $weightsDict = $db->getAllWeights();

        $phrases = [];
        $singleWords = [];
        foreach ($weightsDict as $key => $value) {
            if (strpos($key, ' ') !== false || strpos($key, '-') !== false) {
                $phrases[] = $key;
            } else {
                $singleWords[] = $key;
            }
        }

        $updated = 0;
        $firstId = $rows[0]['ID'];
        $lastId = $rows[count($rows) - 1]['ID'];

        foreach ($rows as $row) {
            $id = $row['ID'];
            $name = $row['NAME'];
            $netWeight = $row['NET_WEIGHT'];

            $summedWeight = sumWeightsByName($name, $weightsDict, $phrases, $singleWords);

            if ($summedWeight == 0 || $summedWeight == $targetWeight) {
                $summedWeight = $noWeight;
            }

            try {
                $db->artUpdate((int)$id, (float)$summedWeight);
                $updated++;
            } catch (Exception $e) {
                $logger->error("ERROR: ID {$id}: " . $e->getMessage());
                echo "ERROR: ID {$id}: " . $e->getMessage() . PHP_EOL;
            }
        }

        $msg = "UPD ID's: {$firstId} → {$lastId}, total: {$updated}";
        $logger->info($msg);
        echo $msg . PHP_EOL;

    } catch (Exception $e) {
        $logger->error("ERROR: " . $e->getMessage());
        echo "ERROR: " . $e->getMessage() . PHP_EOL;
    }
}

main();
