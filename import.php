<?php

require_once __DIR__ . '/services/Logger.php';
require_once __DIR__ . '/services/Database.php';

class JsonImporter
{
    private $db;
    private $logger;
    private $jsonPath;

    public function __construct(Database $db, Logger $logger, string $jsonPath)
    {
        $this->db = $db;
        $this->logger = $logger;
        $this->jsonPath = $jsonPath;
    }

    public function import(): void
    {
        if (!file_exists($this->jsonPath)) {
            $this->logger->error("JSON файл не найден: {$this->jsonPath}");
            echo "JSON файл не найден: {$this->jsonPath}" . PHP_EOL;
            return;
        }

        $jsonContent = file_get_contents($this->jsonPath);
        $data = json_decode($jsonContent, true);

        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->logger->error("Ошибка декодирования JSON: " . json_last_error_msg());
            echo "Ошибка декодирования JSON: " . json_last_error_msg() . PHP_EOL;
            return;
        }

        foreach ($data as $name => $weight) {
            try {
                $this->db->insertArtAvgWeight($name, (float)$weight);
            } catch (Exception $e) {
                $this->logger->error("Ошибка вставки записи (name: {$name}): " . $e->getMessage());
                echo "Ошибка вставки записи (name: {$name}): " . $e->getMessage() . PHP_EOL;
            }
        }

        echo "Импорт из JSON завершен." . PHP_EOL;
        $this->logger->info("Импорт из JSON завершен успешно.");
    }
}

$db = new Database();
$logger = new Logger();
$jsonPath = __DIR__ . '/cache.json';

$importer = new JsonImporter($db, $logger, $jsonPath);
$importer->import();
