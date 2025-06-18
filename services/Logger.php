<?php

class Logger {
    private $logDir = __DIR__ . '/../logs';
    private $logFile;
    private $logPath;

    public function __construct() {
        if (!is_dir($this->logDir)) {
            mkdir($this->logDir, 0777, true);
        }

        $this->logFile = date('d.m.Y') . '.log';
        $this->logPath = $this->logDir . '/' . $this->logFile;

        $this->cleanupOldLogs();
    }

    public function info(string $message): void {
        $this->writeLog('INFO', $message);
    }

    public function warning(string $message): void {
        $this->writeLog('WARNING', $message);
    }

    public function error(string $message): void {
        $this->writeLog('ERROR', $message);
    }

    private function writeLog(string $level, string $message): void {
        $timestamp = date('Y-m-d H:i:s');
        $logLine = "{$timestamp} - {$level} - {$message}" . PHP_EOL;
        file_put_contents($this->logPath, $logLine, FILE_APPEND | LOCK_EX);
    }

    private function cleanupOldLogs(): void {
        $cutoff = strtotime('-7 days');

        foreach (scandir($this->logDir) as $file) {
            if (preg_match('/^\d{2}\.\d{2}\.\d{4}\.log$/', $file)) {
                $fileDate = DateTime::createFromFormat('d.m.Y', substr($file, 0, 10));
                if ($fileDate && $fileDate->getTimestamp() < $cutoff) {
                    $fullPath = $this->logDir . '/' . $file;
                    if (!@unlink($fullPath)) {
                        return;
                    }
                }
            }
        }
    }
}
