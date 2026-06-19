from phase2.services.gmail_service import (
    read_unread_emails
)

emails = read_unread_emails()

print("RESULT:")
print(emails)