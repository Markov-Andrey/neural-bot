<?php

class Database {
    private $conn;

    public function __construct() {
        $this->loadEnv(__DIR__ . '/../.env');
        $this->connect();
    }

    private function loadEnv(string $path): void {
        if (!file_exists($path)) {
            return;
        }

        $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $line) {
            if (strpos(trim($line), '#') === 0 || strpos($line, '=') === false) continue;
            list($name, $value) = explode('=', $line, 2);
            $_ENV[trim($name)] = trim($value);
        }
    }

    private function connect(): void {
        $host = $_ENV['ORACLE_HOST'];
        $port = $_ENV['ORACLE_PORT'];
        $sid = $_ENV['ORACLE_SID'];
        $user = $_ENV['ORACLE_USER'];
        $password = $_ENV['ORACLE_PASSWORD'];

        $dsn = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={$host})(PORT={$port}))(CONNECT_DATA=(SID={$sid})))";

        $this->conn = oci_connect($user, $password, $dsn, 'AL32UTF8');

        if (!$this->conn) {
            $e = oci_error();
            throw new Exception('Connection failed: ' . $e['message']);
        }
    }

    public function getAllWeights(): array {
        $sql = "SELECT NAME, WEIGHT FROM ART_AVG_WEIGHTS";
        $stmt = oci_parse($this->conn, $sql);
        oci_execute($stmt);

        $weights = [];
        while ($row = oci_fetch_assoc($stmt)) {
            $weights[$row['NAME']] = $row['WEIGHT'];
        }

        oci_free_statement($stmt);
        return $weights;
    }

    public function insertArtAvgWeight(string $name, float $weight): void {
        $sql = "
            INSERT INTO ART_AVG_WEIGHTS (ID, NAME, WEIGHT)
            VALUES (art_avg_weights_seq.NEXTVAL, :name, :weight)
        ";

        $stmt = oci_parse($this->conn, $sql);
        oci_bind_by_name($stmt, ":name", $name);
        oci_bind_by_name($stmt, ":weight", $weight);
        oci_execute($stmt, OCI_COMMIT_ON_SUCCESS);
        oci_free_statement($stmt);
    }

    public function artSelect(int $maxRows): array {
        $sql = "
            SELECT ID, NAME, NET_WEIGHT
            FROM (
                SELECT ID, NAME, NET_WEIGHT
                FROM ART
                WHERE CLIENT_ID IN (497, 407, 501)
                  AND NAME IS NOT NULL
                  AND NET_WEIGHT = 200
                  AND LOWER(NAME) NOT LIKE '%mix%'
            )
            WHERE ROWNUM <= :max_rows
        ";

        $stmt = oci_parse($this->conn, $sql);
        oci_bind_by_name($stmt, ":max_rows", $maxRows);
        oci_execute($stmt);

        $results = [];
        while ($row = oci_fetch_assoc($stmt)) {
            $results[] = $row;
        }

        oci_free_statement($stmt);
        return $results;
    }

    public function artUpdate(int $id, float $weight): void {
        $sql = "
            UPDATE ART
            SET NET_WEIGHT = :weight,
                GROSS_WEIGHT = :weight
            WHERE ID = :id
        ";

        $stmt = oci_parse($this->conn, $sql);
        oci_bind_by_name($stmt, ":id", $id);
        oci_bind_by_name($stmt, ":weight", $weight);
        oci_execute($stmt, OCI_COMMIT_ON_SUCCESS);
        oci_free_statement($stmt);
    }

    public function __destruct() {
        if ($this->conn) {
            oci_close($this->conn);
        }
    }
}
