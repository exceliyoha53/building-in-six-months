import sqlite3


def view_leads():
    db_name = "leads.db"
    print("\nUnlocking the Vault...\n")

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, link FROM articles")
        all_leads = cursor.fetchall()
        if len(all_leads) == 0:
            print("The Vault is Currently empty.Is your Scraper running?")
        else:
            print(f"Found {len(all_leads)} total leads in the database:\n")
            print("-" * 50)

        for row in all_leads:
            lead_id = row[0]  # The ID column
            title = row[1]  # The Title column
            link = row[2]  # The Link column

            print(f"[{lead_id}] {title}")
            print(f"URL: {link}")
            print("-" * 50)
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    view_leads()
