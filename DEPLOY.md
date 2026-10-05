# Deployment Guide

SentinelGraph is designed to be easily deployed to modern cloud providers.

## 1. FalkorDB
We recommend using [FalkorDB Cloud](https://falkordb.com/cloud) for a managed experience.
1. Create a free tier cluster.
2. Note the endpoint URL (e.g., `redis://default:password@endpoint:6379`).

## 2. Backend (Render / Railway)
1. Fork this repository.
2. Create a new Web Service on Render or Railway.
3. Point to the `Dockerfile.api`.
4. Set Environment Variables:
   - `FALKORDB_URL` = (from step 1)
   - `ANTHROPIC_API_KEY` = your api key
   - `LLM_MODEL` = claude-3-5-sonnet-20241022
5. (Optional) Deploy a second service for the MCP server using `Dockerfile.mcp` and set `MCP_SERVER_URL`.

## 3. Frontend (Vercel)
1. Import the repository in Vercel.
2. Set the Root Directory to `web`.
3. Set the build command to `npm run build` and output to `dist`.
4. Add Environment Variable:
   - `VITE_API_URL` = (URL of the backend service from step 2).

## Data Seeding
On first boot, run the ingestion script against your production FalkorDB instance:
```bash
export FALKORDB_URL=redis://your-prod-url
python data/gen_security.py
python data/gen_company.py
python graph/ingest.py
```
