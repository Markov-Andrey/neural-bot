Анализатор веса и использование собранного словаря для обновления БД

табл и инкремент:

CREATE TABLE ART_AVG_WEIGHTS (
                                 ID NUMBER PRIMARY KEY,
                                 NAME VARCHAR2(255) NOT NULL UNIQUE,
                                 WEIGHT NUMBER(10) NOT NULL
);

CREATE SEQUENCE art_avg_weights_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER art_avg_weights_bir
    BEFORE INSERT ON ART_AVG_WEIGHTS
    FOR EACH ROW
BEGIN
    IF :NEW.ID IS NULL THEN
        SELECT art_avg_weights_seq.NEXTVAL INTO :NEW.ID FROM dual;
    END IF;
END;
/

`index.php` - выполнение скрипта на обновление, лимит 1000 записей в транзакции

`import.php` - перегнать записи из `cache.json` в БД (1-разовый скрипт)