# TUGAS 3 - Next Steps (Step 6-10)

## Current Status
✅ **Steps 1-5 COMPLETED and PUSHED to GitHub**

Files pushed:
- `TUGAS3_RATU_API_ANALYSIS.md` - API documentation
- `TUGAS3_ARCHITECTURE.md` - Architecture design
- `TUGAS3_PROGRESS.md` - Progress summary
- `portal/service/app/attendance_client.py` - Integration client
- Updated `portal/service/app/main.py` - Portal endpoints with JWT validation
- Updated `portal/service/requirements.txt` - Added PyJWT dependency

---

## Step 6: Test Integration (Ready to Run)

### 6A. Local Testing (if running locally)
```bash
# Start local containers
docker-compose up -d

# Register test user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "role": "admin"
  }'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# Test attendance endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/attendance/E001
```

### 6B. STB Testing (more important)
```bash
# Via SSH to STB
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id

# Go to deployment directory
cd /opt/tst-dina-identity-portal

# First, push updated code if not already there
# (From local machine, push to GitHub, then pull on STB)

# Register test user
curl -s -X POST http://localhost:18081/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "petugas1",
    "password": "secure123",
    "role": "committee"
  }' | jq '.'

# Login
TOKEN=$(curl -s -X POST http://localhost:18081/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"petugas1","password":"secure123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# Test attendance endpoint
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:18081/api/attendance/E001 | jq '.'

# Test check-in endpoint
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"E001","ticket_id":"T001"}' \
  http://localhost:18081/api/checkins | jq '.'

# Test get user checkins
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:18081/api/checkins | jq '.'
```

### Expected Results
- ✅ Register returns: `{"message":"registered","username":"...","role":"..."}`
- ✅ Login returns: `{"access_token":"eyJ...","token_type":"bearer"}`
- ✅ Attendance returns: Attendance data from Ratu
- ✅ Check-in returns: Check-in confirmation
- ✅ Get checkins returns: List of user's check-ins

---

## Step 7: Deploy to STB

### 7A. Update Code on STB
```bash
# On STB
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id "
  cd /opt/tst-dina-identity-portal && \
  git pull origin main && \
  echo 'Code updated'
"
```

### 7B. Rebuild Docker Image
```bash
# On STB
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id "
  cd /opt/tst-dina-identity-portal && \
  docker-compose -f docker-compose.prod.yml down && \
  docker-compose -f docker-compose.prod.yml up -d --build && \
  echo 'Services rebuilt and started'
"
```

### 7C. Verify Deployment
```bash
# Check all containers running
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id "
  docker ps | grep tst-dina
"

# Check logs for errors
ssh -o ProxyCommand='cloudflared access ssh --hostname %h' root@ssh.theokaitou.my.id "
  docker logs portal-service-prod | tail -20
"

# Test health endpoint
curl -s https://dina.theokaitou.my.id:18081/health | jq '.'
```

### Expected Results
- ✅ All 4 containers running (identity-service-prod, portal-service-prod, nginx-proxy-prod, dina-db-prod)
- ✅ Health endpoint shows: attendance_base pointing to https://ratu.theokaitou.my.id
- ✅ No error messages in logs

---

## Step 8: Write Makalah (10-12 pages)

Create file: `TUGAS3_MAKALAH.md`

### Content Structure (suggested page breakdown)
**Pages 1-2: Introduction**
- Background (TST DINA Identity + Ratu Attendance partnership)
- Problem statement (need for integrated system)
- Objectives
- Scope of TUGAS 3

**Pages 3: TUGAS 2 Review**
- System overview
- Technologies used
- Current architecture
- API endpoints

**Pages 4-5: TUGAS 3 Requirements**
- Integration goal
- New features to build
- Data flow requirements
- Security requirements

**Pages 6-7: Architecture Design**
- System diagram (ASCII or Mermaid)
- Component interaction diagram
- Data flow diagrams (auth, attendance query, check-in)
- Security considerations

**Pages 8: Implementation Details**
- AttendanceClient class design
- Portal endpoint implementation
- JWT validation strategy
- Error handling approach

**Pages 9: API Documentation**
- Endpoint specifications
- Request/response examples
- Error scenarios
- Testing examples

**Pages 10: Testing & Results**
- Unit testing approach
- Integration testing results
- curl test commands and outputs
- Performance considerations

**Pages 11: Deployment**
- Docker configuration
- Environment variables
- Deployment procedure
- Verification steps

**Page 12: Conclusion & Future Work**
- Summary of achievements
- Challenges overcome
- Future enhancements
- Lessons learned

### Command to Create Makalah
```bash
# From your machine
nano TUGAS3_MAKALAH.md
# Or copy template and fill in details
```

---

## Step 9: Record Combined Video (10 minutes)

