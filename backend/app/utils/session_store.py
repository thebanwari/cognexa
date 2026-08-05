import time
import threading
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class SessionData:
    """Data structure for session storage"""
    session_id: str
    data: Dict[str, Any]
    created_at: float
    expires_at: float


class SessionStore:
    """Thread-safe session storage with TTL cleanup"""

    def __init__(self, default_ttl: int = 86400):
        """
        Initialize session store.

        Args:
            default_ttl: Default session TTL in seconds (default 24 hours)
        """
        self.default_ttl = default_ttl
        self.sessions: Dict[str, SessionData] = {}
        self.lock = threading.RLock()
        self._cleanup_thread = None
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        """Start background thread for session cleanup"""
        self._cleanup_thread = threading.Thread(target=self._cleanup_expired_sessions, daemon=True)
        self._cleanup_thread.start()

    def _cleanup_expired_sessions(self):
        """Background task to clean up expired sessions"""
        while True:
            try:
                time.sleep(3600)  # Run every hour
                current_time = time.time()

                with self.lock:
                    expired_sessions = [
                        session_id for session_id, session_data in self.sessions.items()
                        if session_data.expires_at < current_time
                    ]

                    for session_id in expired_sessions:
                        del self.sessions[session_id]

                    if expired_sessions:
                        print(f"Cleaned up {len(expired_sessions)} expired sessions")

            except Exception as e:
                print(f"Error in session cleanup: {e}")

    def create_session(self, data: Dict[str, Any], ttl: Optional[int] = None) -> str:
        """
        Create a new session.

        Args:
            data: Session data to store
            ttl: Session TTL in seconds (uses default if None)

        Returns:
            Session ID
        """
        session_id = self._generate_session_id()
        expires_at = time.time() + (ttl or self.default_ttl)

        session_data = SessionData(
            session_id=session_id,
            data=data.copy(),
            created_at=time.time(),
            expires_at=expires_at
        )

        with self.lock:
            self.sessions[session_id] = session_data

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data.

        Args:
            session_id: Session ID

        Returns:
            Session data if valid, None otherwise
        """
        current_time = time.time()

        with self.lock:
            session_data = self.sessions.get(session_id)

            if session_data is None:
                return None

            if session_data.expires_at < current_time:
                # Session expired, remove it
                del self.sessions[session_id]
                return None

            return session_data.data.copy()

    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Update existing session data.

        Args:
            session_id: Session ID
            data: New session data

        Returns:
            True if updated, False if session doesn't exist
        """
        with self.lock:
            session_data = self.sessions.get(session_id)

            if session_data is None:
                return False

            # Extend session expiry
            session_data.data.update(data)
            session_data.expires_at = time.time() + self.default_ttl

            return True

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session ID

        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            if session_id in self.sessions:
                del self.sessions[session_id]
                return True
            return False

    def session_exists(self, session_id: str) -> bool:
        """
        Check if session exists and is valid.

        Args:
            session_id: Session ID

        Returns:
            True if session exists and is valid
        """
        return self.get_session(session_id) is not None

    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session metadata.

        Args:
            session_id: Session ID

        Returns:
            Session info if exists, None otherwise
        """
        current_time = time.time()

        with self.lock:
            session_data = self.sessions.get(session_id)

            if session_data is None:
                return None

            if session_data.expires_at < current_time:
                # Session expired, remove it
                del self.sessions[session_id]
                return None

            return {
                'session_id': session_data.session_id,
                'created_at': datetime.fromtimestamp(session_data.created_at),
                'expires_at': datetime.fromtimestamp(session_data.expires_at),
                'ttl_remaining': session_data.expires_at - current_time,
                'data_size': len(session_data.data)
            }

    def list_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        List all active sessions (for debugging).

        Returns:
            Dictionary of session info
        """
        current_time = time.time()
        sessions_info = {}

        with self.lock:
            for session_id, session_data in self.sessions.items():
                if session_data.expires_at >= current_time:
                    sessions_info[session_id] = {
                        'created_at': datetime.fromtimestamp(session_data.created_at),
                        'expires_at': datetime.fromtimestamp(session_data.expires_at),
                        'ttl_remaining': session_data.expires_at - current_time,
                        'data_size': len(session_data.data)
                    }

        return sessions_info

    def cleanup_all_sessions(self) -> int:
        """
        Clean up all sessions (for testing).

        Returns:
            Number of sessions cleaned up
        """
        with self.lock:
            count = len(self.sessions)
            self.sessions.clear()
            return count

    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        import uuid
        return f"session_{uuid.uuid4().hex}"


# Global session store instance
session_store = SessionStore()