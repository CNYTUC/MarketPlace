from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
TableName = "MC_User"

def get_client() -> Client:
    url  = os.getenv("SUPABASE_URL")
    key  = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL veya SUPABASE_KEY eksik.")
    return create_client(url, key)


# ─────────────────────────────────────────────────────────────────────────────────────────
# ── TUM KULLANCILARI ÇEK ──
# ─────────────────────────────────────────────────────────────────────────────────────────

def get_all_users() -> list[dict]:
    """Tüm kullanıcıları döndürür."""
    client = get_client()
    result = client.table("MC_User").select("*").order("id").execute()
    return result.data

# ─────────────────────────────────────────────────────────────────────────────────────────
# ── TUM HİSSE SENETLERİNİ ÇEK ──
# ─────────────────────────────────────────────────────────────────────────────────────────

def get_all_bist() -> list[dict]:
    """Tüm kullanıcıları döndürür."""
    client = get_client()
    result = client.table("MC_BistList").select("*").order("id").execute()
    return result.data