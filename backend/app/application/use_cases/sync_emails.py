from app.domain.ports import EmailSourcePort, ClassifierPort, LogRepositoryPort
from app.domain.entities import Category, ClassificationLog
from app.infrastructure.monitoring.drift import drift_monitor

class SyncEmailsUseCase:
    def __init__(
        self,
        email_source: EmailSourcePort,
        classifier: ClassifierPort,
        repo: LogRepositoryPort,
        profile_id: str,
        tokenizer,
    ):
        self.email_source = email_source
        self.classifier = classifier
        self.repo = repo
        self.profile_id = profile_id
        self.tokenizer = tokenizer

    def run(self, stop_event=None):
        print("[DEBUG] Starting SyncEmailsUseCase.run()")

        for msg_id, email in self.email_source.fetch_unread():
            if stop_event and stop_event.is_set():
                print("[DEBUG] Stopping processing due to stop_event")
                return

            print(f"[DEBUG] Processing email {msg_id} - Subject: {email.subject}")

            result = self._classify_email(msg_id, email)
            if not result:
                continue
                        
            drift_monitor.record(result.category == Category.UNPRODUCTIVE)

            folder = "Productive" if result.category == Category.PRODUCTIVE else "Unproductive"
            result.extra = {**(result.extra or {}), "profile_id": self.profile_id, "moved_to": folder}

            log = ClassificationLog(
                profile_id=self.profile_id,
                category=result.category,
                reason=result.reason,
                suggested_reply=result.suggested_reply,
                subject=email.subject,
                sender=email.sender,
                body_excerpt=(email.body or "")[:200],
                extra=result.extra,
            )

            self._save_log(msg_id, log)
            self._move_email(msg_id, folder)

        print("[DEBUG] Finished SyncEmailsUseCase.run()")

    def _classify_email(self, msg_id, email):
        try:
            tokens = self.tokenizer.tokenize(email.body or "")
            result = self.classifier.classify(email, tokens=tokens)
            print(f"[DEBUG] Classification: {result.category}")
            return result
        except Exception as e:
            print(f"[ERROR] Failed to classify {msg_id}: {e}")
            return None

    def _save_log(self, msg_id, log: ClassificationLog):
        try:
            self.repo.save(log)
            print(f"[DEBUG] Log saved to repository for {msg_id}")
        except Exception as e:
            print(f"[ERROR] Failed to save log to repository: {e}")

    def _move_email(self, msg_id, folder: str):
        try:
            self.email_source.move_to_folder(msg_id, folder)
            print(f"[DEBUG] Email {msg_id} successfully moved to {folder}")
        except Exception as e:
            print(f"[WARN] Failed to move {msg_id} to {folder}: {e}")