### Video Script Structure
```
0:00-0:30 - INTRO
  "Hello, I'm Dina..."
  "Today I'll show TUGAS 2 and TUGAS 3 of the TST Identity Portal"

0:30-2:00 - TUGAS 2 RECAP & DEMO (1.5 min)
  - Show landing page
  - Explain what TST DINA Identity Portal is
  - Demo: Login → Register → Get user info
  - Show architecture (4 containers, database)
  - Explain: Identity service, Portal service, Nginx proxy
  - Show: Public access via HTTPS

2:00-3:00 - TUGAS 3 INTRO (1 min)
  - Explain: Ratu Attendance Service integration
  - Show: Both systems (Dina + Ratu)
  - Explain: Shared JWT authentication

3:00-7:00 - TUGAS 3 ARCHITECTURE & IMPLEMENTATION (4 min)
  - Show architecture diagram
  - Explain data flow (user → portal → Ratu)
  - Show code: AttendanceClient class
  - Show code: New endpoints (/api/attendance/*, /api/checkins)
  - Demo: Get attendance data from Ratu
  - Demo: Create check-in and see it in Ratu
  - Show: Ratu data displayed in Dina portal

7:00-8:30 - INTEGRATION DEMO (1.5 min)
  - Full workflow demo:
    1. Register user (Dina)
    2. Login (get JWT token from Dina)
    3. Query attendance (from Ratu)
    4. Create check-in (on Ratu via Dina)
  - Show: All data flows correctly
  - Explain: How JWT enables secure cross-domain access

8:30-10:00 - CONCLUSION & SUMMARY (1.5 min)
  - Summary of what was built
  - Benefits of integration
  - Next steps / improvements
  - Thank you
```

### Recording Tips
- Use Zoom, OBS, or built-in screen recording
- Include your voice narration
- Show code and running system
- Make sure audio is clear
- Upload to YouTube (unlisted or public based on requirement)

### Recording Command (Mac)
```bash
# Using built-in QuickTime
open -a QuickTime\ Player
# Then File → New Screen Recording

# Or use ScreenFlow (if installed)
open -a ScreenFlow
```

---

## Step 10: Final Push to GitHub

### Create Proof Document
```bash
# Create TUGAS3_BUKTI_PENYELESAIAN.md with:
# - Screenshots of running system
# - curl test results
# - Architecture diagrams
# - Links to YouTube video
# - Makalah PDF (or MD) link
```

### Push Everything
```bash
git add -A
git commit -m "TUGAS 3 Final Submission: Makalah, video link, complete implementation, proof of integration"
git push origin main
```

### Create Release on GitHub
- Go to GitHub repository
- Create Release
- Tag: v1.0-TUGAS-3-Complete
- Description: Brief summary of TUGAS 3 completion
- Upload Makalah as PDF if needed

---

## Timeline Estimate

| Step | Task | Time Est | Status |
|------|------|----------|--------|
| 6 | Test Integration | 1-2 hours | 📋 Ready to run |
| 7 | Deploy to STB | 30 minutes | 📋 Ready |
| 8 | Write Makalah | 4-5 hours | 📋 Ready (template provided) |
| 9 | Record Video | 2-3 hours | 📋 Ready (script provided) |
| 10 | Final Push | 30 minutes | 📋 Ready |
| **Total** | | **8-11 hours** | ✅ Can be completed today/tomorrow |

---

## Quick Checklist

Before Final Submission:

- [ ] Step 6: Integration tests pass
- [ ] Step 7: Deployed to STB successfully
- [ ] Step 8: Makalah written (10-12 pages)
- [ ] Step 9: Video recorded and uploaded
- [ ] Step 10: All files pushed to GitHub
- [ ] README.md updated with new endpoints
- [ ] TUGAS3_BUKTI_PENYELESAIAN.md created with proof
- [ ] GitHub release created
- [ ] Video link documented

---

## Current File Structure

```
tst-dina-identity-portal/
├── TUGAS2_CHECKLIST.md ✅
├── TUGAS3_RATU_API_ANALYSIS.md ✅
├── TUGAS3_ARCHITECTURE.md ✅
├── TUGAS3_PROGRESS.md ✅
├── TUGAS3_MAKALAH.md ⏳ (Step 8)
├── TUGAS3_BUKTI_PENYELESAIAN.md ⏳ (Step 10)
├── portal/service/
│   ├── app/
│   │   ├── attendance_client.py ✅ (NEW - Step 4)
│   │   ├── main.py ✅ (MODIFIED - Step 5)
│   │   ├── proxy.py ✅
│   │   └── security.py ✅
│   └── requirements.txt ✅ (MODIFIED - added pyjwt)
├── identity/service/
│   ├── app/
│   │   ├── auth.py ✅
│   │   ├── main.py ✅
│   │   └── security.py ✅
│   └── requirements.txt ✅
├── docker-compose.prod.yml ✅
├── .env ✅
├── .env.production ✅
├── README.md ✅
└── ... (other files)
```

---

## Final Notes

**You've completed 50% of TUGAS 3!** 🎉

The hard part (API analysis, architecture design, and implementation) is done.

Now it's just:
1. ✅ Test it works (Step 6)
2. ✅ Deploy it (Step 7)
3. ✅ Document it (Step 8)
4. ✅ Record it (Step 9)
5. ✅ Submit it (Step 10)

**Estimated time to completion: 8-11 hours of focused work**

Good luck! 💪

