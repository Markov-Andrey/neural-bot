from services.clean import normalize_text
from services.db_connect import get_oracle_connection
from db import get_all_weights
from services.sql_request import art_select, art_update
from services.log import logger, cleanup_old_logs


def sum_weights_by_name(name, weights_dict, phrases, single_words):
    cleaned_name = normalize_text(name)
    total_weight = 0

    for phrase in phrases:
        if phrase in cleaned_name:
            count = cleaned_name.count(phrase)
            try:
                total_weight += float(weights_dict[phrase]) * count
            except (ValueError, TypeError):
                continue

    words = cleaned_name.split()
    for w in words:
        if w in single_words:
            try:
                total_weight += float(weights_dict[w])
            except (ValueError, TypeError):
                continue

    return total_weight


def main():
    target_weight = 200
    no_weight = 204

    conn = get_oracle_connection()
    cursor = conn.cursor()
    cursor.execute(art_select())
    rows = cursor.fetchall()

    weights_dict = get_all_weights()
    phrases = [k for k in weights_dict if (' ' in k) or ('-' in k)]
    single_words = [k for k in weights_dict if (' ' not in k) and ('-' not in k)]

    try:
        for id, name, net_weight in rows:
            summed_weight = sum_weights_by_name(name, weights_dict, phrases, single_words)

            if summed_weight == 0 or summed_weight == target_weight:
                summed_weight = no_weight

            try:
                cursor.execute(art_update(), {"weight": summed_weight, "id": id})
                logger.info(f"UPD: id={id} name='{name}' weight={summed_weight}")
            except Exception as e:
                logger.error(f"ERROR: ID {id}: {e}")

        conn.commit()

    except Exception as e:
        conn.rollback()
        logger.error(f"ERROR: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    cleanup_old_logs()
    main()
