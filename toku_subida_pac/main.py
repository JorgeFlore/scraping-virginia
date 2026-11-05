import logging

from config import LOG_FILE
from sftp_client import upload_files
from email_sender import send_report


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():

    logging.info(
        "===== INICIO PROCESO TOKU ====="
    )

    try:

        archivos_ok, archivos_error = upload_files()

        send_report(
            archivos_ok,
            archivos_error
        )

        logging.info(
            f"Archivos OK: {len(archivos_ok)}"
        )

        logging.info(
            f"Archivos Error: {len(archivos_error)}"
        )

    except Exception as e:

        logging.exception(
            f"Error general: {e}"
        )

    logging.info(
        "===== FIN PROCESO TOKU ====="
    )


if __name__ == "__main__":
    main()