# Возвращает SQL-запрос для выбора артикулов с весом 200, без слова 'mix' в названии
def art_select():
    return """
        SELECT ID, NAME, NET_WEIGHT
        FROM ART
        WHERE CLIENT_ID IN (497, 407, 501)
          AND NAME IS NOT NULL
          AND NET_WEIGHT = 200
          AND LOWER(NAME) NOT LIKE '%mix%'
          AND ROWNUM <= 1000
    """

# Возвращает SQL-запрос для обновления веса (нетто и брутто) по ID артикула
def art_update():
    return """
        UPDATE ART
        SET NET_WEIGHT = :weight,
            GROSS_WEIGHT = :weight
        WHERE ID = :id
    """
