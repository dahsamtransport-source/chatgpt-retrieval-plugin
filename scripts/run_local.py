"""Start the real API on loopback using local-only credentials (never printed)."""
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / '.local' / 'runtime.env', override=False)
load_dotenv(ROOT / '.env.local', override=False)
if not os.environ.get('OPENAI_API_KEY'):
    print('OpenAI key missing: API/database can start, embedding search is unavailable.', flush=True)

if __name__ == '__main__':
    uvicorn.run('server.main:app', host='127.0.0.1', port=8000)
